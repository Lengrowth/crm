# Phase 10 — White-label and Domain Management

Status: Completed

Summary

This phase introduces per-tenant white-label and domain metadata, plus manual activation fields and an API for operations teams to manage DNS/SSL metadata. The implementation is metadata-only (no external DNS or SSL calls). It provides hooks for future automation (workers/jobs) but keeps the API and service logic focused on recording operator-driven state.

Key additions

- Model: `app.models.domain.DomainMapping` extended with fields:
  - `is_active` (bool) — whether the domain is active for routing.
  - `manual_activation_required` (bool) — whether tenant requires manual enable.
  - `dns_verified_at` (datetime) — when DNS was marked verified by ops.
  - `manual_activation_by` (saas_users.id) — who performed manual activation.
  - `manual_activation_at` (datetime) — when manual activation happened.
  - `notes_json` (JSON) — structured notes (used to append manual activation audit entries).

- Alembic migration: `backend/alembic/versions/20260527_0006_domain_management.py` adds the new columns and FK for `manual_activation_by`.

- Schemas: `app.schemas.domain_management` exposes:
  - `DomainOut` — read model for the API.
  - `DomainCreateRequest` — payload for create.
  - `DomainUpdateRequest` — partial fields for update.
  - `ManualActivationRequest` — payload to toggle manual activation.

- Service: `app.services.domain_service.DomainService` implements:
  - create_domain, update_domain
  - list_domains
  - mark_dns_verified
  - set_ssl_status
  - manual_activate

  Domain validation is intentionally lightweight (string checks only). No DNS or SSL network I/O is performed in this phase.

- API router: `app.api.domain_management` mounted at the main API router. Endpoints:
  - GET /tenants/{tenant_id}/domains
  - POST /tenants/{tenant_id}/domains
  - PATCH /tenants/{tenant_id}/domains/{domain_id}
  - POST /tenants/{tenant_id}/domains/{domain_id}/manual_activate

- Tests:
  - `backend/tests/test_domain_service.py` — unit tests for validation and manual activation.
  - `backend/tests/test_domain_api.py` — API test using TestClient with dependency overrides and an in-memory SQLite file.

Operational runbook (manual DNS/SSL)

1) Adding a custom domain
- Operator creates a domain record via the API (or internal UI) with the tenant id and domain (e.g., `example.customer.com`).
- System will store `dns_target` which indicates the provider target (CNAME / ALIAS value).
- The domain's `status` initially is `pending_dns` and `dns_verified_at` is null.

2) Verifying DNS
- After the customer has created the DNS record, the operator marks DNS as verified using an operational UI which calls `mark_dns_verified` (future worker) or by setting `dns_verified_at` via the API / service.
- Setting `dns_verified_at` does not automatically activate SSL or routing. It only records that DNS is present.

3) SSL provisioning
- SSL provisioning should be performed by an offline job/worker. That worker will update `ssl_status` (e.g., `pending`, `issued`, `failed`) and may set `verified_at` when certificate is in place.
- This phase does not perform certificate issuance.

4) Manual activation
- If a tenant requires manual activation (`manual_activation_required` = true), operators can toggle activation using the manual activate endpoint. The API records `manual_activation_by` and `manual_activation_at` and appends a structured entry to `notes_json.manual_activations` so there's an audit trail.

Field definitions (summary)

- tenant_id: FK to tenants table.
- domain: domain name string (unique).
- type: `system_subdomain` | `custom` etc.
- status: high-level state for domain (e.g., `pending_dns`, `active`, `disabled`).
- dns_target: provider gateway target (CNAME/ALIAS value) — informational.
- is_active: whether the domain is active for routing.
- manual_activation_required: mark if tenant should be manually activated by ops.
- dns_verified_at: timestamp when DNS was marked verified.
- ssl_status: `unknown` | `pending` | `issued` | `failed`.
- verified_at: when the domain/cert was verified as usable.
- manual_activation_by / manual_activation_at: operator who toggled manual activation and when.
- notes_json: free-form JSON for operator notes and structured entries (manual_activations list).

Follow-ups

- Phase 11 should introduce automation: a worker that performs DNS checks and triggers SSL issuance (e.g., via ACME/Let's Encrypt or a provider API) and transitions `ssl_status` automatically.
- UI work: add simple operations UI pages for listing tenant domains, showing verification status, and manual activation toggles.

Security

- No secrets are stored in these fields.
- Audit logs for activations are recorded in `notes_json`; consider adding a dedicated audit table in a later phase for immutable audit records.

Testing notes

- Tests use SQLite files and clear dependency overrides. They do not perform network queries.
- Tests exercise validation, create, update, and manual activation behaviors.

