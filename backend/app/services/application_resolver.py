from __future__ import annotations

"""Deterministic application requirements for tenant provisioning.

The control plane owns module metadata.  This module turns that metadata into
an ordered, version-pinned application plan while keeping platform apps
separate from module-requested apps.  It deliberately contains no provider
side effects; callers must validate the plan before mutating a site.
"""

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class ApplicationPin:
    name: str
    version: str
    commit: str
    source: str
    license: str = ""
    compatibility_status: str = "verified"
    compatibility_reason: str = ""


@dataclass(frozen=True)
class ApplicationRequirement:
    pin: ApplicationPin
    required_by: tuple[str, ...]


@dataclass(frozen=True)
class ApplicationResolution:
    ordered: tuple[ApplicationRequirement, ...]

    @property
    def applications(self) -> tuple[str, ...]:
        return tuple(item.pin.name for item in self.ordered)

    @property
    def exact_versions(self) -> dict[str, str]:
        return {item.pin.name: item.pin.version for item in self.ordered}

    @property
    def commits(self) -> dict[str, str]:
        return {item.pin.name: item.pin.commit for item in self.ordered}

    @property
    def module_applications(self) -> tuple[str, ...]:
        return tuple(item.pin.name for item in self.ordered if item.pin.source == "module")

    @property
    def platform_applications(self) -> tuple[str, ...]:
        return tuple(item.pin.name for item in self.ordered if item.pin.source == "platform")

    @property
    def unverified_applications(self) -> tuple[str, ...]:
        return tuple(item.pin.name for item in self.ordered if item.pin.compatibility_status != "verified")


# These values are the reviewed Frappe v15 staging baseline.  HRMS is pinned
# to an immutable upstream tag/commit; it is not a floating branch dependency.
PLATFORM_APPLICATION_PINS: tuple[ApplicationPin, ...] = (
    ApplicationPin("frappe", "15.119.1", "edae775dd36b6c4ad7acab10230262bd74040765", "platform"),
    ApplicationPin("erpnext", "15.120.0", "945e825bee3d0d645f6cb59bcaab90fcbfb98ce3", "platform"),
    ApplicationPin("lenerp_core", "0.2.0", "f58bc5f7c0eaa411c1d099f5e722c0bd32a7bc22", "platform"),
)

MODULE_APPLICATION_PINS: dict[str, ApplicationPin] = {
    "hrms": ApplicationPin(
        "hrms",
        "15.64.1",
        "e68a3deaa95ae5b2c3d743297d0a4ab505733fc1",
        "module",
        "GNU General Public License (v3)",
        "verified",
        "Verified by the clean disposable Frappe/ERPNext/HRMS/lenerp_core install recorded in ops/staging/evidence/phase2-clean-disposable-install.json.",
    ),
}

_INSTALL_ORDER = {name: index for index, name in enumerate(("frappe", "erpnext", "hrms", "lenerp_core"))}


def _module_value(module: Any, name: str, default: Any = None) -> Any:
    if isinstance(module, dict):
        return module.get(name, default)
    return getattr(module, name, default)


def calculate_required_applications(modules: Iterable[Any], *, include_platform: bool = True) -> ApplicationResolution:
    """Calculate a stable, deduplicated application plan from module metadata.

    Missing application pins and conflicting exact pins are rejected before a
    provider is called.  The returned order is stable and follows the safe
    installation order for the current Frappe baseline.
    """

    requirements: dict[str, tuple[ApplicationPin, set[str]]] = {}
    if include_platform:
        for pin in PLATFORM_APPLICATION_PINS:
            requirements[pin.name] = (pin, {"platform"})

    for module in modules:
        code = str(_module_value(module, "code", "")).strip().lower()
        app_name = str(_module_value(module, "required_app", "") or "").strip().lower()
        if not app_name:
            continue
        pin = MODULE_APPLICATION_PINS.get(app_name)
        if pin is None:
            # Existing ERPNext-backed modules are already covered by the
            # platform pin.  Any genuinely new application must be pinned in
            # this map before it can be provisioned.
            if app_name == "erpnext":
                pin = next(item for item in PLATFORM_APPLICATION_PINS if item.name == "erpnext")
            elif app_name == "lenerp_core":
                pin = next(item for item in PLATFORM_APPLICATION_PINS if item.name == "lenerp_core")
            else:
                raise ValueError(f"No immutable application pin exists for module {code}: {app_name}.")
        existing = requirements.get(app_name)
        if existing is None:
            requirements[app_name] = (pin, {code})
            continue
        existing_pin, required_by = existing
        if existing_pin.version != pin.version or existing_pin.commit != pin.commit:
            raise ValueError(f"Conflicting application pins for {app_name}.")
        required_by.add(code)

    ordered = sorted(
        (ApplicationRequirement(pin=pin, required_by=tuple(sorted(required_by))) for pin, required_by in requirements.values()),
        key=lambda item: (_INSTALL_ORDER.get(item.pin.name, 1000), item.pin.name),
    )
    return ApplicationResolution(tuple(ordered))


def compare_installed_applications(
    installed_apps: dict[str, str] | list[str] | tuple[str, ...],
    resolution: ApplicationResolution,
    installed_commits: dict[str, str] | None = None,
) -> tuple[list[str], list[str]]:
    """Return missing and incompatible app names from a provider readback."""

    if isinstance(installed_apps, dict):
        installed = {str(name): str(version or "") for name, version in installed_apps.items()}
    else:
        installed = {str(name): "" for name in installed_apps}
    missing: list[str] = []
    incompatible: list[str] = []
    commits = {str(name): str(commit or "") for name, commit in (installed_commits or {}).items()}
    for requirement in resolution.ordered:
        actual = installed.get(requirement.pin.name)
        if actual is None:
            missing.append(requirement.pin.name)
        elif requirement.pin.version and actual != requirement.pin.version:
            incompatible.append(f"{requirement.pin.name} (expected {requirement.pin.version}, read {actual or 'unknown'})")
        elif requirement.pin.commit and commits.get(requirement.pin.name) != requirement.pin.commit:
            incompatible.append(f"{requirement.pin.name} commit (expected {requirement.pin.commit}, read {commits.get(requirement.pin.name) or 'unknown'})")
    return sorted(missing), sorted(incompatible)
