# 17 — ERPNext Deployment On GCP

**Project:** SaaS-first ERPNext control platform  
**Audience:** infrastructure operators, implementation leads, and technical admins  
**Status:** planning and readiness runbook only  
**Last updated:** 2026-05-27

---

## 1. Purpose

This document turns **Phase 17** into an operator-friendly deployment preparation and execution checklist for **ERPNext/Frappe as the external tenant runtime** on Google Cloud Platform.

It is written as a **runbook and checklist**, not as proof that ERPNext has already been deployed.

Phase 17 covers:

- the dedicated GCP VM for ERPNext/Frappe
- host preparation for the ERP runtime
- ERPNext/Frappe stack installation path
- demo site creation
- tenant site creation pattern
- DNS and HTTPS for ERP sites
- backup and restore readiness
- restart, smoke-test, and rollback procedures

Phase 17 does **not** include:

- SaaS control-plane deployment work from Phase 16
- live SaaS ↔ ERPNext integration cutover from Phase 18
- customer self-service tenant provisioning from the SaaS UI
- advanced HA, multi-node clustering, or Kubernetes
- broad ERP customization beyond establishing the runtime and documented custom app path

---

## 2. Phase boundary and operating rule

### Core rule

Treat this phase as **ERP runtime deployment and operator readiness**, not as SaaS integration cutover.

That means the output of this phase should be:

- a stable ERPNext host
- a stable demo site
- a repeatable tenant site creation pattern
- documented backup and restore steps
- a clear operator runbook for restart, smoke tests, and rollback

It should **not** imply that:

- the SaaS backend is already using live ERPNext in production
- the mock/live cutover is complete
- tenant provisioning from the SaaS layer is already automated end to end

### Architecture rule

ERPNext remains an **external managed system**.

- SaaS owns tenant metadata, modules, billing state, provisioning metadata, and orchestration intent.
- ERPNext owns ERP runtime behavior and tenant application data.

Deployment, access control, backup, incident response, and change control should preserve that separation.

---

## 3. What Phase 17 now asks the team to do

Phase 17 is now asking the team to prepare and execute a **repeatable dedicated-VM ERPNext deployment path** in this order:

1. confirm prerequisites and naming rules
2. prepare the ERPNext GCP VM, networking, and DNS plan
3. prepare the host layout and base packages
4. prepare the ERPNext/Frappe runtime installation path
5. create and validate a demo site
6. create and validate a tenant site pattern
7. document the custom app installation path
8. configure DNS and TLS for ERP hostnames
9. validate backup and restore procedures
10. define restart, smoke-test, and rollback procedures
11. stop before Phase 18 live SaaS integration cutover begins

---

## 4. Recommended target topology

For this phase, use **one dedicated ERPNext VM separate from the SaaS VM**.

### Recommended machines

- **VM 1:** SaaS control plane
- **VM 2:** ERPNext/Frappe runtime

### Why a separate ERP VM is the right target

- ERPNext is materially heavier than the SaaS app.
- ERP maintenance should not break the public website or SaaS dashboard.
- Backup and restore workflows are clearer when isolated.
- Performance troubleshooting is easier.
- This matches the SaaS-first architecture boundary already documented.

### Recommended ERP host responsibilities

The ERPNext VM should host:

- ERPNext/Frappe runtime
- MariaDB
- Redis
- workers and scheduler
- site storage
- web edge for ERP traffic
- backup scripts and backup upload path

---

## 5. Phase 17 exit criteria

Phase 17 is ready to close when all of the following are true:

- the operator checklist in this document is complete and understandable
- the ERPNext VM shape, hostnames, and site naming conventions are chosen
- the runtime installation path is documented and repeatable
- a demo site has been created and validated over HTTPS
- a repeatable tenant site creation path is documented and validated
- backup has been executed successfully against a controlled target
- restore has been tested successfully against a controlled target
- the document makes it explicit that live SaaS ↔ ERPNext cutover remains Phase 18 work

---

## 6. Operator checklist

Use this section as the main execution-order checklist.

---

### 6.1 Prerequisites and entry gate

Do not start ERP host creation until these are true:

- [ ] The team has read:
  - `docs/15_Next_Phases_Production_Roadmap.md`
  - `docs/17_ERPNext_Deployment_On_GCP.md`
  - `docs/18_Live_SaaS_ERPNext_Integration_Cutover.md`
  - `docs/21_GCP_SaaS_And_ERPNext_Deployment_Guide.md`
- [ ] The SaaS control-plane deployment path from Phase 16 is already documented and understood.
- [ ] Operators understand that Phase 17 deploys ERPNext as an external runtime, not as part of the SaaS app host.
- [ ] Operators agree on initial site naming rules.
- [ ] Operators agree on demo-site vs tenant-site separation.
- [ ] Operators agree on the backup destination strategy.
- [ ] Operators agree that live SaaS ↔ ERPNext cutover is **not** part of this phase.

### 6.2 Naming and identity checklist

Before deployment, decide the identity rules that Phase 18 will later depend on.

- [ ] Choose a demo hostname, for example `demo.yourdomain.com`.
- [ ] Choose a tenant hostname pattern, for example `tenant-slug.yourdomain.com`.
- [ ] Choose a tenant slug convention that matches SaaS tenant records later.
- [ ] Decide how environment labels will be recorded, for example `demo`, `pilot`, or `production`.
- [ ] Decide who is allowed to create, rename, or restore ERP sites.

### 6.3 GCP project and access preparation

Prepare the GCP account and permissions before creating the ERP host.

- [ ] Confirm the correct GCP project exists.
- [ ] Confirm billing is enabled.
- [ ] Confirm Compute Engine API is enabled.
- [ ] Confirm who has operator SSH access.
- [ ] Reserve a static external IP for the ERPNext VM.
- [ ] Confirm which DNS provider controls the ERP hostnames.
- [ ] Confirm where backups will be stored.
- [ ] Confirm who is allowed to trigger restores.

### 6.4 ERP VM creation checklist

Create one Ubuntu LTS VM for ERPNext/Frappe.

Recommended starting profile:

- 4 vCPU or higher
- 8–16 GB RAM depending on pilot load expectations
- SSD persistent disk sized for site data, logs, and backups
- Ubuntu LTS

Checklist:

- [ ] Create the VM in the chosen region/zone.
- [ ] Attach the reserved static IP.
- [ ] Restrict SSH access to trusted admin IPs.
- [ ] Allow inbound HTTP on `80`.
- [ ] Allow inbound HTTPS on `443`.
- [ ] Do **not** expose internal service ports publicly.
- [ ] Document the VM name, zone, and IP in the operator notes.

### 6.5 DNS preparation checklist

Prepare DNS only after the VM and static IP are known.

- [ ] Create or plan the A record for the demo site.
- [ ] Create or plan the A record pattern for the first tenant site.
- [ ] Confirm the DNS pattern can scale to additional tenants later.
- [ ] Wait for propagation before TLS issuance.

---

## 7. Host layout checklist

Use a predictable host structure so operators know where runtime data, config, and backups live.

### Recommended host layout

```txt
/opt/erpnext-runtime/
  runtime/
  shared/
    config/
    logs/
    backups/
    compose/
  scripts/
```

### Directory purpose

- `runtime/` — checked-out runtime assets or deployment working tree
- `shared/config/` — local environment files and runtime-specific config kept off git where applicable
- `shared/logs/` — operator-visible logs or exported logs
- `shared/backups/` — local backup staging path if needed before upload
- `shared/compose/` — saved runtime or compose-related backups before changes
- `scripts/` — local helper scripts for restart, backup, restore, smoke tests, and rollback

### Host layout checklist

- [ ] Create `/opt/erpnext-runtime/`.
- [ ] Create `runtime/`, `shared/config/`, `shared/logs/`, `shared/backups/`, `shared/compose/`, and `scripts/`.
- [ ] Decide which service user or operator account owns the ERP runtime.
- [ ] Keep secrets and local runtime config outside the repository working tree where practical.

---

## 8. Base host bootstrap checklist

Install the minimum packages needed to run ERPNext/Frappe.

### Required runtime families

- Git
- Docker
- Compose support
- common CLI utilities for logs, networking, and archive handling

### Preparation checklist

- [ ] Install Git.
- [ ] Install Docker.
- [ ] Install Compose support.
- [ ] Verify Docker starts on boot.
- [ ] Verify `docker --version`.
- [ ] Verify the compose workflow the team will use.
- [ ] Confirm disk availability for sites, logs, and backups.
- [ ] Confirm host time sync and hostname are correct.

### Operational note

Treat the ERP host like a managed runtime node, not a personal sandbox. Avoid unrelated software on this machine.

---

## 9. ERPNext runtime installation checklist

This phase needs a documented and repeatable ERPNext/Frappe runtime installation path.

### Operator outcome required

By the end of this step, the team must be able to answer:

- where the runtime assets live
- how the stack is started
- how logs are checked
- how the stack is restarted
- how upgrades will later be performed safely

### Runtime checklist

- [ ] Decide the canonical ERPNext deployment source or runtime assets to use.
- [ ] Place the runtime assets in the agreed host location.
- [ ] Configure the required local environment and runtime settings.
- [ ] Start the runtime stack.
- [ ] Confirm the web-facing service starts cleanly.
- [ ] Confirm MariaDB is healthy.
- [ ] Confirm Redis is healthy.
- [ ] Confirm ERP workers and scheduler are healthy.
- [ ] Record the exact operator start and restart commands.

### Phase caution

Do not mix Phase 17 ERP host changes with Phase 18 live SaaS cutover changes. Stabilize the ERP runtime first.

---

## 10. Demo site checklist

Create a demo site before creating the first tenant site.

### Why the demo site comes first

- it confirms the runtime is healthy
- it gives the team a safer validation target
- it provides the first real target for future Phase 18 cutover tests
- it avoids using a pilot tenant as the first restore experiment

### Demo site checklist

- [ ] Create the demo site.
- [ ] Install ERPNext on the demo site.
- [ ] Configure the demo site hostname.
- [ ] Issue or attach HTTPS for the demo site.
- [ ] Confirm the site loads over HTTPS.
- [ ] Confirm admin login works.
- [ ] Confirm the base ERPNext application is usable.
- [ ] Record the exact operator steps used.

---

## 11. Tenant site creation checklist

After the demo site is stable, document a manual but repeatable tenant site creation pattern.

### Tenant site checklist

- [ ] Create one test or pilot tenant site.
- [ ] Install ERPNext on that site.
- [ ] Assign the chosen tenant hostname.
- [ ] Issue or attach HTTPS.
- [ ] Confirm the site loads successfully.
- [ ] Confirm first admin access works.
- [ ] Record the exact operator steps to create future tenant sites.
- [ ] Record where site-specific settings and logs can be found.

### Required output for Phase 18 readiness

Document what will later need to be recorded in the SaaS control layer for each tenant:

- tenant slug
- ERP site name
- primary hostname
- environment label
- operator notes on creation time or references

---

## 12. Custom app installation checklist

If a custom Frappe app exists or is expected soon, document the installation path now rather than improvising later.

### Custom app checklist

- [ ] Document where the custom app source is obtained.
- [ ] Document how the app is installed into the ERP runtime.
- [ ] Document how the app is enabled for a site.
- [ ] Document version compatibility checks.
- [ ] Document how updates will be applied safely later.

### Important note

This does not require broad ERP customization in this phase. It requires an operator-safe installation path.

---

## 13. DNS and TLS checklist

Each ERP site in this phase needs a clear hostname and HTTPS plan.

### Required DNS outcomes

- [ ] Demo site hostname resolves to the ERP VM static IP.
- [ ] Tenant site hostname resolves to the ERP VM static IP.
- [ ] The naming pattern is easy to manage and verify.
- [ ] The naming pattern can scale to additional tenants later.

### Required TLS outcomes

- [ ] Certificates issue successfully.
- [ ] Browser trust is clean.
- [ ] Renewal behavior is documented.
- [ ] HTTPS behavior is verified for both demo and tenant sites.

### Boundary note

Custom branded client domains can come later. Start with predictable subdomains first so Phase 18 mapping and operator troubleshooting stay simple.

---

## 14. Backup checklist

Do not treat backup as optional. Before any real client onboarding, the ERP runtime must support a basic, tested backup flow.

### Backup scope

Backups should cover, at minimum:

- site database
- site files or assets as required by the runtime
- critical runtime configuration where applicable

### Backup checklist

- [ ] Choose the backup destination, preferably remote storage such as Cloud Storage.
- [ ] Document how backups are triggered.
- [ ] Document where backups are stored.
- [ ] Document retention expectations.
- [ ] Document who is allowed to restore.
- [ ] Execute at least one controlled backup successfully.
- [ ] Record the exact operator backup steps.

---

## 15. Restore drill checklist

A backup policy is incomplete until restore is tested.

### Minimum restore drill for this phase

- [ ] Identify a non-production site backup.
- [ ] Restore it in a controlled way.
- [ ] Confirm the restored site boots successfully.
- [ ] Confirm admin access works.
- [ ] Confirm expected data appears intact.
- [ ] Record the exact operator restore steps.

### Restore success criteria

- [ ] ERPNext loads successfully after restore.
- [ ] Login works.
- [ ] Restore steps are repeatable without guesswork.
- [ ] Operators know when restore is allowed and who approves it.

---

## 16. Operational health and smoke-test checklist

Run these checks after the runtime starts and after any candidate deployment or maintenance change.

### Host/runtime checks

- [ ] VM is reachable by SSH.
- [ ] Docker is active.
- [ ] The ERP runtime stack is healthy.
- [ ] Logs show no unresolved fatal startup issues.
- [ ] Demo site is reachable over HTTPS.

### Demo site smoke tests

- [ ] Demo site homepage loads.
- [ ] Admin login works.
- [ ] ERPNext loads successfully after login.
- [ ] Basic navigation works.

### Tenant site smoke tests

- [ ] Tenant site loads over HTTPS.
- [ ] Tenant admin login works.
- [ ] Naming convention matches the documented pattern.

### Resilience checks

- [ ] A backup completed successfully.
- [ ] A restore drill has been performed and recorded.

---

## 17. Restart procedure

Use this after config changes, runtime updates, or host reboot validation.

### Restart order

1. restart the ERP runtime stack
2. confirm web service health
3. confirm demo-site availability
4. confirm tenant-site availability
5. rerun smoke tests

### Operator expectations

- [ ] exact restart command is documented
- [ ] logs can be checked immediately after restart
- [ ] operators know where to look for failing services

### Restart success criteria

- [ ] runtime services return healthy state
- [ ] demo site loads successfully
- [ ] tenant site loads successfully
- [ ] no obvious worker or scheduler failure remains unresolved

---

## 18. Rollback procedure

Rollback should restore ERP runtime availability quickly and safely.

### Minimum rollback assets to keep

- previous known-good runtime revision or deployment asset reference
- previous compose or runtime config backup
- recent verified backup before risky changes
- operator notes on the last known-good stack state

### Rollback triggers

Rollback if any of these remain broken after a focused restart check:

- demo site is unavailable
- tenant site is unavailable
- web runtime remains unhealthy
- workers or scheduler fail persistently
- changes introduce unresolved 5xx or startup failures
- restore confidence is reduced because the runtime state is unclear

### Rollback steps

1. stop and inspect the failing runtime briefly
2. restore the last known-good runtime config or deployment asset
3. restart the runtime stack
4. recheck logs and web health
5. rerun demo-site and tenant-site smoke tests
6. confirm backup posture is still understood after rollback

### Rollback warning

Do not combine rollback improvisation with live SaaS cutover work. Stabilize ERPNext first, then resume later phases.

---

## 19. What is still not done after Phase 17

Even after this document is complete and the runtime is deployed, the following work is still not done:

- live SaaS ↔ ERPNext integration cutover
- activation of the live ERPNext client path from the SaaS backend
- validated tenant-to-site mapping from the SaaS layer against the live runtime
- validated live provisioning-related calls from the SaaS layer
- broader pilot onboarding and go-live operations

Phase 17 prepares and stabilizes the ERP runtime. It does not complete live SaaS integration.

---

## 20. What remains for Phase 18

### Phase 18 — live SaaS ↔ ERPNext integration cutover

Still remains to be done:

- explicitly activate the live ERPNext client path
- validate tenant-to-site mapping against the deployed ERPNext environment
- validate live health/status calls from the SaaS backend
- validate low-risk provisioning-related calls against a real site
- confirm safe live-mode toggles, observability, and rollback behavior

---

## 21. Final operator-ready deliverables for this phase

Phase 17 should now be treated as complete when the repository contains or the operator team has:

- this step-by-step ERPNext deployment checklist
- a defined ERP VM preparation sequence
- a defined host layout
- a defined runtime installation path
- a defined demo-site and tenant-site creation process
- a defined custom app installation path
- a defined DNS and TLS plan
- a defined backup and restore drill
- a defined restart and rollback procedure
- explicit separation from Phase 18 live SaaS ↔ ERPNext cutover
