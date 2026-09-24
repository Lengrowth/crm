"""Isolated LenERP relying-party bridge for the Phase 03 synthetic rollout.

This is a temporary authorization-code broker boundary. It never receives or
stores a control-plane password, control-plane cookie, Frappe cookie, or
reusable bearer token. A maintained OIDC client/provider should replace this
module once the provider contract and callback infrastructure are approved.
"""

from __future__ import annotations

import hashlib
import json
import secrets
from base64 import urlsafe_b64encode
from contextlib import contextmanager
from urllib.parse import urlencode, urlsplit

import frappe
import requests
from frappe.exceptions import DuplicateEntryError

from lenerp_core.phase4 import extend_bootinfo as extend_phase4_bootinfo


MANAGED_ROLES = {
    "Champion Administrator",
    "Champion Dispatcher",
    "Champion Sales User",
    "Champion Accounting User",
    "Champion Inventory Manager",
    "Champion Field Technician",
    "Champion HR Payroll User",
    "Champion Quality Support User",
    "Champion Read Only User",
    "Champion Platform Operator",
}
DEFAULT_ROLE_PROFILES = {"champion-v1": ["Champion Sales User"]}
_STATE_COOKIE = "lenerp_sso_state"
_STATE_TTL_SECONDS = 300


def _conf(name: str, default: str | None = None) -> str | None:
    value = frappe.conf.get(name)
    return str(value) if value is not None else default


def enabled() -> bool:
    return str(_conf("lenerp_sso_enabled", "0")).lower() in {"1", "true", "yes", "on"}


def _jit_enabled() -> bool:
    return str(_conf("lenerp_sso_jit_enabled", "0")).lower() in {"1", "true", "yes", "on"}


def _control_plane_url() -> str:
    value = (_conf("lenerp_control_plane_url") or "").rstrip("/")
    return _validated_control_plane_url(value)


def _validated_control_plane_url(value: str) -> str:
    parsed = urlsplit(value)
    if not parsed.hostname or (parsed.scheme != "https" and parsed.hostname not in {"localhost", "127.0.0.1"}):
        frappe.throw("Central sign-in is not configured for this ERP site.")
    return value


def _control_plane_api_url() -> str:
    value = (_conf("lenerp_control_plane_api_url", _control_plane_url()) or "").rstrip("/")
    return _validated_control_plane_url(value)


def _tls_verify() -> str | bool:
    """Use the system trust store unless an isolated staging CA is configured."""
    return _conf("lenerp_sso_ca_bundle") or True


def _client_id() -> str:
    return _conf("lenerp_sso_client_id", "lenerp-erp") or "lenerp-erp"


def _audience() -> str:
    return _conf("lenerp_sso_audience", _client_id()) or _client_id()


def _cache_key(state: str) -> str:
    return f"lenerp-sso:{hashlib.sha256(state.encode('utf-8')).hexdigest()}"


def _state_binding(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _set_state_cookie(value: str, *, delete: bool = False) -> None:
    manager = getattr(frappe.local, "cookie_manager", None)
    if manager is None:
        frappe.throw("Central sign-in is not configured for this ERP site.")
    if delete:
        manager.delete_cookie(_STATE_COOKIE)
    else:
        manager.set_cookie(_STATE_COOKIE, value, max_age=_STATE_TTL_SECONDS, httponly=True, secure=True, samesite="Lax")


def _safe_path(path: str) -> str:
    candidate = path or "/app"
    parsed = urlsplit(candidate)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or "\\" in candidate:
        frappe.throw("The requested ERP destination is not allowed.")
    if not candidate.startswith("/") or candidate.startswith("//") or ".." in candidate.split("/"):
        frappe.throw("The requested ERP destination is not allowed.")
    return candidate


def _start_transaction(next_path: str = "/app") -> str:
    if not enabled():
        frappe.throw("Central ERP sign-in is not enabled for this site.")
    tenant_id = _conf("lenerp_control_plane_tenant_id")
    if not tenant_id:
        frappe.throw("Central sign-in is not configured for this ERP site.")
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(48)
    challenge = urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    callback = frappe.utils.get_url("/api/method/lenerp_core.sso.callback")
    transaction = {
        "state": state,
        "code_verifier": verifier,
        "tenant_id": tenant_id,
        "callback": callback,
        "requested_path": _safe_path(next_path),
    }
    browser_nonce = secrets.token_urlsafe(32)
    transaction["browser_binding"] = _state_binding(browser_nonce)
    frappe.cache().set_value(_cache_key(state), json.dumps(transaction), expires_in_sec=300)
    _set_state_cookie(browser_nonce)
    query = urlencode(
        {
            "tenant_id": tenant_id,
            "client_id": _client_id(),
            "audience": _audience(),
            "redirect_uri": callback,
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "requested_path": transaction["requested_path"],
        }
    )
    return f"{_control_plane_url()}/sso/authorize?{query}"


@frappe.whitelist(allow_guest=True)
def begin(next_path: str = "/app") -> dict[str, str]:
    return {"authorization_url": _start_transaction(next_path)}


def _redirect_to(url: str) -> None:
    if getattr(getattr(frappe.local, "request", None), "path", "").startswith("/api/"):
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = url
        frappe.local.response["http_status_code"] = 302
        return
    frappe.redirect(url)


@frappe.whitelist(allow_guest=True)
def direct_visit(next_path: str = "/app") -> None:
    _redirect_to(_start_transaction(next_path))


def _read_transaction(state: str) -> dict[str, str]:
    raw = frappe.cache().get_value(_cache_key(state))
    if not raw:
        frappe.throw("This sign-in link is expired. Start again from LenERP.")
    transaction = json.loads(raw) if isinstance(raw, str) else raw
    browser_nonce = getattr(getattr(frappe.local, "request", None), "cookies", {}).get(_STATE_COOKIE)
    if not isinstance(transaction, dict) or transaction.get("state") != state or not browser_nonce or not secrets.compare_digest(str(transaction.get("browser_binding", "")), _state_binding(browser_nonce)):
        frappe.throw("This sign-in request is invalid. Start again from LenERP.")
    return transaction


@contextmanager
def _advisory_lock(key: str, timeout: int = 5):
    """Use the MariaDB advisory-lock primitive available on the staging bench."""
    result = frappe.db.sql("SELECT GET_LOCK(%s, %s)", (key, timeout))
    if not result or result[0][0] != 1:
        frappe.throw("This sign-in request is busy. Retry safely from LenERP.")
    try:
        yield
    finally:
        frappe.db.sql("SELECT RELEASE_LOCK(%s)", (key,))


def _consume_transaction(state: str) -> dict[str, str]:
    """Atomically consume a browser-bound transaction before creating a session."""
    with _advisory_lock(_cache_key(state), timeout=5):
        transaction = _read_transaction(state)
        frappe.cache().delete_value(_cache_key(state))
        _set_state_cookie("", delete=True)
        return transaction


def _role_profile(version: str) -> list[str]:
    configured = _conf("lenerp_sso_role_profiles")
    if configured:
        try:
            profiles = json.loads(configured) if isinstance(configured, str) else configured
            roles = profiles.get(version, [])
            if isinstance(roles, list) and all(isinstance(role, str) for role in roles):
                return sorted(set(roles) & MANAGED_ROLES)
        except (TypeError, ValueError, json.JSONDecodeError):
            frappe.throw("The configured ERP role profile is invalid.")
    return DEFAULT_ROLE_PROFILES.get(version, [])


def _break_glass_user() -> str:
    return _conf("lenerp_break_glass_user", "Administrator") or "Administrator"


def _same_identity(left: object, right: object) -> bool:
    return str(left or "").strip().casefold() == str(right or "").strip().casefold()


def _provision_user(email: str, full_name: str, role_profile_version: str) -> tuple[str, bool]:
    if _same_identity(email, _break_glass_user()):
        frappe.throw("The break-glass account is not managed by central sign-in.")
    existing_name = frappe.db.exists("User", {"email": email})
    created = not bool(existing_name)
    if created:
        if not _jit_enabled():
            frappe.throw("Just-in-time ERP user provisioning is not enabled for this site.")
        try:
            user = frappe.get_doc({"doctype": "User", "email": email, "first_name": full_name, "enabled": 1, "user_type": "System User", "send_welcome_email": 0})
            user.insert(ignore_permissions=True)
        except DuplicateEntryError:
            existing_name = frappe.db.exists("User", {"email": email})
            if not existing_name:
                raise
            created = False
            user = frappe.get_doc("User", existing_name)
    else:
        user = frappe.get_doc("User", existing_name)
        if not user.enabled:
            frappe.throw("The ERP user is inactive.")
        user.first_name = full_name or user.first_name
    frappe.db.sql("SELECT name FROM `tabUser` WHERE name=%s FOR UPDATE", (user.name,))
    roles = _role_profile(role_profile_version)
    if not roles:
        frappe.throw("The approved ERP role profile is not available.")
    user.set("roles", [{"role": role} for role in [*sorted({row.role for row in user.roles if row.role not in MANAGED_ROLES}), *roles]])
    user.save(ignore_permissions=True)
    return user.name, created


@frappe.whitelist(allow_guest=True)
def callback(code: str | None = None, state: str | None = None) -> None:
    if not enabled() or not code or not state:
        frappe.throw("The central sign-in response is incomplete. Start again safely.")
    transaction = _read_transaction(state)
    try:
        response = requests.post(
            f"{_control_plane_api_url()}/api/sso/token",
            json={
                "code": code,
                "client_id": _client_id(),
                "audience": _audience(),
                "redirect_uri": transaction["callback"],
                "code_verifier": transaction["code_verifier"],
                "client_secret": _conf("lenerp_sso_exchange_secret"),
            },
            timeout=10,
            verify=_tls_verify(),
        )
    except requests.RequestException:
        frappe.cache().delete_value(_cache_key(state))
        frappe.throw("The control plane is temporarily unavailable. Retry safely.")
    if response.status_code != 200:
        frappe.cache().delete_value(_cache_key(state))
        frappe.throw(f"Central sign-in could not be completed (token exchange status {response.status_code}). Retry safely or contact an administrator.")
    try:
        token = response.json()
    except (TypeError, ValueError):
        frappe.cache().delete_value(_cache_key(state))
        frappe.throw("Central sign-in returned an invalid response. Retry safely.")
    if not isinstance(token, dict):
        frappe.cache().delete_value(_cache_key(state))
        frappe.throw("Central sign-in returned an invalid response. Retry safely.")
    expected_issuer = _control_plane_url()
    required_fields = ("email", "control_plane_user_id", "organization_id", "role_profile_version")
    if (
        token.get("issuer") != expected_issuer
        or token.get("audience") != _audience()
        or token.get("client_id") != _client_id()
        or token.get("tenant_id") != transaction["tenant_id"]
        or any(not isinstance(token.get(field), str) or not token[field] for field in required_fields)
    ):
        frappe.cache().delete_value(_cache_key(state))
        frappe.throw("Central sign-in returned an invalid tenant or issuer.")
    transaction = _consume_transaction(state)
    user_name, created = _provision_user(token["email"], token.get("full_name", ""), token["role_profile_version"])
    try:
        mapping = requests.post(
            f"{_control_plane_api_url()}/api/sso/mappings",
            json={
                "exchange_handle": token["mapping_handle"],
                "client_secret": _conf("lenerp_sso_exchange_secret"),
                "erp_user": user_name,
            },
            timeout=10,
            verify=_tls_verify(),
        )
        mapping.raise_for_status()
    except requests.RequestException:
        if created:
            frappe.db.set_value("User", user_name, "enabled", 0, update_modified=False)
        frappe.throw("Central sign-in could not save the identity mapping. Retry safely.")
    frappe.local.flags.lenerp_sso_authenticated = True
    frappe.local.login_manager.login_as(user_name)
    _redirect_to(frappe.utils.get_url(transaction["requested_path"]))


def extend_bootinfo(bootinfo: dict[str, object]) -> None:
    extend_phase4_bootinfo(bootinfo)
    if not enabled() or frappe.session.user == "Guest":
        return
    tenant_id = _conf("lenerp_control_plane_tenant_id")
    organization_id = _conf("lenerp_control_plane_organization_id")
    if tenant_id and organization_id:
        bootinfo["lenerp_control_plane_return_url"] = f"{_control_plane_url()}/app/tenants/{tenant_id}?organization_id={organization_id}"
        bootinfo["lenerp_control_plane_label"] = "LenERP Control Plane"


def on_login(login_manager: object) -> None:
    login_identity = getattr(login_manager, "user", None) or getattr(login_manager, "username", None)
    if (
        not enabled()
        or _same_identity(frappe.session.user, "Guest")
        or _same_identity(frappe.session.user, _break_glass_user())
        or _same_identity(login_identity, _break_glass_user())
    ):
        return
    if getattr(frappe.local.flags, "lenerp_sso_authenticated", False):
        return
    frappe.local.login_manager.logout()
    frappe.throw("Use LenERP Control Plane sign-in for this ERP site.")
