# 17 — ERPNext Deployment On GCP

**Project:** SaaS-first ERPNext control platform  
**Audience:** infrastructure operators, implementation leads, and technical admins  
**Status:** planning and readiness runbook only  
**Last updated:** 2026-05-27

---

## 1. Purpose

This document is the **exact beginner-friendly deployment runbook** for **ERPNext/Frappe as the external tenant runtime** on Google Cloud Platform.

It is written for a deployment model where:

- the SaaS control plane already lives on its own VM
- ERPNext is deployed on a **second separate VM**
- the ERP VM uses Docker / Docker Compose
- you create a **demo ERP site first**
- you create the **first tenant site second**

This document covers:

- creating the ERPNext VM on GCP
- attaching a static IP
- opening the correct firewall ports
- setting up DNS for the ERP VM
- installing Docker and Compose
- cloning and configuring the Frappe Docker runtime
- starting the ERPNext stack
- creating a demo ERP site
- creating the first tenant ERP site
- validating DNS, HTTPS, backup, and restart behavior

This document does **not** cover:

- SaaS control-plane deployment work from Phase 16
- live SaaS ↔ ERPNext integration cutover from Phase 18
- self-service tenant provisioning from the SaaS UI
- Kubernetes, autoscaling, HA, or multi-node ERP clustering
- production secrets in git

---

## 2. Final target for this phase

At the end of Phase 17, the target is:

- **one dedicated GCP VM** for ERPNext/Frappe
- **one static public IP** attached to that ERP VM
- Docker / Compose running the ERPNext runtime
- one demo ERP site running over HTTPS
- one first tenant ERP site pattern documented and validated
- a basic backup path validated
- a basic restore drill documented and operator-controlled

### Important boundary

This VM is for ERPNext/Frappe only.

It must remain separate from the SaaS VM that serves:

- `crm.lenquant.com`
- `crm-api.lenquant.com`

Phase 17 is **ERP runtime deployment only**. It is **not** the live cutover phase.

---

## 3. Example ERP hostnames for this runbook

To make this runbook concrete, use these example ERP hostnames:

- `demo-erp.lenquant.com` → demo ERPNext site
- `champion.lenquant.com` → first tenant ERPNext site

You can rename these later if you choose another convention, but use these throughout the runbook unless you intentionally substitute your own values everywhere.

### Why these names are recommended

- they do **not** overlap with the SaaS domains
- they make the SaaS/ERP boundary obvious
- they are easy to map later during Phase 18

---

## 4. Before you start

Do not start Phase 17 until all of these are true:

- [ ] Phase 16 SaaS deployment is already working or nearly complete.
- [ ] You understand there will be **two VMs**, not one.
- [ ] You can log into GCP.
- [ ] You can edit DNS for `lenquant.com` or you know who can.
- [ ] You understand that Phase 17 deploys ERPNext only.
- [ ] You understand that Phase 18 will later connect SaaS to ERPNext.
- [ ] You have decided to use these initial ERP hostnames:
  - `demo-erp.lenquant.com`
  - `champion.lenquant.com`
- [ ] You have a safe place ready for ERP credentials and passwords outside git.

---

## 5. GCP overview for beginners

The main GCP Console places you will use are:

- **Project selector** → top header bar
- **Navigation menu** → top-left hamburger menu
- **Billing**
- **APIs & Services > Library**
- **VPC network > IP addresses**
- **VPC network > Firewall**
- **Compute Engine > VM instances**
- **Cloud Storage > Buckets**
- **Network Services > Cloud DNS** if you use Cloud DNS

When this doc says **Navigation menu > X > Y**, that means:

1. click the hamburger icon
2. click the main section
3. click the submenu item

---

## 6. Exact GCP setup steps

---

### Step 1 — Create or select the correct GCP project

1. Open the Google Cloud Console.
2. Click the **project selector** in the top bar.
3. Select the correct production project.
4. If it does not exist yet:
   - click **New Project**
   - enter a name such as `lenquant-production`
   - click **Create**
5. Switch into that project.

### Step 2 — Attach billing

1. Open **Navigation menu > Billing**.
2. Confirm billing is attached to the project.
3. If not, attach the correct billing account.

### Step 3 — Enable required APIs

1. Open **Navigation menu > APIs & Services > Library**.
2. Enable these APIs:
   - **Compute Engine API**
   - **Cloud Storage API**
3. Optional but useful:
   - **Cloud DNS API**
   - **Cloud Monitoring API**
   - **Cloud Logging API**

### Step 4 — Reserve a static public IP for the ERP VM

1. Open **Navigation menu > VPC network > IP addresses**.
2. Click **Reserve external static address**.
3. Fill in:
   - **Name:** `erpnext-runtime-ip`
   - **Network service tier:** `Premium`
   - **IP version:** `IPv4`
   - **Type:** `Regional`
   - **Region:** choose the same region you will use for the ERP VM
4. Click **Reserve**.
5. Write down the IP address. You will use it in DNS.

### Step 5 — Create a Cloud Storage bucket for ERP backups

This is recommended before you bring the ERP runtime live.

1. Open **Navigation menu > Cloud Storage > Buckets**.
2. Click **Create**.
3. Use a bucket name that is globally unique, for example:
   - `lenquant-erpnext-backups-prod`
4. Keep the bucket in the same region as the ERP VM if possible.
5. Finish bucket creation.
6. Write down the bucket name.

### Step 6 — Create the ERP VM

1. Open **Navigation menu > Compute Engine > VM instances**.
2. Click **Create Instance**.
3. Use these recommended values.

#### Basic configuration
- **Name:** `erpnext-01`
- **Region:** same region you used for the static IP
- **Zone:** any zone in that region

#### Machine configuration
- **Series:** `E2`
- **Machine type:** `e2-standard-4`
  - 4 vCPU
  - 16 GB RAM

This is a good starting point for:
- the demo ERP site
- the first tenant site
- Docker, MariaDB, Redis, workers, and scheduler

#### Boot disk
- click **Change** under **Boot disk**
- choose:
  - **Operating system:** `Ubuntu`
  - **Version:** `Ubuntu 24.04 LTS` or current Ubuntu LTS image available in GCP
  - **Boot disk type:** `Balanced persistent disk`
  - **Size:** `150 GB` minimum
- click **Select**

#### Firewall checkboxes
You can check these if you want:
- **Allow HTTP traffic**
- **Allow HTTPS traffic**

But do **not** rely on those checkboxes alone. This runbook will still create explicit firewall rules in the next step.

#### Networking
1. Expand **Networking**.
2. Under **Network interfaces**, use the default interface.
3. For **External IPv4 address**, select:
   - `erpnext-runtime-ip`
4. Save the network interface.

#### Finish
1. Review the settings.
2. Click **Create**.
3. Wait until the VM is running.

### Step 7 — Create explicit ERP firewall rules

Create these rules even if you already checked the HTTP/HTTPS checkboxes during VM creation.

#### Rule 1 — Allow HTTP
1. Open **Navigation menu > VPC network > Firewall**.
2. Click **Create firewall rule**.
3. Use:
   - **Name:** `allow-erp-http`
   - **Network:** `default` unless you intentionally use another network
   - **Direction of traffic:** `Ingress`
   - **Action on match:** `Allow`
   - **Targets:** `All instances in the network`
   - **Source IPv4 ranges:** `0.0.0.0/0`
   - **Protocols and ports:** `tcp:80`
4. Click **Create**.

#### Rule 2 — Allow HTTPS
Create another rule:
- **Name:** `allow-erp-https`
- **Network:** same network
- **Direction:** `Ingress`
- **Action:** `Allow`
- **Targets:** `All instances in the network`
- **Source IPv4 ranges:** `0.0.0.0/0`
- **Protocols and ports:** `tcp:443`

Click **Create**.

#### Rule 3 — SSH
If you already have a working SSH rule for your admin IP, keep it.
If not, create a restricted SSH rule for your public IP instead of leaving SSH open globally.

### Step 8 — Connect to the ERP VM using browser SSH

1. Go back to **Compute Engine > VM instances**.
2. Find `erpnext-01`.
3. Click **SSH**.
4. A browser terminal should open.

---

## 7. DNS setup for ERP hostnames

For this runbook, use:

- `demo-erp.lenquant.com`
- `champion.lenquant.com`

### Step 9 — Create the first ERP DNS record

Before the demo site can receive HTTPS, `demo-erp.lenquant.com` must point to the ERP VM IP.

#### Option A — DNS managed outside GCP
At your DNS provider, create:

| Type | Host | Value |
| --- | --- | --- |
| A | `demo-erp` | `YOUR_ERP_STATIC_IP` |

Save the record.

#### Option B — Cloud DNS
If you use Cloud DNS, add:

- `demo-erp.lenquant.com.` → A → `YOUR_ERP_STATIC_IP`

### Step 10 — Verify DNS for the demo hostname

From your local computer:

```powershell
nslookup demo-erp.lenquant.com
```

Expected:
- it resolves to the ERP VM static IP

Do **not** move to HTTPS testing until DNS resolves correctly.

---

## 8. Prepare the ERP VM runtime

Run the following commands inside the browser SSH terminal on the ERP VM.

### Step 11 — Update the host

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 12 — Install base packages

```bash
sudo apt install -y git curl unzip jq docker.io docker-compose-v2
```

### Step 13 — Enable Docker and add your user to the docker group

```bash
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

Then start a new shell group session without fully logging out:

```bash
newgrp docker
```

### Step 14 — Verify Docker

```bash
docker --version
docker compose version
```

If `docker compose version` works, the Compose plugin is installed correctly.

---

## 9. Create the ERP host layout

### Step 15 — Create directories

```bash
sudo mkdir -p /opt/erpnext-runtime/runtime
sudo mkdir -p /opt/erpnext-runtime/shared/config
sudo mkdir -p /opt/erpnext-runtime/shared/logs
sudo mkdir -p /opt/erpnext-runtime/shared/backups
sudo mkdir -p /opt/erpnext-runtime/shared/compose
sudo mkdir -p /opt/erpnext-runtime/scripts
sudo chown -R $USER:$USER /opt/erpnext-runtime
```

Expected layout:

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

---

## 10. Clone the Frappe Docker runtime

### Step 16 — Clone the Frappe Docker repository

```bash
git clone https://github.com/frappe/frappe_docker.git /opt/erpnext-runtime/runtime/frappe_docker
```

### Step 17 — Move into the runtime directory

```bash
cd /opt/erpnext-runtime/runtime/frappe_docker
```

### Important note

Do **not** use disposable demo files like `pwd.yml` for the intended production-style path.
Use:

- `compose.yaml`
- `overrides/compose.mariadb.yaml`
- `overrides/compose.redis.yaml`
- `overrides/compose.https.yaml`

---

## 11. Create the ERP runtime `.env` file

### Step 18 — Create the shared ERP env file

```bash
nano /opt/erpnext-runtime/shared/config/frappe.env
```

Paste this template and replace the placeholder values with your own real values:

```dotenv
ERPNEXT_VERSION=v16.19.1
DB_PASSWORD=REPLACE_WITH_LONG_RANDOM_DB_PASSWORD
GUNICORN_THREADS=4
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=120
LETSENCRYPT_EMAIL=REPLACE_WITH_YOUR_EMAIL
HTTP_PUBLISH_PORT=80
HTTPS_PUBLISH_PORT=443
SITES_RULE=Host(`demo-erp.lenquant.com`)
```

### Important notes

- Do **not** commit this file into git.
- `DB_PASSWORD` should be long and random.
- `LETSENCRYPT_EMAIL` should be a real email you control.
- Start with `SITES_RULE=Host(`demo-erp.lenquant.com`)` only.
- You will update `SITES_RULE` later when adding `champion.lenquant.com`.

### Step 19 — Link that env file into the Frappe Docker runtime

```bash
ln -sf /opt/erpnext-runtime/shared/config/frappe.env /opt/erpnext-runtime/runtime/frappe_docker/.env
```

### Step 20 — Verify the symlink exists

```bash
ls -la /opt/erpnext-runtime/runtime/frappe_docker/.env
```

---

## 12. Start the ERP runtime stack

### Step 21 — Start the stack

From inside `/opt/erpnext-runtime/runtime/frappe_docker`, run:

```bash
docker compose \
  -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  -f overrides/compose.https.yaml \
  up -d
```

### Step 22 — Check container status

```bash
docker compose ps
```

Expected services should include the main runtime components such as:
- frontend
- backend
- websocket
- scheduler
- queue workers
- mariadb
- redis

### Step 23 — Check logs if something failed

```bash
docker compose logs -f --tail=100
```

Press `Ctrl+C` when finished viewing logs.

### Step 24 — Check that Docker is listening on HTTP/HTTPS

```bash
sudo ss -tulpn | grep -E ':80|:443'
```

Expected:
- something is listening on port 80
- something is listening on port 443 once HTTPS is configured by the stack

---

## 13. Create the demo ERP site

The demo site comes first.

### Step 25 — Create the demo site

Run:

```bash
docker compose exec backend bench new-site demo-erp.lenquant.com \
  --admin-password 'REPLACE_DEMO_ADMIN_PASSWORD' \
  --db-root-password 'REPLACE_WITH_THE_SAME_DB_PASSWORD' \
  --install-app erpnext
```

### Step 26 — Run migrate and clear caches

```bash
docker compose exec backend bench --site demo-erp.lenquant.com migrate
docker compose exec backend bench --site demo-erp.lenquant.com clear-cache
docker compose exec backend bench --site demo-erp.lenquant.com clear-website-cache
```

### Step 27 — Wait for HTTPS to settle

Because `demo-erp.lenquant.com` is already in DNS and `SITES_RULE`, the Traefik/HTTPS flow should now be able to issue the certificate.

### Step 28 — Test the demo site in the browser

Open:

- `https://demo-erp.lenquant.com`

Expected:
- valid certificate
- ERPNext login screen loads
- no certificate warning

### Step 29 — Test the demo site from the VM

```bash
curl -I http://demo-erp.lenquant.com
curl -k -I https://demo-erp.lenquant.com
```

### Step 30 — Demo-site operator checklist

Confirm:

- [ ] DNS resolves to the ERP VM IP
- [ ] HTTPS works
- [ ] Administrator login works
- [ ] ERPNext base app is installed
- [ ] `docker compose ps` is healthy

---

## 14. Create the first tenant ERP site

Do this only after the demo site works.

### Step 31 — Create the tenant DNS record

At your DNS provider or Cloud DNS, create:

| Type | Host | Value |
| --- | --- | --- |
| A | `champion` | `YOUR_ERP_STATIC_IP` |

Then verify from your local computer:

```powershell
nslookup champion.lenquant.com
```

### Step 32 — Update `SITES_RULE` to include both demo and tenant site

Edit the shared env file:

```bash
nano /opt/erpnext-runtime/shared/config/frappe.env
```

Change:

```dotenv
SITES_RULE=Host(`demo-erp.lenquant.com`)
```

To:

```dotenv
SITES_RULE=Host(`demo-erp.lenquant.com`) || Host(`champion.lenquant.com`)
```

Save the file.

### Step 33 — Recreate the stack so the routing rule updates

```bash
cd /opt/erpnext-runtime/runtime/frappe_docker
docker compose \
  -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  -f overrides/compose.https.yaml \
  up -d
```

### Step 34 — Create the first tenant site

```bash
docker compose exec backend bench new-site champion.lenquant.com \
  --admin-password 'REPLACE_CHAMPION_ADMIN_PASSWORD' \
  --db-root-password 'REPLACE_WITH_THE_SAME_DB_PASSWORD' \
  --install-app erpnext
```

### Step 35 — Run migrate and clear caches for the tenant site

```bash
docker compose exec backend bench --site champion.lenquant.com migrate
docker compose exec backend bench --site champion.lenquant.com clear-cache
docker compose exec backend bench --site champion.lenquant.com clear-website-cache
```

### Step 36 — Test the tenant site

Open:

- `https://champion.lenquant.com`

Expected:
- valid certificate
- login page loads
- first tenant admin can log in

### Step 37 — Tenant-site operator checklist

Confirm:

- [ ] DNS resolves
- [ ] HTTPS works
- [ ] site loads and logs in
- [ ] the naming pattern is documented
- [ ] future tenant creation steps are now repeatable

---

## 15. Optional custom app installation path

If your custom Frappe app exists later, document and use a predictable install path.

### Step 38 — Example install shape for a custom app

Only do this if the custom app actually exists in the runtime.

```bash
docker compose exec backend bench --site champion.lenquant.com install-app YOUR_CUSTOM_APP_NAME
docker compose exec backend bench --site champion.lenquant.com migrate
```

### Record these decisions

- where the app source comes from
- how it is added to the runtime
- which sites should have it installed
- how updates are applied later

---

## 16. Backup setup and validation

Do not skip this.

### Step 39 — Create a manual backup of the demo site

```bash
cd /opt/erpnext-runtime/runtime/frappe_docker
docker compose exec backend bench --site demo-erp.lenquant.com backup --with-files
```

### Step 40 — Locate the backup files

Run:

```bash
find sites/demo-erp.lenquant.com -path '*private/backups*' -type f | sort | tail -n 20
```

You should see recent backup files under the demo site's backup folder.

### Step 41 — Optional: back up all sites

```bash
docker compose exec backend bench --site all backup --with-files
```

### Step 42 — Remote backup recommendation

Before real client onboarding, you should copy backup artifacts to your Cloud Storage bucket.

If you later install and configure `gcloud` on the VM with bucket access, the upload shape is:

```bash
gcloud storage cp -r sites/demo-erp.lenquant.com/private/backups gs://YOUR_BACKUP_BUCKET/manual/demo-erp/
```

If `gcloud` is not installed yet, at minimum complete the local backup validation first and document the remote upload as a required follow-up before paid clients.

---

## 17. Restore drill guidance

Keep this operator-controlled.

### Goal of the first restore drill

- prove you know where the backup files are
- prove you know which site the backup belongs to
- prove you can restore in a controlled non-production way

### Recommended restore drill approach

Use a temporary restore-check site instead of overwriting the demo site immediately.

### Step 43 — Create a temporary restore-check site

```bash
docker compose exec backend bench new-site restore-check.lenquant.local \
  --admin-password 'REPLACE_TEMP_ADMIN_PASSWORD' \
  --db-root-password 'REPLACE_WITH_THE_SAME_DB_PASSWORD'
```

### Step 44 — Identify the latest backup artifact names

Run:

```bash
find sites/demo-erp.lenquant.com -path '*private/backups*' -type f | sort | tail -n 10
```

### Step 45 — Restore drill command shape

The exact restore filenames depend on the backup files that were generated.

Use the backup file paths you found in the previous step. The command shape is:

```bash
docker compose exec backend bench --site restore-check.lenquant.local restore /PATH/TO/DATABASE.sql.gz \
  --with-private-files /PATH/TO/private-files.tar \
  --with-public-files /PATH/TO/files.tar
```

### Step 46 — Restore drill validation checklist

After the restore drill, confirm:

- [ ] the temporary restore-check site exists
- [ ] restore command completed without error
- [ ] the site can be migrated if required
- [ ] admin login works on the restored data set
- [ ] the exact restore steps are written down

### Important restore note

Do not perform destructive restore operations casually against the real demo or client site during the first production-style deployment.

---

## 18. Restart procedure

Use this after env changes, runtime changes, or host reboot.

### Step 47 — Restart the ERP runtime stack

```bash
cd /opt/erpnext-runtime/runtime/frappe_docker
docker compose \
  -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  -f overrides/compose.https.yaml \
  restart
```

### Step 48 — Check health after restart

```bash
docker compose ps
docker compose logs --tail=100
```

### Step 49 — Re-test demo and tenant URLs

Open:

- `https://demo-erp.lenquant.com`
- `https://champion.lenquant.com`

---

## 19. Rollback basics

If a runtime change breaks ERPNext:

1. stop and inspect logs
2. restore the last known-good runtime config
3. restart the stack
4. retest demo and tenant sites
5. if needed, restore from a verified backup

### Minimum rollback triggers

Rollback if:
- demo site is down
- tenant site is down
- HTTPS is broken
- workers or scheduler stay unhealthy
- you lose confidence in runtime state after a change

---

## 20. What is still not done after this doc

Even after following this document, the following work is still outside Phase 17:

- live SaaS ↔ ERPNext integration cutover
- activation of the live ERPNext client path from the SaaS backend
- tenant-to-site mapping validation from the SaaS layer
- live provisioning-related calls from the SaaS backend
- pilot-client onboarding and go-live operations

---

## 21. Quick reference checklist

### GCP Console clicks

- Project selector → choose project
- Navigation menu > Billing
- Navigation menu > APIs & Services > Library
- Navigation menu > VPC network > IP addresses
- Navigation menu > VPC network > Firewall
- Navigation menu > Compute Engine > VM instances
- Navigation menu > Cloud Storage > Buckets
- Navigation menu > Network Services > Cloud DNS

### Example ERP hostnames used in this runbook

- `demo-erp.lenquant.com`
- `champion.lenquant.com`

### Main ERP VM paths

- `/opt/erpnext-runtime/runtime/frappe_docker`
- `/opt/erpnext-runtime/shared/config/frappe.env`
- `/opt/erpnext-runtime/shared/backups`

### Main runtime start command

```bash
docker compose \
  -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  -f overrides/compose.https.yaml \
  up -d
```

### Main site-creation commands

```bash
docker compose exec backend bench new-site demo-erp.lenquant.com --admin-password 'REPLACE_DEMO_ADMIN_PASSWORD' --db-root-password 'REPLACE_WITH_THE_SAME_DB_PASSWORD' --install-app erpnext
```

```bash
docker compose exec backend bench new-site champion.lenquant.com --admin-password 'REPLACE_CHAMPION_ADMIN_PASSWORD' --db-root-password 'REPLACE_WITH_THE_SAME_DB_PASSWORD' --install-app erpnext
```

### Main verification URLs

- `https://demo-erp.lenquant.com`
- `https://champion.lenquant.com`
