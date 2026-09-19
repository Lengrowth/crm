# Phase 04 — Role-Based ERP Shell and Module Home

## AI goal

Turn the installed module set into a coherent Champion ERP experience with task-oriented navigation, consistent module homes, responsive layouts and clear movement back to the control plane.

## Build scope

1. Expand the version-controlled Champion workspace instead of editing ERP production records by hand.
2. Create role-oriented entry experiences for Administration, Office/Dispatch, Sales, Accounting, Inventory, Field, HR/Payroll, Quality/Support and Read-only audiences.
3. Add the target navigation from the program README, hiding irrelevant modules without weakening server permissions.
4. Provide a module home pattern containing:
   - plain-language purpose;
   - two or three primary actions;
   - recent/assigned work;
   - exception or attention cards sourced from real records;
   - useful empty state;
   - help/context link.
5. Add product, organization, environment and current-role context.
6. Add `LenERP Control Plane` to the ERP user dropdown and `Open ERP` to the control-plane tenant context using Phase 03’s authorized handoff.
7. Ensure standard ERPNext/HRMS routes remain compatible and direct-route authorization remains effective.
8. Keep standard advanced workspaces accessible only to approved administrator roles.

## UX requirements

- Prefer Champion concepts such as Office Board, Wells & Jobs, Crew & Hours, Callbacks & Quality and Support & Requests.
- Do not rename underlying records inconsistently across forms, reports and documentation.
- The first screen answers: What needs my attention? What can I do? Where am I?
- Navigation remains usable at 320 CSS pixels and 200% browser zoom.
- Keyboard users can reach the application switcher, primary menu, page actions and profile menu predictably.
- Status chips include text and accessible names, not color alone.
- Sensitive totals never appear on roles lacking financial/payroll permission.

## Acceptance tests

- Every approved role lands on a useful home and sees only intended navigation.
- Hidden links remain denied through direct URL and API access.
- Every promised module has a working route or an honest `Pending configuration` state; there are no dead cards.
- Control-plane and ERP cross-links preserve tenant context and pass the Phase 03 authorization flow.
- Desktop, tablet, mobile, light/dark, keyboard, zoom and axe checks pass.
- Empty, partial, slow and failed API states remain understandable.
- Existing Well, Job, Customer, Quote, Invoice, Asset and report routes still work.

## Non-goals

- Rebuilding every standard ERPNext form.
- Applying final Champion branding before approval.
- Creating business rules that belong to later workflow phases.

## Gate and rollback

Ship the new workspace/menu behind a server-controlled role or feature flag. Keep the previous Champion workspace available until the new shell passes staging. Rollback disables the new workspace and restores the previous navigation; permissions remain authoritative.

## Execution prompt

> Build the role-based Champion ERP shell and module-home experience described here inside `lenerp_core` and the control-plane tenant context. Reuse standard ERPNext/HRMS records, enforce permissions independently of visibility, preserve existing routes, add complete responsive/accessibility/error states, and keep unaccepted configuration labeled synthetic or pending.
