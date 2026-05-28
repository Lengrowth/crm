# 25 — Durable Provisioning, Domain Automation, Observability, and Recovery

**Project:** SaaS-first ERPNext control platform  
**Audience:** infrastructure operators, backend developers, and support leads  
**Status:** proposed production-readiness phase  
**Last updated:** 2026-05-28

---

## 1. Purpose

This phase exists to convert the remaining operationally fragile parts of the platform into durable, observable, and recoverable workflows.

The repository already contains runbooks and some operational primitives, but the audit shows the following are still not strong enough for a first real client:

- provisioning is still too dependent on in-process execution in key paths
- domain lifecycle actions are still too metadata-heavy and manual
- backup and restore are described, but not fully enforced operationally
- observability exists in fragments, not as a production operating system
- rollback is documented more than it is proven

This phase closes that gap.

---

## 2. Why this phase must exist

A production SaaS platform must survive failures.

If a tenant provisioning run fails, operators need a durable retry path.
If a domain cannot be verified or activated, operators need a visible lifecycle.
If a restore is needed, the team must know it works before a client is impacted.
If the deployment breaks, rollback must be repeatable.

This phase makes those requirements concrete.

---

## 3. Scope

### In scope

- durable provisioning queue / worker execution
- persisted retry and failure handling for provisioning jobs
- explicit state transitions for provisioning and domain lifecycles
- DNS verification and SSL issuance automation for custom domains
- offsite backup sync and retention policy enforcement
- restore drill automation and verification
- production logs, metrics, and alerting baseline
- deploy-time smoke tests and rollback validation

### Out of scope

- major ERPNext product customization
- new commercial billing features
- redesign of the public website
- replacing the existing SaaS control-plane architecture

---

## 4. Key repository risks this phase addresses

### 4.1 Provisioning still needs stronger durability

In-process or ephemeral handling is not enough for real customer onboarding.

### 4.2 Domain management is still mostly operator-driven

The platform needs an automated path from pending DNS to verified and active.

### 4.3 Recovery is not yet proven enough

Backups and restore need to be tested as if a real incident happened.

### 4.4 Observability is incomplete

Operators must be able to answer, quickly and confidently:

- is the platform healthy?
- what failed?
- which tenant was affected?
- can we retry safely?
- did the rollback work?

---

## 5. Deliverables

- durable provisioning job execution with retry support
- persisted provisioning logs and failure states
- automated domain verification and SSL issuance workflow
- domain activation status transitions with audit trail
- offsite backup sync to object storage
- documented and tested restore drill
- monitoring and alerting baseline
- deploy and rollback smoke tests
- operator-facing status views for provisioning and recovery

---

## 6. Exit criteria

This phase is complete only when all of the following are true:

- failed provisioning jobs can be retried safely and visibly
- domain lifecycle transitions are automated or operator-safe with strong audit records
- backups are copied off-host and retention is defined
- restore has been rehearsed and succeeds in a controlled drill
- operators can detect major service issues without guesswork
- deployment rollback is proven in a rehearsal
- the operational state of the system is visible enough to support a real client

---

## 7. Validation / test plan

- forced provisioning failure and retry tests
- DNS/SSL happy-path and failure-path tests
- backup generation and offsite sync verification
- restore drill on a controlled target
- health/alert smoke checks after deploy
- rollback rehearsal from a known-good revision

---

## 8. Dependencies

- production control-plane deployment
- production security and auth hardening
- ERPNext live integration cutover
- object storage or backup target configuration
- monitoring/alerting destination(s)

---

## 9. Recommended implementation order

1. Make provisioning durable.
2. Automate domain lifecycle transitions.
3. Add backup/restore enforcement.
4. Add monitoring and alerts.
5. Rehearse rollback and recovery.

---

## 10. Why this phase must precede onboarding

A client should never be the first place the team discovers that backups do not restore, provisioning cannot be retried, or domain activation is still manual and fragile.

That kind of discovery belongs in rehearsal, not in a live onboarding window.

---

## 11. What already exists in the repository

This phase is not starting from zero. The repository already contains several pieces that should be hardened and connected rather than replaced.

### 11.1 Durable provisioning foundations

- `ProvisioningJob` already exists as a persisted job record.
- The provisioning worker already supports queue, retry, and completion semantics in-process.
- Provisioning logs and failure details are already modeled in the database.

### 11.2 Domain lifecycle foundations

- Domain metadata already includes status, DNS verification, SSL status, and manual activation flags.
- The domain management work already distinguishes system subdomains from custom domains.
- Operator-facing notes and audit fields already exist for manual actions.

### 11.3 Recovery and operational foundations

- The operational hardening and recovery readiness doc already defines backup, restore, and rollback expectations.
- The ERPNext integration maturation phase already established a mock/live integration boundary.
- The roadmap already recognizes backup/restore and rollback as prerequisites for onboarding.

---

## 12. Workstreams in this phase

### 12.1 Make provisioning durable by design

The provisioning flow should be treated as a durable workflow, not a best-effort request handler.

Expected outcomes:

- job state survives process restarts
- retries are explicit and visible
- failed jobs can be reviewed by operators
- provisioning progress is auditable from the control plane

### 12.2 Automate the custom-domain lifecycle

Custom-domain handling should move from manual coordination toward a visible state machine.

Expected outcomes:

- DNS verification is checked and recorded
- SSL issuance is triggered or validated automatically
- transitions from pending to active are explicit
- manual intervention remains possible when automation cannot complete safely

### 12.3 Make backup, restore, and rollback provable

Recovery is only useful if the team can demonstrate it under controlled conditions.

Expected outcomes:

- backups are generated on a defined schedule
- offsite copies are verified
- restore drills are repeatable
- rollback steps are documented and rehearsed

### 12.4 Turn observability into an operating system

Operators need a concise answer to every live incident question.

Expected outcomes:

- logs identify the tenant and workflow involved
- metrics show provisioning health and recovery readiness
- alerts surface failed jobs and domain issues
- status views expose enough context to make safe retry decisions

---

## 13. Operational acceptance criteria

This phase is complete only when the following can be demonstrated in a production-like environment:

- a failed provisioning job can be retried without losing context
- a provisioning failure is visible without reading raw application logs
- a custom domain can move from pending DNS to active with minimal manual effort
- a failed domain verification attempt leaves a clear audit trail
- a backup can be restored from the configured offsite target
- a restore drill can be repeated and documented
- a rollback rehearsal can be completed against a known-good revision
- operators can identify the affected tenant, workflow, and failure reason quickly

---

## 14. Dependencies and sequencing

### 14.1 Dependencies

- production security and authorization hardening
- durable provisioning job storage and worker execution
- domain metadata and lifecycle state models
- offsite backup target configuration
- monitoring and alerting destination(s)
- production deployment / rollback validation path

### 14.2 Recommended sequence

1. Harden provisioning persistence and retry behavior.
2. Automate domain verification and SSL lifecycle transitions.
3. Add backup sync and restore validation.
4. Establish metrics, logs, and alerting for the new workflows.
5. Rehearse rollback and recovery before client onboarding.

---

## 15. Notes for implementation planning

- Prefer incremental hardening of the existing workflow model over a full rewrite.
- Keep operator override paths available for the cases automation cannot safely resolve.
- Treat success as both a technical and operational property: it must work and it must be visible.
- Do not mark this phase complete until the team can explain how to recover from provisioning, domain, backup, and rollback failures without guessing.
