# 18 — Live SaaS ↔ ERPNext Integration Cutover

**Project:** SaaS-first ERPNext control platform  
**Audience:** backend developers, operators, and implementation leads  
**Last updated:** 2026-05-27

---

## 1. Purpose

This document defines the detailed execution plan for **Phase 18 — live SaaS ↔ ERPNext integration cutover**.

The purpose of this phase is to move the platform from **mock integration behavior** to a **real ERPNext connection path** under controlled conditions.

This is the phase where the SaaS control layer stops pretending to provision or inspect ERPNext and begins interacting with a real runtime.

---

## 2. Phase objective

By the end of Phase 18, the SaaS platform should be able to:

- identify and reference a real ERPNext tenant site
- use the live ERPNext integration client rather than the mock path in production
- check site health against a live environment
- execute controlled provisioning-related actions against that environment
- record live integration references and statuses in the SaaS layer
- fail safely when integration problems occur

This phase is the bridge between infrastructure readiness and real customer operations.

---

## 3. Scope

### In scope

- real integration client activation
- mock vs live path clarification
- tenant-to-site mapping rules
- live credential reference usage
- health-check validation against ERPNext
- provisioning smoke tests against a real site
- backup/restore call validation where the integration supports it
- safe production toggle and rollback design
- operator checklist for cutover

### Out of scope

- broad ERP business-process customization
- self-service tenant creation by customers without operator oversight
- large-scale job orchestration redesign beyond what is needed for safe cutover
- advanced event-driven integration architecture

---

## 4. Dependencies and entry conditions

Do not start this phase until:

- Phase 16 SaaS deployment is stable
- Phase 17 ERPNext deployment is stable
- a real ERPNext demo or tenant site exists
- backend integration abstractions already exist in the codebase
- the team understands where mock behavior still exists
- integration credentials can be provided securely by reference

Recommended pre-cutover state:

- mock client behavior still works in development
- live client is implemented or partially implemented
- backend logs clearly show which integration path is being used
- at least one non-production site is available for live validation

---

## 5. Core architectural rule

The SaaS control plane remains the orchestrator. ERPNext remains the runtime.

That means:

- SaaS stores tenant metadata and operational intent
- SaaS initiates supported actions
- ERPNext executes tenant runtime behavior
- integration state is observable from the SaaS side
- ERP tenant business data does not become SaaS control-plane data

This rule prevents the integration cutover from blurring system boundaries.

---

## 6. What “cutover” means in this project

Cutover does **not** mean removing all mock code immediately.

It means:

- production or pilot environments use the live client path intentionally
- operators can tell whether a request used mock or live integration
- the live path has been validated against a real ERPNext site
- the fallback/rollback path is documented if live calls fail unexpectedly

### Practical interpretation

Mock mode can still exist for local development, isolated tests, or CI. It should not be the hidden default for real deployment environments.

---

## 7. Mock vs live mode strategy

This phase must remove ambiguity.

### Required behaviors

The system should make it obvious:

- whether the current environment is using mock or live integration
- where that decision is configured
- how operators verify the active mode
- how the application logs mode selection and failures

### Required documentation outcome

The team should be able to answer:

- what enables live mode?
- what blocks live mode?
- what is the rollback path to mock or safe-disable mode for non-production?
- how do we prevent accidental mock usage in production?

---

## 8. Tenant-to-site mapping model

A stable mapping model is mandatory.

### Required tenant metadata

Each SaaS tenant should be able to reference:

- organization ID
- tenant slug
- environment
- ERPNext site name
- ERPNext base URL
- provisioning/integration status
- credential reference or integration reference ID

### Mapping principle

One SaaS tenant record should map clearly to one ERPNext site runtime target for the given environment.

If one organization later has multiple sites, the mapping must still remain explicit and not inferred from naming alone.

### Why this matters

Without a formal mapping rule, the system risks:

- provisioning actions hitting the wrong site
- health checks targeting the wrong domain
- support teams misreading the environment relationship

---

## 9. Credential and secret-reference handling

This phase must use the project’s existing rule: do **not** store raw secrets carelessly.

### Required approach

The SaaS layer should store:

- credential references
- secret manager references
- labels and provider metadata
- status/rotation metadata if implemented

It should avoid storing live raw ERP credentials directly in plain database fields.

### Operator expectations

Document:

- who creates the ERP credential
- where the secret value is stored
- how the SaaS app references it
- how credential rotation will happen later

---

## 10. Live health-check validation

The first live function to validate should be health/status, because it is lower risk than broad mutation workflows.

### Health-check goals

The SaaS layer should be able to confirm:

- the ERPNext site is reachable
- authentication works
- the site responds as expected
- status failures are visible to operators

### Minimum validation outputs

A health check should let the team determine:

- reachable vs unreachable
- authorized vs unauthorized
- healthy vs degraded
- target site identity

### Why start here

If health checks are unreliable, provisioning and admin automation will be unreliable too.

---

## 11. Live provisioning smoke tests

After health-check success, validate a narrow set of controlled live operations.

### Suggested smoke-test order

1. resolve tenant-to-site mapping
2. run site health check
3. fetch a simple authorized ERP endpoint or metadata probe
4. test a low-risk provisioning-related action if supported
5. confirm SaaS-side logging and status updates

### Cutover rule

Do not begin with high-risk destructive actions. Start with visibility and low-risk operations first.

---

## 12. Backup and restore integration checks

If the integration layer includes backup or restore endpoints/actions, validate them deliberately.

### Minimum expectations

- backup invocation path is understood
- backup status can be observed
- failure states are clear
- restore remains operator-controlled unless explicitly automated

### Important safety note

Restore operations should remain tightly controlled. They are not a good candidate for casual experimentation during the first production cutover.

---

## 13. Observability requirements

A live integration path without observability is dangerous.

### The SaaS side should make visible

- which tenant initiated the action
- which ERP site was targeted
- which integration mode was active
- whether the request succeeded or failed
- the high-level failure category
- when the action occurred

### Logging guidance

Do not log raw secrets. Log identifiers, status transitions, and actionable failure context.

---

## 14. Failure handling and operator behavior

This phase must define how the system behaves when live ERP calls fail.

### Required failure categories to think through

- DNS/network unreachable
- authentication failure
- target site not found
- timeout
- partial provisioning failure
- ERP application error

### Required operator outcome

When a live call fails, the team should know:

- whether it is safe to retry
- whether tenant metadata is still correct
- whether the target site changed state partially
- whether rollback or manual intervention is required

---

## 15. Production toggle and safeguards

A safe toggle path is one of the most important outputs of this phase.

### Required control points

The team must know:

- how live mode is enabled
- how mock mode is disabled for production
- how non-production environments remain able to use mock mode intentionally
- how an accidental misconfiguration will be detected quickly

### Safety principle

Make production behavior explicit, not implicit.

Do not let a missing setting silently fall back to mock behavior in a live environment unless that is a consciously documented emergency choice.

---

## 16. Cutover execution plan

Use a staged cutover rather than a big-bang switch.

### Suggested sequence

1. validate the live ERP site manually outside the SaaS flow
2. verify the SaaS environment is correctly configured for live mode
3. run SaaS-side live health checks on a demo site
4. run one controlled provisioning smoke test on a demo or non-critical tenant
5. verify logs, statuses, and UI/operator visibility
6. repeat on the intended pilot tenant only after the demo path is stable

### Why this matters

Integration cutovers fail when too many unknowns are introduced at once. Stage the change.

---

## 17. Rollback strategy

Rollback must exist before cutover starts.

### Minimum rollback options

- disable live integration for the affected environment
- revert to operator-driven manual steps temporarily
- preserve tenant mapping and logs for troubleshooting
- prevent duplicate provisioning attempts caused by confusion

### Rollback triggers

Rollback or pause if:

- health checks fail consistently
- the wrong site is being targeted
- authentication errors cannot be resolved quickly
- provisioning smoke tests cause inconsistent state
- the team cannot determine whether live or mock mode is active

---

## 18. Deliverables

This phase should produce:

- explicit live-vs-mock mode documentation
- validated tenant-to-site mapping rules
- live health-check capability
- controlled live provisioning smoke-test results
- integration credential reference plan
- logging/visibility for live operations
- operator cutover checklist
- rollback checklist

---

## 19. Exit criteria

Phase 18 is complete only when all of the following are true:

- the SaaS app can target a real ERPNext site intentionally
- production or pilot mode uses the live client path knowingly
- the active integration mode is visible and not ambiguous
- health checks work against a live site
- at least one controlled live provisioning-related smoke test has succeeded
- failures are observable and actionable
- rollback or temporary safe-disable behavior is documented

---

## 20. Risks and common failure points

Watch carefully for:

- hidden fallback to mock behavior
- inconsistent tenant/site naming and mapping
- missing credential-reference wiring
- success states recorded in SaaS when ERP changes did not actually happen
- poor logging that hides whether a failure was network, auth, or application-level
- attempting broad provisioning automation before the health-check path is trustworthy

---

## 21. Handoff to Phase 19

Once live integration works, the platform becomes much closer to real customer impact.

Phase 19 must then harden the platform operationally, including:

- auditability
- operator-visible failures
- recovery readiness
- support processes
- monitoring and rollback discipline

The output of Phase 18 is a real integrated platform. The output of Phase 19 must be a platform that is safe to operate.
