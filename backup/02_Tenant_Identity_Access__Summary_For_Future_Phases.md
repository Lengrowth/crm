# Summary for Future Phases

## Final Decisions Made

- `Tenant` is the top-level SaaS isolation boundary.
- `Company` is the customer organization inside a Tenant.
- `Company` must not be confused with CRM `Account`.
- Company-level access through `UserMembership` is the default MVP permission boundary.
- `User` is the canonical human identity.
- A User can belong to one or more Companies through `UserMembership`.
- Roles and company access are assigned through UserMembership, not as a single global user role.
- Super Admin and Company Admin are separate concepts and must not be merged.
- Drivers, technicians, warehouse operators, dispatchers, sales reps, managers, analysts, and read-only users are all Users with memberships and roles when they authenticate.
- Module access requires both Company module enablement and user permission.
- RBAC is the baseline authorization model.
- Policy-based authorization, including possible Cerbos adoption, must remain future-compatible.
- Record-level access is future-capable but not mandatory for every MVP feature.
- Backend permission checks are mandatory; frontend hiding is not sufficient.
- Reports, exports, search, imports, integrations, and offline sync must respect tenant/company/module/permission rules.
- Offline queued actions must be revalidated on sync.
- MongoDB `_id` must not be exposed as the public API identifier.

## Entities Introduced

| Entity | Purpose | Scope | Future Phase Rule |
| --- | --- | --- | --- |
| Tenant | Top-level SaaS isolation boundary. | Platform / Tenant | Every tenant-owned record must include `tenant_id`. |
| Company | Customer organization inside Tenant. | Tenant / Company | Company-scoped records must include `tenant_id` and `company_id`. |
| User | Human platform identity. | Tenant/global identity depending final decision | No module may create its own user system. |
| UserMembership | Bridge between User and Company access. | Tenant + Company | All company access, roles, team links, branch scope, and status use this entity. |
| Role | Named permission grouping. | Tenant or Company | Later phases add permission keys; do not change role concept. |
| Permission | Stable action key. | Platform registry / scoped use | Use `module.resource.action` naming. |
| Policy | Conditional access rule beyond static roles. | Tenant / Company / future resource | Future-capable for Cerbos/policy engine. |
| Session | Authenticated device/browser/app context. | User + Tenant + current Company | Must be revocable and audit-relevant. |
| Invitation | User onboarding into Company. | Tenant + Company | Acceptance creates/updates UserMembership. |
| ModuleAccess / Company enabled_modules | Company module enablement. | Company | User also needs permission. |
| AuditLog identity/access usage | Append-only record of access/admin/security actions. | Tenant + Company where applicable | Phase 15 expands audit architecture. |

## Fields Introduced

### Tenant

`id`, `name`, `slug`, `status`, `settings`, `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, `deleted_by`, `metadata`.

### Company

`id`, `tenant_id`, `name`, `legal_name`, `display_name`, `slug`, `status`, `enabled_modules`, `settings`, `external_refs`, `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, `deleted_by`, `metadata`.

### User

`id`, `tenant_id` if tenant-scoped, `email`, `email_normalized`, `name`, `first_name`, `last_name`, `phone`, `avatar_url`, `status`, `last_login_at`, `mfa_enabled`, `locale`, `timezone`, `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, `deleted_by`, `metadata`.

### UserMembership

`id`, `tenant_id`, `company_id`, `user_id`, `role_ids`, `team_ids`, `department_id`, `branch_ids`, `status`, `is_primary`, `joined_at`, `invited_by`, `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, `deleted_by`, `metadata`.

### Session

`id`, `user_id`, `tenant_id`, `current_company_id`, `status`, `ip_address`, `user_agent`, `created_at`, `last_seen_at`, `expires_at`, `revoked_at`, `revoked_by`, `metadata`.

### Invitation

`id`, `tenant_id`, `company_id`, `email`, `role_ids`, `team_ids`, `status`, `token_hash`, `expires_at`, `accepted_at`, `accepted_by_user_id`, `revoked_at`, `revoked_by`, `invited_by`, `created_at`, `updated_at`, `metadata`.

## APIs Introduced

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/me`
- `GET /api/v1/me/memberships`
- `PUT /api/v1/me/current-company`
- `GET /api/v1/companies`
- `POST /api/v1/admin/users/invitations`
- `POST /api/v1/invitations/{invitation_id}/accept`
- `POST /api/v1/admin/users/invitations/{invitation_id}/revoke`
- `GET /api/v1/admin/users`
- `GET /api/v1/admin/users/{user_id}`
- `PATCH /api/v1/admin/memberships/{membership_id}`
- `POST /api/v1/admin/memberships/{membership_id}/deactivate`
- `POST /api/v1/admin/memberships/{membership_id}/reactivate`
- `GET /api/v1/admin/roles`
- `POST /api/v1/admin/roles` if custom roles are enabled.
- `PATCH /api/v1/admin/roles/{role_id}` if custom roles are enabled.
- `GET /api/v1/admin/permissions`
- `GET /api/v1/admin/module-access`
- `PATCH /api/v1/admin/module-access`
- `GET /api/v1/admin/audit/identity-access`
- `PATCH /api/v1/me/profile`
- `GET /api/v1/me/sessions`
- `POST /api/v1/me/sessions/{session_id}/revoke`

## Permissions Introduced

| Permission Key | Purpose |
| --- | --- |
| `profile.self.view` | View own profile. |
| `profile.self.update` | Update own permitted profile fields. |
| `sessions.self.view` | View own sessions. |
| `sessions.self.manage` | Revoke own sessions. |
| `company.switch` | Switch current company among active memberships. |
| `admin.users.view` | View company users and memberships. |
| `admin.users.invite` | Invite users to company. |
| `admin.users.manage` | Manage/deactivate/reactivate memberships. |
| `admin.roles.view` | View roles. |
| `admin.roles.assign` | Assign/remove roles. |
| `admin.roles.manage` | Manage custom roles if enabled. |
| `admin.permissions.view` | View permission registry. |
| `admin.company_settings.view` | View company settings. |
| `admin.company_settings.manage` | Manage company settings. |
| `admin.modules.view` | View enabled modules. |
| `admin.modules.manage` | Enable/disable company modules. |
| `admin.audit.view` | View identity/access audit logs. |
| `platform.tenants.view` | Super Admin tenant visibility. |
| `platform.tenants.manage` | Super Admin tenant management. |
| `platform.support_access` | Controlled support/break-glass access. |
| `admin.company_users.export` | Export company user/admin data where allowed. |
| `admin.security.review` | Review security/session/auth events. |

## UX Patterns Introduced

- Login, logout, password reset, and email verification flows.
- MFA setup placeholder/future-ready security screen.
- Current user profile screen.
- Company switcher shown when the user has multiple active memberships.
- Company settings screen.
- Company-scoped user management list.
- Invite user modal/page.
- User detail page with membership, roles, sessions, and audit context.
- Role assignment UI with permission preview.
- Role/permission overview.
- Module access settings.
- Session/device management.
- Identity/access audit log view for admins.

## Reports or Dashboards Introduced

- User count by company.
- Active users.
- Invited users.
- Pending invitations.
- Role distribution.
- Last login activity.
- Module access adoption.
- Identity/access audit reports.
- Failed login trends.
- Admin activity reports.

Full reporting is deferred to Phase 12, but Phase 02 must capture the data required for these reports.

## Notifications Introduced

- Invitation sent.
- Invitation accepted.
- Invitation revoked.
- Password reset requested.
- Password changed.
- MFA enabled/disabled if used.
- New login from unknown device.
- Membership deactivated.
- Role changed.
- Company Admin added.
- Super Admin support/action alert where appropriate.

Email is required for invitations and password flows. In-app is optional depending on recipient state. SMS is future-capable only.

## Audit Events Introduced

- `login_success`
- `login_failure`
- `logout`
- `password_reset_requested`
- `password_changed`
- `email_verified`
- `mfa_enabled`
- `mfa_disabled`
- `user_invited`
- `invitation_accepted`
- `invitation_revoked`
- `membership_created`
- `membership_updated`
- `membership_deactivated`
- `membership_reactivated`
- `role_assigned`
- `role_removed`
- `role_created`
- `role_updated`
- `permission_changed`
- `company_module_enabled`
- `company_module_disabled`
- `company_settings_changed`
- `super_admin_accessed_tenant`
- `super_admin_accessed_company`
- `session_revoked`
- `company_switched`
- `user_profile_updated`
- `tenant_suspended`
- `company_suspended`

## Integrations Introduced

- No provider-specific integration is implemented in Phase 02.
- Future API keys, webhooks, sync jobs, QuickBooks connections, and integration service actors must be tenant/company scoped.
- Integration jobs must run with explicit system actor identity and company context.
- External references must never bypass identity/access checks.

## Dependencies Created

- Phase 03 depends on Phase 02 for audit, files, notifications, settings, and platform context.
- Phase 04 depends on company-scoped CRM access and the distinction between Company and Account.
- Phase 05 depends on user, role, and activity ownership.
- Phase 06 depends on user identity and team assignment foundations.
- Phase 07 depends on field-user roles and mobile permission behavior.
- Phase 08 depends on warehouse/depot user roles and future location-scoped permissions.
- Phase 09 depends on dispatcher/driver roles.
- Phase 10 depends on driver/device access rules.
- Phase 11 depends on service technician roles.
- Phase 12 depends on reporting visibility rules.
- Phase 13 depends on company-scoped integration context.
- Phase 14 depends on offline permission revalidation.
- Phase 15 depends on identity/access audit events.
- Phase 17 depends on API key and integration actor scoping.
- Phase 18 depends on permission-aware search and filters.

## Constraints Future Phases Must Respect

- Do not create duplicate user, role, membership, permission, driver-user, technician-user, or warehouse-user systems.
- Do not confuse Company with CRM Account.
- Do not bypass Tenant and Company scope in APIs, UI, reports, exports, search, integrations, imports, or background jobs.
- Do not expose MongoDB `_id` as the public API identifier.
- Do not grant module access through module enablement alone; user permission is also required.
- Do not treat frontend hiding as security enforcement.
- Do not allow Company Admin to grant or become Super Admin.
- Do not implement branch, depot, warehouse, team, or record-level restrictions without preserving company-level access as the parent boundary.
- Do not let offline-created or offline-queued actions bypass server-side revalidation.
- Do not let integrations or external IDs bypass access-control rules.
- Do not implement reports or exports that reveal records the user cannot access in the source module.
- Do not silently override Phase 02 open questions; carry them forward until resolved.

## Open Questions Carried Forward

- Should Cerbos be adopted from day one or later?
- Should MFA be required for admins at MVP?
- Should SSO/SAML/OIDC be MVP or enterprise later?
- Should branch-level permissions be introduced in MVP?
- Should warehouse/depot-level permissions be introduced in MVP?
- Should company admins be allowed to create custom roles in MVP?
- Should support impersonation be allowed?
- Should Super Admin actions require extra confirmation?
- Should company switching be session-level or request-level?
- Should users be able to belong to companies in different tenants?
