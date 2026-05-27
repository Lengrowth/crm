# 20 — Pilot Client Onboarding And First Go-Live

**Project:** SaaS-first ERPNext control platform  
**Audience:** founders, implementation leads, support staff, and operators  
**Last updated:** 2026-05-27

---

## 1. Purpose

This document defines the detailed execution plan for **Phase 20 — pilot client onboarding and first go-live**.

This phase is where the platform stops being only an internal build milestone and becomes a real client-delivery workflow.

The purpose of the phase is to onboard the **first real pilot customer** through the SaaS control plane, connect that customer to a real ERPNext tenant runtime, complete implementation tasks, and reach a controlled go-live with clear ownership and support.

---

## 2. Phase objective

By the end of Phase 20, the team should have proven that it can:

- create and manage a real customer organization in the SaaS layer
- create and configure the customer tenant correctly
- provision or link the corresponding ERPNext site
- apply the correct plan, modules, branding, and domain settings
- prepare users and initial data
- run training and validation
- execute go-live with a support plan
- document what must improve before broader rollout

This phase validates the end-to-end operating model, not just the software features.

---

## 3. Scope

### In scope

- pilot-customer readiness checklist
- organization and tenant setup
- plan/module assignment
- implementation project generation and tracking
- ERPNext site linkage or provisioning
- branding/domain setup
- initial user creation and access validation
- initial data preparation/import planning
- training and go-live checklist
- support and hypercare plan
- pilot success criteria and lessons learned

### Out of scope

- large-scale multi-client rollout automation
- fully self-service onboarding by customers
- advanced enterprise migration programs
- broad custom development outside the approved pilot scope

---

## 4. Dependencies and entry conditions

Do not start this phase until:

- the SaaS control plane is deployed and usable
- ERPNext runtime is deployed and stable
- live SaaS ↔ ERPNext integration path is understood
- backup and restore readiness is documented
- support and rollback expectations are defined
- the team has identified an actual pilot client or a realistic internal proxy

Recommended pre-pilot conditions:

- at least one demo tenant has already been tested end to end
- the implementation template for the pilot industry is reasonably mature
- the team knows which modules are included in the pilot scope
- legal/commercial expectations with the pilot client are understood

---

## 5. Pilot philosophy

The first client is not just another record in the system.

The pilot should be treated as:

- a product validation opportunity
- an operational rehearsal
- a support-process test
- a boundary test for what is and is not ready for broader rollout

The goal is not to pretend the system is perfect. The goal is to learn in a controlled way without creating chaos for the client or the team.

---

## 6. Pilot client selection criteria

Before onboarding, confirm the pilot client is appropriate.

### Good pilot characteristics

- willing to collaborate closely
- tolerant of an early-stage product with managed support
- has a contained implementation scope
- has a decision-maker available
- has realistic expectations about timeline and change
- matches the first vertical, such as drilling or field operations

### Risky pilot characteristics

- expects enterprise-scale customization immediately
- has unclear ownership on their side
- requires broad integration commitments before the core workflow is stable
- is unwilling to participate in validation and feedback loops

---

## 7. Pre-onboarding internal checklist

Before entering client data, the internal team should confirm:

- who owns the pilot implementation internally
- who owns technical operations internally
- who will support the client during go-live
- what modules are in scope
- what data the client must provide
- what training sessions are required
- what success looks like after go-live

### Internal ownership matrix

At minimum assign:

- implementation owner
- technical owner
- support owner
- client-side primary contact
- escalation contact

---

## 8. Organization setup in the SaaS layer

The pilot begins by creating the organization record correctly.

### Required organization data

Capture and validate:

- organization name
- legal name if relevant
- industry classification
- billing/admin contact details
- timezone
- country/region
- initial status (trial, active, pilot-specific state if used operationally)

### Quality rule

Do not treat organization setup as throwaway demo data. The first real client should start with clean metadata because later billing, support, and provisioning will depend on it.

---

## 9. Tenant setup in the SaaS layer

Once the organization exists, create the tenant record that will represent the client runtime.

### Required tenant data

Capture and confirm:

- tenant slug
- environment
- primary domain or planned domain
- ERP site linkage fields
- provisioning status
- implementation template reference

### Naming discipline

The tenant slug, domain, and ERP site name should align closely enough that support staff can identify the relationship immediately.

---

## 10. Plan and module assignment

The first pilot should not get an undefined package.

### Required decisions

Document clearly:

- which commercial plan the pilot is on
- whether billing is active, waived, manual, or deferred during pilot
- which modules are included
- which modules are explicitly out of scope

### Module-scope rule

Module sprawl is a major risk in early pilots. Be explicit about what the client is getting now versus later.

---

## 11. Implementation project generation

The implementation project is the operational control mechanism for the pilot.

### It should include

- project owner
- target go-live date
- implementation template used
- task list with statuses
- blockers and notes
- client dependencies

### Suggested default task groups

- company profile and branding collection
- user list collection
- roles and permissions setup
- customer data preparation
- supplier/item/material data preparation
- site/domain confirmation
- ERP validation tasks
- training sessions
- go-live approval

### Why this matters

Without a structured implementation project, the first pilot turns into ad hoc chat messages and forgotten setup steps.

---

## 12. ERPNext site provisioning or linkage

At this stage, the ERP runtime for the pilot must be created or linked deliberately.

### Required outcomes

The team should know:

- whether the site is newly provisioned or pre-created
- which environment the site belongs to
- the site URL
- the initial admin access plan
- whether custom app installation is required now

### Validation checklist

- site is reachable over HTTPS
- admin login works
- tenant metadata maps correctly to the site
- SaaS integration status reflects reality

---

## 13. Branding and domain setup

Even in a pilot, the client experience should feel coherent.

### Branding scope

Confirm:

- logo asset availability
- brand colors if supported
- tenant display name
- public-facing domain/subdomain choice
- any white-label expectations that are actually in scope

### Domain rule

If custom domain is not yet fully production-ready, communicate that clearly and use a stable platform-managed subdomain during pilot instead of improvising a fragile setup.

---

## 14. User setup and access validation

A pilot cannot succeed if the right people cannot log in.

### Required user setup

Prepare:

- internal admin/support users
- client admin users
- initial end-user roles if applicable
- access instructions
- password/reset or invite flow validation

### Access validation

Confirm that each critical user type can:

- log into the correct system
- reach the expected screens
- avoid access to restricted administrative areas

### Important distinction

SaaS user access and ERP tenant user access should remain conceptually separate. The onboarding plan must be clear about which credentials and interfaces apply to which system.

---

## 15. Initial data preparation and import planning

The first client often succeeds or fails based on initial data quality.

### Data categories to plan for

Depending on scope:

- customers
- suppliers
- items/materials
- equipment/assets
- crews/employees
- opening reference data
- branding/legal template assets

### Data-handling rule

Do not promise bulk import quality without validating source data first.

### Minimum import workflow

- identify required templates
- collect source files
- review data quality
- map fields
- test import on a non-production or controlled path if possible
- confirm post-import checks

---

## 16. Training readiness

Training should be part of the implementation plan, not an afterthought.

### Training should cover

- what the SaaS portal is for
- what ERPNext tenant site is for
- who uses which interface
- key daily workflows
- escalation/support path
- what is intentionally not part of the pilot yet

### Recommended training outputs

- agenda per role
- attendance list
- quick-start notes
- known limitations shared with the client honestly

---

## 17. Go-live checklist

Go-live should happen only when the minimum readiness threshold is met.

### Minimum go-live checks

- organization and tenant records are correct
- plan/modules are confirmed
- ERP site is reachable and validated
- required users can log in
- critical initial data is loaded or explicitly deferred
- training has been delivered
- support owner is assigned
- rollback/containment plan exists

### Go-live decision rule

If a critical dependency is unresolved, delay go-live rather than forcing it and creating avoidable trust damage.

---

## 18. Hypercare and support model

The first pilot needs heightened support after go-live.

### Hypercare expectations

Define:

- duration of hypercare window
- response-time expectations internally
- escalation path for SaaS issues
- escalation path for ERP/runtime issues
- how defects vs training questions are classified

### Support ownership

The client should know:

- where to report issues
- who is their main contact
- what information helps triage an issue quickly

---

## 19. Success criteria for the pilot

A pilot is complete only if it produces usable evidence.

### Suggested success indicators

- client can log in reliably
- client can perform the agreed core workflows
- implementation tasks are substantially complete
- support issues are manageable and understandable
- major architecture boundaries hold up in practice
- the team can repeat the onboarding path for the next client with fewer unknowns

### Suggested review topics after go-live

- what confused the client?
- what confused the internal team?
- what steps were manual but acceptable?
- what steps were too fragile to repeat?
- which product gaps blocked smooth adoption?

---

## 20. Lessons learned and post-pilot review

This phase should end with a structured internal review.

### Review areas

- SaaS onboarding flow quality
- ERP provisioning quality
- implementation template usefulness
- support burden
- documentation gaps
- architecture decisions that need revisiting
- backlog items required before additional clients

### Output expectation

The pilot should generate a concrete next-step list, not vague impressions.

---

## 21. Deliverables

This phase should produce:

- pilot organization and tenant setup
- confirmed plan and module scope
- implementation project and task tracking
- ERP site linkage/provisioning validation
- branding/domain setup decision record
- user setup and access validation
- data import plan or completion notes
- training checklist
- go-live checklist
- hypercare/support plan
- pilot success review notes

---

## 22. Exit criteria

Phase 20 is complete only when all of the following are true:

- a real pilot client has been onboarded through the defined process
- the client can access the agreed environment successfully
- the client can execute the agreed core workflows
- support ownership is active and understood
- implementation and go-live checklists are complete or consciously deferred with visibility
- the team has documented lessons learned for the next onboarding cycle

---

## 23. Risks and common failure points

Watch for:

- unclear pilot scope leading to endless “just one more thing” work
- weak distinction between SaaS portal responsibilities and ERP tenant responsibilities
- poor-quality source data causing avoidable onboarding delay
- training gaps being mistaken for product defects
- go-live happening before user access is truly validated
- lack of a named support owner during hypercare

---

## 24. What should happen after this phase

Once the first pilot is live, the team should decide deliberately whether the platform is ready for:

- a second pilot client
- a small rollout wave
- targeted product hardening only
- additional implementation-template maturity work
- broader automation for provisioning and onboarding

The most important output of Phase 20 is confidence grounded in real use, not just in internal optimism.
