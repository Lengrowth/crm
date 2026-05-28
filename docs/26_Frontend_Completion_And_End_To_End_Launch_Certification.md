# 26 — Frontend Completion and End-to-End Launch Certification

**Project:** SaaS-first ERPNext control platform  
**Audience:** frontend developers, product owners, and QA/operators  
**Status:** proposed production-readiness phase  
**Last updated:** 2026-05-28

---

## 1. Purpose

This phase exists to remove the last draft/demo remnants from the user journey and prove the full SaaS path works end to end.

The audit found that the repository still contains screens and flows that are clearly described as drafts, walkthroughs, or demo-only experiences. That is acceptable for exploration, but not for first-client onboarding.

This phase turns the frontend into a launch-certified surface.

---

## 2. Why this phase must exist

Even if the backend is secure and the deployment is stable, a customer can still fail if the UI is incomplete.

The first real operator and the first real client need to be able to:

- sign in
- create or review an organization
- create or review a tenant
- understand domain and provisioning status
- move through the dashboard without placeholder screens
- complete the onboarding path without dead ends

This phase exists to prove that the visible product path is complete enough for production.

---

## 3. Scope

### In scope

- replace placeholder organization and tenant screens with persisted CRUD flows
- connect protected app pages to the real backend APIs
- remove demo-only language from critical onboarding screens
- align public marketing pages with production launch copy
- verify mobile and desktop usability for all launch-critical routes
- add browser-level end-to-end smoke coverage for the core path
- confirm error states are user-friendly and actionable

### Out of scope

- large brand redesign beyond what is needed for production readiness
- ERPNext runtime feature development
- new commercial packaging strategy
- major backend refactoring unrelated to the launch path

---

## 4. Key repository risks this phase addresses

### 4.1 Placeholder onboarding screens are still present

Draft screens are not acceptable when the product is supposed to be production-ready.

### 4.2 Critical path UX is not yet proven end to end

The control plane must be tested as a whole, not page by page only.

### 4.3 Public-facing copy still needs final verification

The marketing website should not sound like a build phase when the company is trying to sell or onboard.

---

## 5. Deliverables

- persisted organization creation flow
- persisted tenant creation flow
- completed dashboard pages for launch-critical views
- consistent protected route navigation
- real loading and error states
- removed draft/demo copy from critical flows
- e2e browser smoke suite for auth, org, tenant, domain, and provisioning visibility
- launch checklist for manual QA

---

## 6. Exit criteria

This phase is complete only when all of the following are true:

- a new operator can complete the onboarding path without hitting placeholder-only screens
- dashboard navigation is coherent and usable
- public pages read like a real product, not a scaffold
- the core user journey is covered by browser-level smoke tests
- the UI errors fail gracefully and clearly
- responsive behavior is acceptable on typical laptop and tablet viewports

---

## 7. Validation / test plan

- browser e2e smoke tests against a production-like environment
- manual operator dry run from sign-in to tenant review
- responsive layout checks on public and protected routes
- error-state verification for failed auth, failed fetches, and empty-state views

---

## 8. Dependencies

- production security and auth hardening
- stable backend CRUD and authorization
- durable provisioning and domain workflows
- a release candidate deployment environment

---

## 9. Recommended implementation order

1. Replace draft onboarding screens.
2. Wire the real CRUD actions.
3. Clean up public launch copy.
4. Add browser-level smoke coverage.
5. Run a full dry-run certification.

---

## 10. Why this phase must precede onboarding

If the UI still contains draft-only or non-persistent screens, the platform is not ready for a real customer, even if the backend is otherwise healthy.

---

## 11. What already exists in the repository

This phase is not starting from zero. The repository already contains several pieces that should be finished, connected, and verified rather than replaced.

### 11.1 Frontend foundations

- The Next.js App Router structure already exists under `frontend/app`.
- Auth, dashboard, and marketing route groups are already present.
- Shared UI primitives and shell components already exist and should be reused where possible.

### 11.2 API and data foundations

- Frontend API helpers already exist in `frontend/lib/api.ts`, `frontend/lib/auth-api.ts`, and `frontend/lib/auth.ts`.
- The backend already exposes the control-plane data needed for organizations, tenants, domains, and provisioning visibility.
- Protected flows should build on the existing authenticated request patterns rather than introducing a parallel client layer.

### 11.3 Phase continuity

- Phase 24 focuses on security, authorization, and billing integrity.
- Phase 25 focuses on durable provisioning, domain automation, observability, and recovery.
- Phase 26 should finish the user-facing launch path and prove the full experience is coherent enough for onboarding.

---

## 12. Workstreams in this phase

### 12.1 Replace draft screens with real control-plane flows

The visible onboarding path should stop looking like a scaffold and start behaving like a launch-ready SaaS surface.

Expected outcomes:

- organization pages read and update persisted data
- tenant pages show real status and actions
- dashboard routes no longer rely on placeholder-only content
- empty states guide the user toward the next real action

### 12.2 Make the protected app shell coherent

Navigation should feel like one product, not a collection of partial screens.

Expected outcomes:

- route transitions are predictable
- active states and page hierarchy are clear
- loading and error states are consistent across launch-critical views
- mobile and tablet layouts remain usable

### 12.3 Finish public launch copy

Marketing pages should sound like a live product that is ready to sell and support, not an internal prototype.

Expected outcomes:

- placeholder or demo language is removed from public pages
- copy matches the current production scope
- calls to action reflect the actual onboarding path
- public pages align with the platform’s real capabilities

### 12.4 Add browser-level certification coverage

The final launch path should be verified by browser smoke tests, not just manual review.

Expected outcomes:

- sign-in and entry into the app shell are covered
- organization and tenant journeys are covered
- domain and provisioning visibility are covered
- the tests fail when placeholder-only routes or broken navigation reappear

---

## 13. Operational acceptance criteria

This phase is complete only when the following can be demonstrated in a production-like environment:

- a new operator can sign in and reach the dashboard without encountering draft-only screens
- organization and tenant pages display and update real persisted state
- the user can understand provisioning and domain status from the UI alone
- the public website reads like a finished product ready for onboarding
- loading, empty, and error states are clear enough for support use
- the core launch path passes browser-level smoke tests
- the application remains usable on common laptop and tablet viewports

---

## 14. Dependencies and sequencing

### 14.1 Dependencies

- production security and authorization hardening
- durable provisioning and domain automation
- stable backend CRUD and read APIs
- release-candidate deployment environment
- browser automation test coverage and test data setup

### 14.2 Recommended sequence

1. Replace placeholder onboarding and dashboard screens.
2. Wire the real CRUD and status views.
3. Clean up public launch copy and route messaging.
4. Add or update browser-level smoke coverage.
5. Run a full launch certification dry run.

---

## 15. Notes for implementation planning

- Prefer finishing the existing app structure over creating new route groups or duplicate screens.
- Keep the UI changes focused on launch readiness rather than a broad redesign.
- Treat browser smoke coverage as a release gate, not a nice-to-have regression test.
- Do not mark this phase complete until the team can walk a new operator through the full SaaS path without explaining away placeholders or dead ends.
