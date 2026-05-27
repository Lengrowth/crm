# SaaS-First ERPNext/Frappe Build Documentation Pack

Created: 2026-05-22

This pack adds the missing SaaS-first build direction.

## Files

1. `08_SaaS_First_Master_Build_Documentation.md`
   - The master phased build plan.
   - Explains SaaS first, ERPNext second.
   - Defines models, routes, backend endpoints, and phase order.

2. `09_AI_Build_Prompt_For_SaaS_First_ERPNext_Project.md`
   - Main prompt to paste into another AI coding session.
   - Tells the AI how to start with Next.js frontend and Python backend.
   - Restricts the AI to Phase 00 and Phase 01 first.

3. `10_Phase_By_Phase_AI_Task_Prompts.md`
   - Individual prompts for each phase.
   - Use one phase at a time.

## Recommended usage

Start with:

1. Feed the AI documents 01–08.
2. Paste `09_AI_Build_Prompt_For_SaaS_First_ERPNext_Project.md`.
3. Ask it to implement Phase 00 and Phase 01 only.
4. Review the result.
5. Then use `10_Phase_By_Phase_AI_Task_Prompts.md` phase by phase.

## Important rule

Do not start with ERPNext infrastructure.

Build the SaaS control layer first, then connect ERPNext/Frappe later.
