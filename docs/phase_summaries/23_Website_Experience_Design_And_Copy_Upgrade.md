# Phase 23 — Website Experience, Design, And Copy Upgrade

## Date
2026-05-27

## Goal
Create a dedicated documentation package for a major public website redesign and content upgrade, separate from the core infrastructure and ERP integration phases.

## What changed

### New design strategy document
- Added `docs/23_Website_Experience_Design_And_Copy_Upgrade.md`.
- Defined the website redesign as a parallel product/brand workstream rather than a replacement for the next core runtime phase.

### Clarified what the next core phase is
- Kept the roadmap logic clear:
  - the next core platform phase is still `docs/18_Live_SaaS_ERPNext_Integration_Cutover.md`
  - the website redesign is a parallel execution track for product presentation and launch quality

### Website direction documented
- Captured the requested design ambition:
  - premium, memorable, startup-like public website
  - less text-heavy and more visually led
  - stronger spacing, hierarchy, and CTA clarity
- Documented the requested frontend direction:
  - Tailwind CSS
  - shadcn/ui selectively
  - Lucide-style icons and a cleaner icon vocabulary
  - icon-based Sun / Moon theme toggle instead of text labels
  - Zinc-based dark mode surfaces and contrast
- Documented the requested quality improvements:
  - stronger homepage hero with a clear primary button
  - interactive or animated hero background treatment
  - more varied section layouts instead of repeated card grids
  - animations and hover interactions that feel polished, not gimmicky
  - real end-user copy instead of scaffold copy

### Implementation structure
- Added page-by-page guidance for:
  - homepage
  - pricing
  - demo
  - contact
  - modules
  - industries
  - drilling
  - login
- Added section-level design and copy guidance for each page.
- Added component-system direction and phased implementation order.

### Master index sync
- Updated `docs/00_Master_Index.md` to include the new website design/copy document.

## Validation run
- No code validation was run.
- This was a documentation-only refinement.

## What remains for later phases

### Core platform work
- Phase 18 live SaaS ↔ ERPNext integration cutover still remains the next core platform phase.

### Website execution work
- no frontend implementation has been performed yet for the new design direction
- no copy rewrite has been applied yet from this new design document
- no shadcn/ui or icon-system integration has been executed yet from this document
