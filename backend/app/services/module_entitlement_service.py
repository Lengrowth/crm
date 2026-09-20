from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.domain import (
    ImplementationProject,
    ImplementationTemplate,
    Module,
    ModuleApplicationStatus,
    ModuleBundle,
    ModuleBundleItem,
    ModuleEntitlementAudit,
    ModuleEntitlementRequest,
    OrganizationModule,
    SaaSUser,
    Subscription,
    Tenant,
)
from app.schemas.modules import (
    ModuleAuditRead,
    ModuleBundleItemRead,
    ModuleBundleRead,
    ModuleChangeRequest,
    ModuleChangeResult,
    ModuleEffectiveItem,
    ModuleEffectiveRead,
    ModulePreviewRead,
    ModuleReversalRequest,
)
from app.services.application_resolver import calculate_required_applications


class ModuleEntitlementError(Exception):
    pass


class ModuleEntitlementNotFound(ModuleEntitlementError):
    pass


class ModuleEntitlementAccessError(ModuleEntitlementError):
    pass


class ModuleEntitlementValidationError(ModuleEntitlementError):
    pass


class ModuleDependencyConflictError(ModuleEntitlementValidationError):
    def __init__(self, conflicts: list[tuple[str, str]]) -> None:
        self.conflicts = conflicts
        details = ", ".join(f"{root} depends on {dependency} (requires {dependency})" for root, dependency in conflicts)
        super().__init__(f"Dependency conflict: explicit disable cannot be applied because {details}.")


MODULE_WRITE_ROLES = {"owner", "admin", "implementation_manager"}

# Champion's primary navigation deliberately keeps these capabilities out of
# view until their owning workflow is configured and verified. This is a
# presentation contract only; it never changes catalog or entitlement state.
CHAMPION_PRESERVED_HIDDEN_CODES = {"manufacturing"}
CHAMPION_HRMS_GATED_CODES = {"hr", "payroll"}


class ModuleEntitlementService:
    """Deterministic control-plane module resolution.

    Precedence is safe-empty, active plan defaults, latest implementation
    template defaults, requested bundle, and explicit organization overrides.
    Explicit disables win over inherited sources; dependencies are closed last.
    This service never changes ERP application or verification state in preview
    or apply.
    """

    def list_enabled_modules(self, organization_id: str, session: Session | None = None) -> list[str]:
        return self.resolve(session, organization_id).effective_codes if session else []

    def list_bundles(self, session: Session) -> list[ModuleBundleRead]:
        bundles = session.execute(select(ModuleBundle).where(ModuleBundle.is_active.is_(True)).order_by(ModuleBundle.bundle_key.asc(), ModuleBundle.version.desc())).scalars().all()
        return [self._bundle_read(session, bundle) for bundle in bundles]

    def list_catalog(self, session: Session) -> list[Module]:
        return list(self._catalog(session).values())

    def list_public_catalog(self, session: Session) -> list[Module]:
        return [module for module in self.list_catalog(session) if module.is_active and module.is_marketed and module.administrative_visibility == "public"]

    def module_by_code(self, session: Session, code: str) -> Optional[Module]:
        """Resolve a public/stable module key to its canonical catalog row."""
        catalog = self._catalog(session)
        return catalog.get(self._canonical_code(catalog, code))

    def resolve_requested_codes(
        self,
        session: Session,
        requested_codes: list[str],
        bundle_key: Optional[str] = None,
        bundle_version: Optional[int] = None,
    ) -> list[str]:
        catalog = self._catalog(session)
        selected = {self._canonical_code(catalog, code) for code in requested_codes}
        if bundle_key:
            bundle = self._find_bundle(session, bundle_key, bundle_version)
            selected.update(self._canonical_code(catalog, item.code) for item in self._bundle_items(session, bundle.id))
        closed = self._close_dependencies(catalog, selected)
        self._validate_selection(catalog, closed)
        return sorted(closed, key=lambda code: (catalog[code].display_order, code))

    def validate_requested_selection(
        self,
        session: Session,
        requested_codes: list[str],
        bundle_key: Optional[str] = None,
        bundle_version: Optional[int] = None,
    ) -> list[str]:
        """Validate public request metadata without creating entitlements."""
        return self.resolve_requested_codes(session, requested_codes, bundle_key, bundle_version)

    def resolve(self, session: Session, organization_id: str, *, enable_codes: Optional[list[str]] = None, disable_codes: Optional[list[str]] = None, clear_codes: Optional[list[str]] = None, bundle_key: Optional[str] = None, bundle_version: Optional[int] = None) -> ModuleEffectiveRead:
        catalog = self._catalog(session)
        canonical = {code: module for code, module in catalog.items() if module.alias_of is None}
        explicit = self._explicit_states(session, organization_id)
        selected: set[str] = set()
        sources: dict[str, list[str]] = {}
        warnings: list[str] = []

        plan_codes, template_codes = self._inherited_codes(session, organization_id)
        for code in plan_codes:
            self._add_source(selected, sources, self._canonical_code(catalog, code), "plan default")
        for code in template_codes:
            self._add_source(selected, sources, self._canonical_code(catalog, code), "implementation-template default")

        if bundle_key is not None:
            bundle = self._find_bundle(session, bundle_key, bundle_version)
            bundle_ref = f"{bundle.bundle_key}@{bundle.version}"
            for item in self._bundle_items(session, bundle.id):
                self._add_source(selected, sources, self._canonical_code(catalog, item.code), f"bundle {bundle_ref}")

        for code, state in explicit.items():
            canonical_code = self._canonical_code(catalog, code)
            if state[0] == "enabled":
                self._add_source(selected, sources, canonical_code, state[1] or "organization override")
            else:
                selected.discard(canonical_code)

        requested_enable = [self._canonical_code(catalog, code) for code in (enable_codes or [])]
        requested_disable = [self._canonical_code(catalog, code) for code in (disable_codes or [])]
        requested_clear = [self._canonical_code(catalog, code) for code in (clear_codes or [])]
        if set(requested_enable) & set(requested_disable):
            raise ModuleEntitlementValidationError("A module cannot be enabled and disabled in the same request.")
        if (set(requested_enable) | set(requested_disable)) & set(requested_clear):
            raise ModuleEntitlementValidationError("A module cannot be changed and cleared in the same request.")
        for code in requested_enable:
            self._add_source(selected, sources, code, "organization override")
        for code in requested_disable:
            selected.discard(code)
        for code in requested_clear:
            selected.discard(code)

        disabled = {
            self._canonical_code(catalog, code)
            for code, state in explicit.items()
            if state[0] == "disabled"
        } | set(requested_disable)
        dependency_conflicts = self._dependency_conflicts(catalog, selected, disabled)
        if dependency_conflicts:
            raise ModuleDependencyConflictError(dependency_conflicts)
        effective = self._close_dependencies(catalog, selected)
        self._validate_selection(catalog, effective)
        ordered = sorted(canonical, key=lambda code: (canonical[code].display_order, code))
        effective_codes = [code for code in ordered if code in effective]
        requested_codes = [code for code in ordered if code in selected]
        tenants = session.execute(select(Tenant).where(Tenant.organization_id == organization_id).order_by(Tenant.created_at.asc(), Tenant.id.asc())).scalars().all()
        items: list[ModuleEffectiveItem] = []
        for code in ordered:
            module = canonical[code]
            entitled = code in effective
            explicit_record = explicit.get(code)
            if explicit_record is None:
                alias = next((alias_code for alias_code, candidate in catalog.items() if candidate.alias_of == code), None)
                explicit_record = explicit.get(alias) if alias else None
            tenant_states = self._tenant_states(session, tenants, module.id) if entitled else []
            app_state, verification_state = self._aggregate_erp_state(tenant_states, entitled)
            explanation = list(sources.get(code, []))
            if entitled and code not in selected:
                explanation.append("required dependency")
            if not explanation:
                explanation.append("not selected by the safe default")
            requested = code in selected
            applied = app_state == "applied"
            verified = verification_state == "verified"
            hidden_reasons: list[str] = []
            if not entitled:
                hidden_reasons.append("Not included in the current entitlement.")
            if module.administrative_visibility != "public":
                hidden_reasons.append("This capability is restricted to operator administration.")
            if code in CHAMPION_PRESERVED_HIDDEN_CODES:
                hidden_reasons.append("Preserved capability; hidden from Champion navigation until a use case is approved.")
            if code in CHAMPION_HRMS_GATED_CODES and not verified:
                hidden_reasons.append("Hidden until HRMS is installed and the capability passes verification.")
            hidden = bool(hidden_reasons)
            attention_reasons: list[str] = []
            if entitled and not applied:
                if module.required_app == "hrms":
                    attention_reasons.append("HRMS is missing from the verified tenant installed-app readback. Install HRMS, rerun the readback, then retry verification.")
                else:
                    attention_reasons.append("ERP application is pending provisioning/readback evidence; retry after the tenant provisioning step completes." if app_state == "pending" else "ERP application failed; review the provider readback and retry.")
            if entitled and not verified:
                if any("role" in str(state.get("failure_reason") or "").lower() or "workspace" in str(state.get("failure_reason") or "").lower() for state in tenant_states):
                    attention_reasons.append("Required ERP roles or workspaces are missing from the verified readback. Configure them, rerun the readback, then retry verification.")
                elif verification_state == "pending":
                    attention_reasons.append("ERP verification is pending; rerun the tenant installed-app/module/role/workspace readback, then retry verification.")
                else:
                    attention_reasons.append("ERP verification failed; review the provider readback and retry.")
            if entitled and module.required_app and not tenant_states:
                attention_reasons.append(f"Required application `{module.required_app}` is not verified by the authorized staging readback.")
            attention_reasons.extend(str(state["failure_reason"]) for state in tenant_states if state.get("failure_reason"))
            needs_attention = bool(attention_reasons)
            states = [state for state, present in (("requested", requested), ("entitled", entitled), ("applied", applied), ("verified", verified), ("hidden", hidden), ("needs_attention", needs_attention)) if present]
            items.append(ModuleEffectiveItem(code=code, name=module.name, category=module.category, requested=requested, entitled=entitled, marketed=bool(module.is_marketed), explicit=explicit_record is not None, source=sorted(set(explanation)), explanation=sorted(set(explanation)), application_state=app_state, verification_state=verification_state, tenant_states=tenant_states, dependency_codes=list(module.dependency_codes_json or []), required_app=module.required_app, minimum_app_version=module.minimum_app_version, compatible_app_version=module.compatible_app_version, states=states, state_reasons=sorted(set(hidden_reasons + attention_reasons)), hidden=hidden, needs_attention=needs_attention))
        return ModuleEffectiveRead(organization_id=organization_id, requested_codes=requested_codes, effective_codes=effective_codes, items=items, warnings=warnings, generated_at=datetime.now(timezone.utc))

    def preview(self, session: Session, payload: ModuleChangeRequest, *, actor: Optional[SaaSUser] = None) -> ModulePreviewRead:
        current = self.resolve(session, payload.organization_id)
        proposed = self.resolve(session, payload.organization_id, enable_codes=payload.enable_codes, disable_codes=payload.disable_codes, clear_codes=payload.clear_codes, bundle_key=payload.bundle_key, bundle_version=payload.bundle_version)
        current_set, proposed_set = set(current.effective_codes), set(proposed.effective_codes)
        catalog = self._catalog(session)
        direct_enable = {self._canonical_code(catalog, code) for code in payload.enable_codes}
        if payload.bundle_key:
            bundle = self._find_bundle(session, payload.bundle_key, payload.bundle_version)
            direct_enable.update(self._canonical_code(catalog, item.code) for item in self._bundle_items(session, bundle.id))
        identity = {
            "organization_id": payload.organization_id,
            "actor_user_id": actor.id if actor else None,
            "enable_codes": sorted(set(payload.enable_codes)),
            "disable_codes": sorted(set(payload.disable_codes)),
            "clear_codes": sorted(set(payload.clear_codes)),
            "bundle_key": payload.bundle_key,
            "bundle_version": payload.bundle_version,
            "catalog_revision": self._catalog_revision(session),
            "current_entitlement_revision": self._entitlement_revision(session, payload.organization_id, current),
        }
        preview_hash = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        entitled_modules = [module for module in catalog.values() if module.code in proposed.effective_codes]
        application_resolution = calculate_required_applications(entitled_modules)
        # Keep the historical field scoped to module metadata.  Platform apps
        # are exposed separately so a preview cannot silently conflate the
        # Frappe baseline with an app newly required by a selected module.
        required_applications = sorted({item.required_app for item in proposed.items if item.entitled and item.required_app})
        bundle_version = None
        if payload.bundle_key:
            bundle_version = self._find_bundle(session, payload.bundle_key, payload.bundle_version).version
        return ModulePreviewRead(organization_id=payload.organization_id, requested_enable_codes=sorted(set(payload.enable_codes)), requested_disable_codes=sorted(set(payload.disable_codes)), requested_clear_codes=sorted(set(payload.clear_codes)), dependency_additions=sorted((proposed_set - current_set) - direct_enable), dependency_removals=sorted(current_set - proposed_set), conflicts=[], effective=proposed, warnings=sorted(set(current.warnings + proposed.warnings)), preview_hash=preview_hash, is_current=True, bundle_key=payload.bundle_key, bundle_version=bundle_version, required_applications=required_applications, platform_required_applications=list(application_resolution.platform_applications), affected_tenants=self._tenant_targets(session, payload.organization_id))

    def apply(self, session: Session, actor: SaaSUser, payload: ModuleChangeRequest, *, operation: str = "apply", source_type_override: Optional[str] = None, source_ref_override: Optional[str] = None) -> ModuleChangeResult:
        request_fingerprint = self._request_fingerprint(payload)
        idempotency_key = payload.idempotency_key or f"auto-{request_fingerprint}"
        if not payload.preview_hash:
            raise ModuleEntitlementValidationError("A server-issued preview_hash is required before apply.")
        prior = session.execute(select(ModuleEntitlementRequest).where(ModuleEntitlementRequest.organization_id == payload.organization_id, ModuleEntitlementRequest.idempotency_key == idempotency_key)).scalar_one_or_none()
        if prior is not None:
            if prior.request_hash != request_fingerprint:
                raise ModuleEntitlementValidationError("The idempotency key was already used for a different module request.")
            result = ModuleChangeResult.model_validate(prior.response_json)
            result.replayed = True
            return result
        preview = self.preview(session, payload, actor=actor)
        if payload.preview_hash != preview.preview_hash:
            raise ModuleEntitlementValidationError("The preview is stale. Generate a new preview before applying.")

        before = self.resolve(session, payload.organization_id)
        previous_requested = self._requested_state_snapshot(session, payload.organization_id)
        previous_bundle_key, previous_bundle_version = self._current_bundle_attribution(session, payload.organization_id)
        catalog = self._catalog(session)
        disable_set = {self._canonical_code(catalog, code) for code in payload.disable_codes}
        clear_set = {self._canonical_code(catalog, code) for code in payload.clear_codes}
        changed_codes = {self._canonical_code(catalog, code) for code in payload.enable_codes + payload.disable_codes + payload.clear_codes}
        source_type, source_ref = source_type_override or "organization", source_ref_override
        if payload.bundle_key:
            bundle = self._find_bundle(session, payload.bundle_key, payload.bundle_version)
            source_type, source_ref = source_type_override or "bundle", source_ref_override or f"{bundle.bundle_key}@{bundle.version}"
            changed_codes.update(self._canonical_code(catalog, item.code) for item in self._bundle_items(session, bundle.id))
        now = datetime.now(timezone.utc)
        for code in sorted(changed_codes):
            module = catalog[code]
            if code in clear_set:
                record = self._find_org_module(session, payload.organization_id, module.id)
                if record is not None:
                    session.delete(record)
                continue
            requested_state = "disabled" if code in disable_set else "enabled"
            record = self._find_org_module(session, payload.organization_id, module.id)
            if record is None:
                record = OrganizationModule(organization_id=payload.organization_id, module_id=module.id)
                session.add(record)
            record.status = requested_state
            record.explicit_state = requested_state
            record.requested_state = requested_state
            record.entitled_state = "entitled" if requested_state == "enabled" else "not_entitled"
            record.source_type = source_type
            record.source_ref = source_ref
            record.reason = payload.reason
            record.last_idempotency_key = idempotency_key
            record.requested_at = now
            if requested_state == "enabled":
                record.enabled_by, record.enabled_at = actor.id, now
            else:
                record.disabled_at = now
        session.flush()
        after = self.resolve(session, payload.organization_id)
        tenant_ids = [tenant.id for tenant in session.execute(select(Tenant).where(Tenant.organization_id == payload.organization_id).order_by(Tenant.created_at.asc(), Tenant.id.asc())).scalars().all()]
        new_bundle_version = self._find_bundle(session, payload.bundle_key, payload.bundle_version).version if payload.bundle_key else None
        audit = ModuleEntitlementAudit(actor_user_id=actor.id, organization_id=payload.organization_id, tenant_id=tenant_ids[0] if len(tenant_ids) == 1 else None, tenant_ids_json=tenant_ids, operation=operation, previous_requested_json=previous_requested, new_requested_json=self._requested_state_snapshot(session, payload.organization_id), previous_effective_json=self._effective_snapshot(before), new_effective_json=self._effective_snapshot(after), source_type=source_type, source_ref=source_ref, previous_bundle_key=previous_bundle_key, previous_bundle_version=previous_bundle_version, new_bundle_key=payload.bundle_key, new_bundle_version=new_bundle_version, reason=payload.reason, idempotency_key=idempotency_key, result="applied")
        session.add(audit)
        session.flush()
        result = ModuleChangeResult(operation=operation, audit_id=audit.id, effective=after)
        session.add(ModuleEntitlementRequest(organization_id=payload.organization_id, actor_user_id=actor.id, idempotency_key=idempotency_key, request_hash=request_fingerprint, operation=operation, response_json=result.model_dump(mode="json"), status="applied"))
        try:
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            raise ModuleEntitlementValidationError("The module change could not be committed safely; retry with a new idempotency key.") from exc
        return result

    def reverse(self, session: Session, actor: SaaSUser, payload: ModuleReversalRequest) -> ModuleChangeResult:
        audit = session.get(ModuleEntitlementAudit, payload.audit_id)
        if audit is None or audit.organization_id != payload.organization_id:
            raise ModuleEntitlementNotFound("Module audit entry not found.")
        previous = audit.previous_requested_json
        current = self._requested_state_snapshot(session, payload.organization_id)
        desired_enabled, desired_disabled = set(previous.get("enabled", [])), set(previous.get("disabled", []))
        current_enabled, current_disabled = set(current.get("enabled", [])), set(current.get("disabled", []))
        desired_codes = desired_enabled | desired_disabled
        current_codes = current_enabled | current_disabled
        request = ModuleChangeRequest(organization_id=payload.organization_id, enable_codes=sorted(desired_enabled - current_enabled) + sorted(current_disabled & desired_enabled), disable_codes=sorted(desired_disabled - current_disabled) + sorted(current_enabled & desired_disabled), clear_codes=sorted(current_codes - desired_codes), reason=payload.reason or f"Reversal of module audit {audit.id}", preview_hash=payload.preview_hash, idempotency_key=payload.idempotency_key)
        if request.preview_hash is None:
            # Reversal is itself an apply operation.  Generate a server-bound
            # preview at the point of reversal so it cannot bypass the same
            # stale-state guard as a normal apply.
            request.preview_hash = self.preview(session, request, actor=actor).preview_hash
        return self.apply(session, actor, request, operation="reverse", source_type_override="reversal", source_ref_override=audit.id)

    def list_audit(self, session: Session, organization_id: str, limit: int = 100) -> list[ModuleAuditRead]:
        rows = session.execute(select(ModuleEntitlementAudit).where(ModuleEntitlementAudit.organization_id == organization_id).order_by(ModuleEntitlementAudit.created_at.desc()).limit(max(1, min(limit, 500)))).scalars().all()
        return [ModuleAuditRead(id=row.id, created_at=row.created_at, actor_user_id=row.actor_user_id, organization_id=row.organization_id, tenant_id=row.tenant_id, tenant_ids=list(row.tenant_ids_json or []), operation=row.operation, previous_requested=row.previous_requested_json, new_requested=row.new_requested_json, previous_effective=row.previous_effective_json, new_effective=row.new_effective_json, source_type=row.source_type, source_ref=row.source_ref, previous_bundle_key=row.previous_bundle_key, previous_bundle_version=row.previous_bundle_version, new_bundle_key=row.new_bundle_key, new_bundle_version=row.new_bundle_version, reason=row.reason, idempotency_key=row.idempotency_key, result=row.result) for row in rows]

    def record_trusted_application_status(self, session: Session, *, tenant_id: str, module_code: str, application_state: str, verification_state: str = "pending", evidence_ref: Optional[str] = None, failure_reason: Optional[str] = None) -> ModuleApplicationStatus:
        module = session.execute(select(Module).where(Module.code == module_code)).scalar_one_or_none()
        if module is None:
            raise ModuleEntitlementNotFound("Module not found.")
        status = session.execute(select(ModuleApplicationStatus).where(ModuleApplicationStatus.tenant_id == tenant_id, ModuleApplicationStatus.module_id == module.id)).scalar_one_or_none()
        if status is None:
            status = ModuleApplicationStatus(tenant_id=tenant_id, module_id=module.id)
            session.add(status)
        status.application_state, status.verification_state = application_state, verification_state
        status.evidence_ref, status.failure_reason = evidence_ref, failure_reason
        status.last_checked_at = datetime.now(timezone.utc)
        if application_state == "applied": status.applied_at = status.applied_at or datetime.now(timezone.utc)
        if verification_state == "verified": status.verified_at = status.verified_at or datetime.now(timezone.utc)
        session.commit()
        session.refresh(status)
        return status

    def _catalog(self, session: Session) -> dict[str, Module]:
        return {module.code: module for module in session.execute(select(Module).order_by(Module.display_order.asc(), Module.code.asc())).scalars().all()}

    def _catalog_revision(self, session: Session) -> str:
        catalog = self._catalog(session)
        payload = [
            {
                "code": code,
                "name": module.name,
                "description": module.description,
                "category": module.category,
                "is_active": module.is_active,
                "is_marketed": module.is_marketed,
                "public_description": module.public_description,
                "internal_description": module.internal_description,
                "display_order": module.display_order,
                "dependencies": sorted(module.dependency_codes_json or []),
                "incompatibilities": sorted(module.incompatibility_codes_json or []),
                "required_app": module.required_app,
                "minimum_app_version": module.minimum_app_version,
                "compatible_app_version": module.compatible_app_version,
                "default_roles": sorted(module.default_roles_json or []),
                "default_workspaces": sorted(module.default_workspaces_json or []),
                "configuration_schema": module.configuration_schema_json or {},
                "administrative_visibility": module.administrative_visibility,
                "alias_of": module.alias_of,
                "deprecated_at": module.deprecated_at.isoformat() if module.deprecated_at else None,
                "metadata_version": module.metadata_version,
            }
            for code, module in catalog.items()
        ]
        bundles = session.execute(select(ModuleBundle).order_by(ModuleBundle.bundle_key.asc(), ModuleBundle.version.asc())).scalars().all()
        for bundle in bundles:
            payload.append({
                "bundle_key": bundle.bundle_key,
                "version": bundle.version,
                "name": bundle.name,
                "description": bundle.description,
                "is_active": bundle.is_active,
                "source": bundle.source,
                "items": [{"code": item.code, "sort_order": item.sort_order} for item in self._bundle_items(session, bundle.id)],
            })
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def _entitlement_revision(self, session: Session, organization_id: str, current: ModuleEffectiveRead) -> str:
        rows = session.execute(
            select(OrganizationModule).where(OrganizationModule.organization_id == organization_id).order_by(OrganizationModule.module_id.asc())
        ).scalars().all()
        return hashlib.sha256(
            json.dumps(
                {
                    "requested": self._requested_state_snapshot(session, organization_id),
                    "effective": current.effective_codes,
                    "rows": [
                        {
                            "id": row.id,
                            "module_id": row.module_id,
                            "status": row.status,
                            "explicit_state": row.explicit_state,
                            "requested_state": row.requested_state,
                            "entitled_state": row.entitled_state,
                            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                        }
                        for row in rows
                    ],
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()

    def _canonical_code(self, catalog: dict[str, Module], code: str) -> str:
        normalized = code.strip().lower()
        module = catalog.get(normalized)
        if module is None: raise ModuleEntitlementValidationError(f"Unknown module code: {normalized}.")
        seen: set[str] = set()
        while module.alias_of:
            if module.code in seen or module.alias_of not in catalog: raise ModuleEntitlementValidationError(f"Module alias mapping is invalid for {normalized}.")
            seen.add(module.code)
            module = catalog[module.alias_of]
        return module.code

    def _explicit_states(self, session: Session, organization_id: str) -> dict[str, tuple[str, Optional[str]]]:
        rows = session.execute(select(OrganizationModule, Module).join(Module, Module.id == OrganizationModule.module_id).where(OrganizationModule.organization_id == organization_id)).all()
        return {module.code: (row.explicit_state or row.status or "enabled", row.source_ref or row.source_type) for row, module in rows}

    def _inherited_codes(self, session: Session, organization_id: str) -> tuple[list[str], list[str]]:
        from app.models.domain import Plan
        subscription = session.execute(select(Subscription).where(Subscription.organization_id == organization_id).order_by(Subscription.created_at.desc())).scalars().first()
        plan_codes: list[str] = []
        if subscription:
            plan = session.get(Plan, subscription.plan_id)
            if plan and plan.is_active and subscription.status not in {"cancelled", "incomplete", "past_due"}: plan_codes = list(plan.default_modules_json or [])
        project = session.execute(select(ImplementationProject).where(ImplementationProject.organization_id == organization_id, ImplementationProject.template_id.is_not(None)).order_by(ImplementationProject.created_at.desc())).scalars().first()
        template_codes: list[str] = []
        if project and project.template_id:
            template = session.get(ImplementationTemplate, project.template_id)
            if template: template_codes = list(template.default_modules_json or [])
        return plan_codes, template_codes

    def _close_dependencies(self, catalog: dict[str, Module], selected: set[str]) -> set[str]:
        canonical = {code: module for code, module in catalog.items() if module.alias_of is None}
        result: set[str] = set(); visiting: set[str] = set()
        def visit(code: str) -> None:
            if code in result: return
            if code in visiting: raise ModuleEntitlementValidationError(f"Dependency cycle detected at module {code}.")
            module = canonical.get(code)
            if module is None: raise ModuleEntitlementValidationError(f"Required dependency {code} is missing from the catalog.")
            if not module.is_active: raise ModuleEntitlementValidationError(f"Module {code} is inactive and cannot be entitled.")
            visiting.add(code)
            for dependency in module.dependency_codes_json or []: visit(self._canonical_code(catalog, dependency))
            visiting.remove(code); result.add(code)
        for code in sorted(selected): visit(self._canonical_code(catalog, code))
        return result

    def _dependency_conflicts(self, catalog: dict[str, Module], selected: set[str], disabled: set[str]) -> list[tuple[str, str]]:
        canonical = {code: module for code, module in catalog.items() if module.alias_of is None}
        conflicts: list[tuple[str, str]] = []
        for root in sorted(selected):
            seen: set[str] = set()
            pending = [root]
            while pending:
                code = pending.pop()
                if code in seen:
                    continue
                seen.add(code)
                module = canonical.get(code)
                if module is None:
                    continue
                for dependency in module.dependency_codes_json or []:
                    dependency_code = self._canonical_code(catalog, dependency)
                    if dependency_code in disabled:
                        conflicts.append((root, dependency_code))
                    pending.append(dependency_code)
        return sorted(set(conflicts))

    def _validate_selection(self, catalog: dict[str, Module], selected: set[str]) -> None:
        for code in sorted(selected):
            module = catalog[code]
            for incompatible in module.incompatibility_codes_json or []:
                other = self._canonical_code(catalog, incompatible)
                if other in selected: raise ModuleEntitlementValidationError(f"Modules {code} and {other} are incompatible.")

    def _find_bundle(self, session: Session, bundle_key: str, version: Optional[int]) -> ModuleBundle:
        statement = select(ModuleBundle).where(ModuleBundle.bundle_key == bundle_key, ModuleBundle.is_active.is_(True))
        if version is not None: statement = statement.where(ModuleBundle.version == version)
        else: statement = statement.order_by(ModuleBundle.version.desc())
        bundle = session.execute(statement).scalars().first()
        if bundle is None: raise ModuleEntitlementNotFound("Module bundle not found.")
        return bundle

    def _bundle_items(self, session: Session, bundle_id: str) -> list[ModuleBundleItemRead]:
        rows = session.execute(select(ModuleBundleItem, Module).join(Module, Module.id == ModuleBundleItem.module_id).where(ModuleBundleItem.bundle_id == bundle_id).order_by(ModuleBundleItem.sort_order.asc(), Module.code.asc())).all()
        return [ModuleBundleItemRead(code=module.code, name=module.name, sort_order=item.sort_order, dependency_codes=list(module.dependency_codes_json or []), required_app=module.required_app, minimum_app_version=module.minimum_app_version, compatible_app_version=module.compatible_app_version) for item, module in rows]

    def _bundle_read(self, session: Session, bundle: ModuleBundle) -> ModuleBundleRead:
        modules = self._bundle_items(session, bundle.id)
        prior = session.execute(select(ModuleBundle).where(ModuleBundle.bundle_key == bundle.bundle_key, ModuleBundle.version < bundle.version).order_by(ModuleBundle.version.desc())).scalars().first()
        prior_codes = {item.code for item in self._bundle_items(session, prior.id)} if prior else set()
        current_codes = {item.code for item in modules}
        return ModuleBundleRead(id=bundle.id, bundle_key=bundle.bundle_key, version=bundle.version, name=bundle.name, description=bundle.description, source=bundle.source, modules=modules, supersedes_version=prior.version if prior else None, added_module_codes=sorted(current_codes - prior_codes), removed_module_codes=sorted(prior_codes - current_codes))

    @staticmethod
    def _add_source(selected: set[str], sources: dict[str, list[str]], code: str, source: str) -> None:
        selected.add(code); sources.setdefault(code, []).append(source)

    @staticmethod
    def _find_org_module(session: Session, organization_id: str, module_id: str) -> Optional[OrganizationModule]:
        return session.execute(select(OrganizationModule).where(OrganizationModule.organization_id == organization_id, OrganizationModule.module_id == module_id)).scalar_one_or_none()

    def _tenant_states(self, session: Session, tenants: list[Tenant], module_id: str) -> list[dict[str, object]]:
        return [{"tenant_id": tenant.id, "application_state": (row.application_state if row else "pending"), "verification_state": (row.verification_state if row else "pending"), "evidence_ref": (row.evidence_ref if row else None), "failure_reason": (row.failure_reason if row else None)} for tenant in tenants for row in [session.execute(select(ModuleApplicationStatus).where(ModuleApplicationStatus.tenant_id == tenant.id, ModuleApplicationStatus.module_id == module_id)).scalar_one_or_none()]]

    @staticmethod
    def _tenant_targets(session: Session, organization_id: str) -> list[dict[str, object]]:
        tenants = session.execute(select(Tenant).where(Tenant.organization_id == organization_id).order_by(Tenant.created_at.asc(), Tenant.id.asc())).scalars().all()
        return [{"tenant_id": tenant.id, "tenant_slug": tenant.tenant_slug, "environment": tenant.environment, "status": tenant.status, "provisioning_status": tenant.provisioning_status} for tenant in tenants]

    @staticmethod
    def _parse_bundle_ref(source_ref: Optional[str]) -> tuple[Optional[str], Optional[int]]:
        if not source_ref or "@" not in source_ref:
            return None, None
        key, raw_version = source_ref.rsplit("@", 1)
        try:
            return key, int(raw_version)
        except ValueError:
            return None, None

    def _current_bundle_attribution(self, session: Session, organization_id: str) -> tuple[Optional[str], Optional[int]]:
        refs = session.execute(select(OrganizationModule.source_ref).where(OrganizationModule.organization_id == organization_id, OrganizationModule.source_type == "bundle", OrganizationModule.source_ref.is_not(None))).scalars().all()
        parsed = {self._parse_bundle_ref(ref) for ref in refs}
        parsed.discard((None, None))
        return next(iter(parsed)) if len(parsed) == 1 else (None, None)

    @staticmethod
    def _aggregate_erp_state(states: list[dict[str, object]], entitled: bool) -> tuple[str, str]:
        if not entitled: return "not_applicable", "pending"
        if not states: return "pending", "pending"
        app_values = [str(state["application_state"]) for state in states]; verify_values = [str(state["verification_state"]) for state in states]
        app = "failed" if "failed" in app_values else ("applied" if all(value == "applied" for value in app_values) else "pending")
        verified = "failed" if "failed" in verify_values else ("verified" if all(value == "verified" for value in verify_values) else "pending")
        return app, verified

    @staticmethod
    def _requested_state_snapshot(session: Session, organization_id: str) -> dict[str, object]:
        rows = session.execute(select(OrganizationModule, Module).join(Module, Module.id == OrganizationModule.module_id).where(OrganizationModule.organization_id == organization_id)).all()
        return {"enabled": sorted(module.code for row, module in rows if (row.explicit_state or row.status) == "enabled"), "disabled": sorted(module.code for row, module in rows if (row.explicit_state or row.status) == "disabled")}

    @staticmethod
    def _effective_snapshot(effective: ModuleEffectiveRead) -> dict[str, object]:
        return {"codes": effective.effective_codes, "items": [item.model_dump(mode="json") for item in effective.items]}

    @staticmethod
    def _request_fingerprint(payload: ModuleChangeRequest) -> str:
        identity = {"organization_id": payload.organization_id, "enable_codes": sorted(set(payload.enable_codes)), "disable_codes": sorted(set(payload.disable_codes)), "clear_codes": sorted(set(payload.clear_codes)), "bundle_key": payload.bundle_key, "bundle_version": payload.bundle_version, "reason": payload.reason}
        return hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


module_entitlement_service = ModuleEntitlementService()
