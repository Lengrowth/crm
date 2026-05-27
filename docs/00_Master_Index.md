# Master Index

This repository is being built as a SaaS-first control platform that will later manage ERPNext/Frappe tenants.

## Core Reading Order

1. `08_SaaS_First_Master_Build_Documentation.md`
2. `09_AI_Build_Prompt_For_SaaS_First_ERPNext_Project.md`
3. `10_Phase_By_Phase_AI_Task_Prompts.md`
4. `15_Next_Phases_Production_Roadmap.md`
5. `16_SaaS_Control_Plane_Deployment_On_GCP.md`
6. `17_ERPNext_Deployment_On_GCP.md`
7. `18_Live_SaaS_ERPNext_Integration_Cutover.md`
8. `19_Operational_Hardening_And_Recovery_Readiness.md`
9. `20_Pilot_Client_Onboarding_And_First_Go_Live.md`
10. `21_GCP_SaaS_And_ERPNext_Deployment_Guide.md`
11. `02_ERPNext_SaaS_Product_Build_Runbook.md`
12. `03_ERPNext_Tenant_Provisioning_And_SaaS_Connection_Runbook.md`
13. `04_Drilling_ERPNext_Implementation_Blueprint.md`
14. `05_Custom_Frappe_App_Development_Runbook.md`

## Current Architecture

- Frontend: Next.js App Router in `/frontend`
- Backend: Python API in `/backend`
- Docs: `/docs`
- Deployment planning: `/infra`
- Helper scripts: `/scripts`

## Phase Summary Index

- `phase_summaries/00_Project_Initialization_Summary.md`
- `phase_summaries/01_Base_Repository_Structure_Summary.md`
- `phase_summaries/02_SaaS_Backend_Data_Model_And_Persistence_Summary.md`
- `phase_summaries/03_SaaS_Authentication_And_Authorization_Summary.md`
- `phase_summaries/04_Main_Website_And_Product_Shell_Summary.md`
- `phase_summaries/05_Organizations_And_Tenants_Management_Summary.md`
- `phase_summaries/06_Implementation_Project_Workflows_Summary.md`
- `phase_summaries/07_ERPNext_Integration_Summary.md`
- `phase_summaries/08_ERPNext_Provisioning_Summary.md`
- `phase_summaries/09_Billing_And_Subscriptions_Summary.md`
- `phase_summaries/10_WhiteLabel_and_Domain_Management.md`
- `phase_summaries/11_ERPNext_Integration_Maturation.md`
- `phase_summaries/12_Durable_Provisioning_Jobs.md`
- `phase_summaries/13_Billing_Provider_Integration.md`
- `phase_summaries/14_Pilot_Client_Onboarding.md`
- `phase_summaries/15_Production_Website_And_Readiness_Cleanup.md`
- `phase_summaries/16_SaaS_Control_Plane_Deployment_Readiness.md`
- `phase_summaries/17_ERPNext_Deployment_Readiness.md`

## Phase Sequence

Phase 00 confirms the architecture and documentation. Phase 01 creates the monorepo scaffold. Phase 02 adds the local SaaS persistence layer. Phase 03 adds local SaaS authentication and authorization. Phase 04 adds the main website and protected app shell. Phase 05 adds organization and tenant management. Phase 06 adds implementation workflows. Phase 07 adds the ERPNext abstraction layer. Phases 08 through 14 extend provisioning, billing, white-label, integration maturity, and pilot onboarding. Phase 15 makes the repository launch/demo-ready. Phase 16 prepares the SaaS control-plane deployment runbook and operator checklist on GCP. Phase 17 prepares and executes the ERPNext runtime deployment runbook on a separate GCP VM. Phase 18 performs the live SaaS-to-ERPNext cutover.