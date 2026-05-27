# 19 — Operational Hardening And Recovery Readiness

**Project:** SaaS-first ERPNext control platform  
**Audience:** operators, backend developers, support leads, and technical leadership  
**Last updated:** 2026-05-27

---

## 1. Purpose

This document defines the detailed execution plan for **Phase 19 — operational hardening and recovery readiness**.

By this point, the platform is no longer just a set of working features. It is a system that may soon affect real customer access, real operational data, and real onboarding commitments.

The purpose of this phase is to make the platform **safe, supportable, and recoverable** before broader real-world usage.

---

## 2. Phase objective

By the end of Phase 19, the team should be able to say:

- we can detect operational problems quickly
- we can understand what happened from logs and audit records
- we can recover from common failures with documented procedures
- dangerous actions are constrained appropriately
- tenant-level operational actions follow defined policy
- the platform is credible for pilot and early-client support

This phase is about reducing operational ambiguity and preventing preventable damage.

---

## 3. Scope

### In scope

- audit logging expectations
- access-control review for dangerous actions
- error handling and actionable failure visibility
- rate-limiting strategy
- secrets-management expectations
- monitoring and alerting expectations
- backup, restore, and retention policy alignment
- deployment rollback guidance
- tenant suspension/reactivation policy
- support and incident-response readiness
- data export and operator accountability considerations

### Out of scope

- enterprise-grade compliance certification work
- formal SOC 2 program execution
- SIEM integration if not yet justified
- advanced distributed tracing platform adoption
- complex autoscaling recovery design

---

## 4. Dependencies and entry conditions

Do not start this phase until:

- the SaaS control plane is deployed and reachable
- ERPNext runtime is deployed and restore-tested at least once
- the live integration path is understood or already active
- the team can reproduce the main operator workflows
- there is at least one realistic pilot flow to protect

This phase should happen after working functionality exists, because hardening without a real workflow often hardens the wrong things.

---

## 5. Security and operations philosophy

The platform does not need maximum theoretical sophistication at this phase.

It does need:

- explicit operational rules
- visible failures
- controlled admin actions
- tested recovery steps
- enough logging to support real troubleshooting

The goal is not perfection. The goal is to avoid running production by intuition.

---

## 6. Audit logging requirements

Audit logging is a core requirement once real users and real tenant operations are involved.

### Actions that should be auditable

At minimum, record who performed sensitive actions such as:

- organization status changes
- tenant creation and status changes
- module enable/disable changes
- plan/subscription state changes
- provisioning retries or manual overrides
- integration credential or reference changes
- tenant suspension/reactivation
- destructive admin actions

### Minimum audit record shape

An audit event should make it possible to identify:

- actor
- timestamp
- target organization or tenant
- action type
- entity type and entity ID
- relevant metadata or change summary

### Why this matters

Without audit history, support and security incidents quickly turn into guesswork.

---

## 7. Access-control review for dangerous actions

A working feature is not automatically safe.

This phase must review dangerous actions and confirm they are restricted properly.

### Examples of dangerous actions

- suspending a tenant
- forcing provisioning retries
- editing integration references
- restoring a tenant environment
- changing billing or plan state manually
- changing domains or activation state
- deleting records with operational impact

### Review requirement

For each dangerous action, document:

- who is allowed to perform it
- whether approval is required
- whether the action should be reversible
- what audit event must be generated
- what support note or ticket should be created, if applicable

---

## 8. Error handling and operator-visible failures

The platform should not hide important operational failures.

### Required qualities of production errors

Errors should be:

- visible to operators
- categorized enough to be useful
- safe to expose at the right audience level
- traceable back to a relevant tenant or workflow where appropriate

### Practical expectations

Support or implementation staff should be able to distinguish between:

- user input error
- authorization failure
- dependency/service outage
- provisioning failure
- integration authentication issue
- unexpected internal server error

### Goal

A failure should tell the team what failed and where to look next, not merely that something went wrong.

---

## 9. Rate limiting and abuse control

Even if the platform is still early, some endpoints should not remain fully unprotected.

### Areas to evaluate for rate limiting

- login/auth endpoints
- password reset flows
- public contact/demo submission endpoints
- provisioning retry endpoints
- admin mutation endpoints with operational impact

### Documentation requirement

The team should document:

- which endpoints need rate limiting first
- what abuse scenario each limit protects against
- where the rate-limiting layer will live
- what operator signal indicates rate limiting is triggering too often

---

## 10. Secrets-management expectations

This project already has a clear rule: do not commit secrets and do not store them carelessly.

### For this phase, document and confirm

- where production secrets live
- who can rotate them
- which services depend on them
- how secret updates are applied without guesswork
- which values are references vs raw runtime-injected values

### Critical principle

Secrets management is not only about storage. It is also about change control and recoverability.

If a credential breaks, the team must know where to rotate it and how to validate the fix.

---

## 11. Monitoring and alerting expectations

The team needs enough monitoring to know whether the platform is healthy.

### Minimum monitoring domains

- SaaS frontend availability
- SaaS backend API availability
- ERPNext site availability for key targets
- background/provisioning health where applicable
- disk usage and host pressure on critical VMs
- certificate expiry awareness
- backup success/failure awareness

### Minimum operator outcomes

Operators should be able to answer:

- is the SaaS app up?
- is the API up?
- is the ERP runtime reachable?
- are provisioning actions failing more than expected?
- did backups run?
- is a host approaching storage or memory problems?

---

## 12. Backup, retention, and restore readiness

Backups should already exist from earlier phases, but Phase 19 must turn them into an operational policy.

### Policy topics that must be clear

- what is backed up
- how often it is backed up
- where it is stored
- how long it is retained
- who can restore
- how restore approval works
- how restore is documented after the fact

### Recovery readiness rule

A platform is not operationally ready if backup exists only as a script and no one knows whether the data can be restored under time pressure.

---

## 13. Deployment rollback guidance

The team needs a written rollback decision framework.

### Rollback should cover at least

- SaaS frontend release rollback
- SaaS backend release rollback
- configuration rollback
- reverse proxy rollback
- tenant-facing ERP update rollback or containment path

### Required decision guidance

Document:

- when rollback is mandatory
- who may authorize it
- what evidence should be captured first
- how tenant communication is handled if customer impact exists

---

## 14. Tenant suspension and reactivation policy

Tenant lifecycle operations need policy, not only technical capability.

### Questions this phase must answer

- when can a tenant be suspended?
- who can suspend a tenant?
- is suspension due to billing, abuse, security risk, or support decision?
- what remains accessible after suspension?
- what happens to data?
- who can reactivate the tenant?
- what checks are required before reactivation?

### Why this matters

Without a policy, support teams may apply inconsistent rules that create customer trust and operational risk.

---

## 15. Data export and customer accountability considerations

Even early-stage platforms should think about customer data access and exit expectations.

### Minimum documentation topics

- what data can be exported from the SaaS layer
- what data remains in ERPNext tenant runtime
- who can request exports
- who can approve exports
- how export requests are tracked

This does not need a full self-service export product yet, but it does need a position.

---

## 16. Incident response readiness

Phase 19 should define an initial incident response model.

### Basic incident categories

- SaaS outage
- ERP tenant outage
- provisioning failure
- failed deployment
- suspected credential issue
- backup/restore problem
- domain/SSL failure

### Minimum incident workflow

For each incident, the team should know:

- who owns triage
- where the first evidence is collected
- how severity is determined
- when a rollback is triggered
- when customer communication is required
- where the final incident notes are stored

---

## 17. Support operations readiness

Pilot support should not be improvised.

### Minimum support expectations

- support contact path exists
- escalation ownership is defined
- operators know the difference between SaaS-layer and ERP-layer issues
- failed provisioning has a documented support path
- known issue categories are documented

### Operational clarity rule

A support lead should be able to route an issue correctly without first reverse-engineering the architecture.

---

## 18. Hardening checklist by domain

### SaaS application hardening

- protected admin routes reviewed
- auth/session behavior reviewed
- dangerous actions audited
- user-visible errors are safe and clear

### Integration hardening

- live vs mock behavior is explicit
- integration credential references are controlled
- ERP target identity is logged clearly

### Infrastructure hardening

- hosts accessible only to intended admins
- TLS is active and renewable
- service restart behavior is reliable
- logs are available during incidents

### Recovery hardening

- backup status is visible
- restore drill has been run
- rollback path is documented
- support escalation exists

---

## 19. Deliverables

This phase should produce:

- audit logging expectations and coverage list
- dangerous-action access review
- operator-visible error handling expectations
- rate-limiting plan
- secrets-management operating notes
- monitoring and alerting checklist
- backup/retention/restore policy notes
- rollback guide
- tenant suspension/reactivation policy
- incident-response checklist

---

## 20. Exit criteria

Phase 19 is complete only when all of the following are true:

- the team can audit meaningful sensitive actions
- operator-facing failures are understandable enough to act on
- critical actions are access-controlled deliberately
- the platform has a documented rollback path
- backup and restore policy is explicit, not implied
- monitoring expectations are defined
- tenant suspension/reactivation rules are documented
- support escalation is clear enough for a pilot customer

---

## 21. Risks and common failure points

Watch for:

- adding logging that is too vague to be useful
- exposing sensitive information in logs while trying to improve visibility
- over-hardening low-value areas while leaving dangerous actions weakly controlled
- assuming backups equal recoverability without restore drills
- leaving support responsibilities ambiguous across SaaS and ERP boundaries
- deferring tenant policy decisions until after a real client issue appears

---

## 22. Handoff to Phase 20

Once the platform is hardened operationally, the team can onboard the first pilot client with far less risk.

Phase 20 should use the outputs of this phase directly:

- auditability
- support ownership
- rollback readiness
- suspension/reactivation policy
- backup and restore confidence

The output of Phase 19 is not just a working system. It is a system the team can responsibly operate for a real client.
