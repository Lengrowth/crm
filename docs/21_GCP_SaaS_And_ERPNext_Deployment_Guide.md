# 21 — GCP SaaS And ERPNext Deployment Guide

**Project:** SaaS-first ERPNext control platform
**Audience:** internal operators and implementers
**Last updated:** 2026-05-27

---

## 1. What this guide covers

This guide is the **high-level deployment map** for the full platform on Google Cloud.

It covers:

- the **SaaS control app** deployment
- the **ERPNext/Frappe runtime** deployment
- the separation between both systems
- the order you should follow so you do not mix phases

This guide is intentionally shorter than the phase runbooks.

Use these as the **primary step-by-step execution docs**:

- `docs/16_SaaS_Control_Plane_Deployment_On_GCP.md` → detailed SaaS VM runbook
- `docs/17_ERPNext_Deployment_On_GCP.md` → detailed ERPNext VM runbook
- `docs/18_Live_SaaS_ERPNext_Integration_Cutover.md` → live integration cutover

---

## 2. Recommended production layout

For the intended production-style deployment, use **two separate GCP VMs**.

### 2.1 SaaS application VM

Use one VM for the SaaS control plane.

This VM hosts:

- Next.js frontend
- FastAPI backend
- Nginx reverse proxy
- TLS/HTTPS
- deploy scripts and service definitions

Current planned SaaS hostnames:

- `crm.lenquant.com` → frontend
- `crm-api.lenquant.com` → backend

Suggested VM name:

- `saas-control-01`

### 2.2 ERPNext VM

Use one separate VM for ERPNext/Frappe.

This VM hosts:

- Docker / Compose runtime
- Frappe / ERPNext
- MariaDB
- Redis
- workers
- scheduler
- backups
- ERP web edge / HTTPS

Suggested VM name:

- `erpnext-01`

### 2.3 Why this split is recommended

- It keeps SaaS control-plane load separate from ERP tenant load.
- It makes troubleshooting easier.
- It reduces the chance that ERP maintenance affects the SaaS portal.
- It keeps the architecture boundary clear.

Do **not** put ERPNext on the same VM as the SaaS app for the planned deployment path unless you intentionally decide to run a short-lived internal demo with extra risk.

---

## 3. Deployment order

Follow this order exactly:

1. **Local readiness**
   - confirm frontend build/typecheck
   - confirm backend runtime endpoints
2. **Phase 16 — SaaS VM deployment**
   - deploy `crm.lenquant.com`
   - deploy `crm-api.lenquant.com`
   - verify HTTPS, health checks, and app routes
3. **Phase 17 — ERPNext VM deployment**
   - deploy ERPNext on a separate VM
   - create a demo site
   - verify backup and restore
4. **Phase 18 — Live cutover**
   - connect SaaS to the real ERPNext runtime intentionally
   - validate live health and provisioning-related paths

Do **not** combine Phases 16, 17, and 18 into one deployment session.

---

## 4. What is already fixed for this repository

These SaaS hostnames are now fixed in the deployment docs:

- `crm.lenquant.com`
- `crm-api.lenquant.com`

The ERPNext hostnames must **not** reuse the SaaS hostnames.

The detailed Phase 17 runbook now uses these concrete example ERP hostnames for the first deployment walkthrough:

- `demo-erp.lenquant.com`
- `champion.lenquant.com`

You can rename them later if you choose another tenant naming convention, but keep the SaaS and ERP hostnames clearly separated.

---

## 5. SaaS deployment summary

For the SaaS control plane:

- create one GCP VM
- reserve one static IP
- point both `crm.lenquant.com` and `crm-api.lenquant.com` to that IP
- install Python 3.11+, Node.js 20, Nginx, and the app runtimes
- run frontend on `127.0.0.1:3000`
- run backend on `127.0.0.1:8000`
- use Nginx and Certbot for HTTPS

Use the exact beginner runbook here:

- `docs/16_SaaS_Control_Plane_Deployment_On_GCP.md`

Important Python note:
- on newer Ubuntu images, use the VM's built-in `python3` if it is already `3.11+`
- do not force `python3.11` on hosts that already ship with a newer supported Python version

---

## 6. ERPNext deployment summary

For ERPNext:

- create a second GCP VM
- reserve a second static IP
- choose separate ERP hostnames
- install the ERP runtime on that VM
- create a demo site first
- create a repeatable tenant-site pattern second
- test backup and restore before live cutover

Use the exact ERP runbook here:

- `docs/17_ERPNext_Deployment_On_GCP.md`

---

## 7. Live cutover summary

Only after both VMs are stable:

- activate the live ERPNext client path intentionally
- verify tenant-to-site mapping
- verify live health/status calls
- verify controlled live provisioning-related flows
- confirm rollback behavior

Use:

- `docs/18_Live_SaaS_ERPNext_Integration_Cutover.md`

---

## 8. Minimal checklist before you begin GCP work

- [ ] local frontend and backend readiness checks passed
- [ ] you can log into GCP
- [ ] billing is enabled on the GCP project
- [ ] Compute Engine API is enabled
- [ ] you can edit DNS for `lenquant.com`
- [ ] you have production env values ready locally
- [ ] you understand there will be **two VMs**, not one

---

## 9. Final recommendation

If you are new to GCP, do **not** start with ERPNext first.

Start with the SaaS VM and follow:

- `docs/16_SaaS_Control_Plane_Deployment_On_GCP.md`

After that is stable, move to:

- `docs/17_ERPNext_Deployment_On_GCP.md`

After both are stable, use:

- `docs/18_Live_SaaS_ERPNext_Integration_Cutover.md`
