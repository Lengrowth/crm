# PLAT-P0 Decision, Blocker, and Risk Register

| ID | Type | Status | Owner | Required action |
|---|---|---|---|---|
| P0-D01 | Decision | Open | Delivery owner / acceptance authority | Record agreement, payment, commencement, and acceptance authority. |
| P0-B01 | Resolved | Codex / infrastructure owner | Read-only SSH access opened temporarily; EC2 as-built inventory completed and the temporary rule can be removed after review. |
| P0-B02 | Conditional | Infrastructure owner | ERP/control-plane backups are in private R2, byte-hash verified, and restored to disposable targets; assign retention/automation ownership and a second restore operator. |
| P0-B03 | Open | Platform owner | Production Frappe/ERPNext worktrees contain preserved drift and no remotes; clean pinned clones now exist locally, but publish `lenerp_core` to the approved private destination and prove install/migrate/list/uninstall on a disposable bench. |
| P0-B04 | Open | Platform owner | Create and prove isolated staging data/process/configuration/hostname lanes on the EC2. |
| P0-B05 | Mandatory pre-data blocker | Deferred by owner | Security/infrastructure owner | Rotate exposed credentials, remove plaintext secret handling, scan history, verify replacements, and enable least privilege/MFA before any Champion data. |
| P0-R01 | Risk | Open | Delivery owner | Temporary hostname may leak through cookies, callbacks, links, email, webhooks, monitoring, or ERP settings; complete the domain checklist. |
| P0-R02 | Risk | Open | Release owner | Database migrations and code rollback are different operations; complete restore/correction rehearsals. |
| P0-R03 | Risk | Open | Repository owner | Client-controlled private repository and infrastructure ownership are not yet evidenced. |
| P0-B06 | Blocker | Cloudflare/infrastructure owner | `api.lenerp.lengrowth.com` returns an edge TLS handshake failure; the connected Wrangler identity lacks zone DNS/SSL permissions needed to correct or verify the edge certificate/settings. |
| P0-R04 | Risk | Release owner | Production has no immutable `current`/`previous` release pointers, so the source commit is known but a code rollback target is not yet recorded. |
