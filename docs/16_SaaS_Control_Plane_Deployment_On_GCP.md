# 16 — SaaS Control-Plane Deployment On GCP

**Project:** SaaS-first ERPNext control platform  
**Audience:** internal operators, technical founders, and implementation leads  
**Status:** planning and readiness runbook only  
**Last updated:** 2026-05-27

---

## 1. Purpose

This document is the **exact beginner-friendly deployment runbook** for the **SaaS control plane only** on Google Cloud Platform.

It is written for the current planned production-style SaaS hostnames:

- `crm.lenquant.com` → Next.js frontend
- `crm-api.lenquant.com` → FastAPI backend

This document covers:

- creating the GCP VM for the SaaS control plane
- attaching a static IP
- setting up DNS for `crm.lenquant.com` and `crm-api.lenquant.com`
- installing the frontend and backend runtimes
- using the VM's built-in `python3` when it is already `3.11+`
- configuring `systemd`
- configuring Nginx
- enabling HTTPS with Let's Encrypt
- validating health checks and smoke tests
- restart and rollback basics

This document does **not** cover:

- ERPNext/Frappe deployment
- live SaaS ↔ ERPNext cutover
- production secrets in git
- Kubernetes, autoscaling, HA, or multi-region design

---

## 2. Final target for this phase

At the end of Phase 16, the target is:

- **one GCP VM** for the SaaS control plane
- **one static public IP** attached to that VM
- `crm.lenquant.com` pointing to that VM
- `crm-api.lenquant.com` pointing to that VM
- Nginx serving both hostnames over HTTPS
- frontend process listening only on `127.0.0.1:3000`
- backend process listening only on `127.0.0.1:8000`

### Important boundary

This VM is for the SaaS app only.

ERPNext should be deployed later on a **separate VM** in Phase 17.

---

## 3. Before you start

Do not start the GCP steps until all of these are true:

- [ ] The frontend builds locally.
- [ ] The backend starts locally.
- [ ] You have read:
  - `docs/15_Next_Phases_Production_Roadmap.md`
  - `docs/16_SaaS_Control_Plane_Deployment_On_GCP.md`
  - `docs/17_ERPNext_Deployment_On_GCP.md`
  - `docs/18_Live_SaaS_ERPNext_Integration_Cutover.md`
- [ ] You understand that this phase deploys only the SaaS control plane.
- [ ] You have your production environment variable values ready locally.
- [ ] You can log into GCP.
- [ ] You can edit DNS for `lenquant.com` or you know who can.

### Local validation already expected before this phase

At minimum, confirm these backend endpoints locally:

- `GET /`
- `GET /health`
- `GET /integrations/erpnext/runtime`

And these frontend routes:

- `/`
- `/pricing`
- `/contact`
- `/demo`
- `/login`
- `/app`
- `/app/organizations`
- `/app/tenants`
- `/app/settings`

---

## 4. GCP overview for beginners

If you are new to GCP, these are the main places you will use in the Console:

- **Project selector** → top header bar
- **Navigation menu** → top-left hamburger menu
- **Billing** → attach billing to the project
- **APIs & Services > Library** → enable APIs
- **Compute Engine > VM instances** → create the VM
- **VPC network > IP addresses** → reserve a static IP
- **VPC network > Firewall** → check firewall rules if needed
- **Network Services > Cloud DNS** → only if you use Cloud DNS for `lenquant.com`

When this doc says **Navigation menu > X > Y**, that means:

1. click the hamburger icon in the top-left
2. click the main section
3. click the submenu item

---

## 5. Exact GCP setup steps

---

### Step 1 — Create or select the correct GCP project

1. Open the Google Cloud Console.
2. In the top bar, click the **project selector**.
3. If you already have the correct project, select it.
4. If not:
   - click **New Project**
   - enter a project name such as `lenquant-production`
   - choose the billing account if prompted
   - click **Create**
5. Wait until the project is ready and switch into it.

### Step 2 — Attach billing

1. Open **Navigation menu > Billing**.
2. If billing is not already linked:
   - click **Manage billing accounts** or **Link a billing account**
   - attach the correct billing account to this project
3. Confirm the project now shows billing enabled.

### Step 3 — Enable required APIs

1. Open **Navigation menu > APIs & Services > Library**.
2. Search for and enable these APIs:
   - **Compute Engine API**
   - **Cloud Resource Manager API**
3. Optional later APIs you may also enable, but are not required for this Phase 16 checklist:
   - **Cloud DNS API**
   - **Cloud Storage API**
   - **Cloud Monitoring API**

### Step 4 — Reserve a static public IP

Do this before creating DNS records.

1. Open **Navigation menu > VPC network > IP addresses**.
2. Click **Reserve external static address**.
3. Fill in:
   - **Name:** `saas-control-ip`
   - **Network service tier:** `Premium`
   - **IP version:** `IPv4`
   - **Type:** `Regional`
   - **Region:** choose the same region you plan to use for the VM
4. Click **Reserve**.
5. Write down the reserved IP address. You will use it in DNS.

### Step 5 — Create the SaaS VM

1. Open **Navigation menu > Compute Engine > VM instances**.
2. Click **Create Instance**.
3. Use these recommended values:

#### Basic configuration
- **Name:** `saas-control-01`
- **Region:** choose a region close to your expected users
- **Zone:** any zone in that region, for example `europe-west1-b` or similar

#### Machine configuration
- **Series:** `E2`
- **Machine type:** `e2-standard-2`
  - 2 vCPU
  - 8 GB memory

This is a good simple starting size for the SaaS control plane.

#### OS and storage
- Click **Change** under **Boot disk**
- Choose:
  - **Operating system:** `Ubuntu`
  - **Version:** `Ubuntu 22.04 LTS`
  - **Boot disk type:** `Balanced persistent disk`
  - **Size:** `30 GB` minimum
- Click **Select**

#### Firewall
Check these boxes:
- **Allow HTTP traffic**
- **Allow HTTPS traffic**

#### Networking
1. Expand **Networking** if needed.
2. Under **Network interfaces**, choose the default interface.
3. For **External IPv4 address**, select the reserved IP:
   - `saas-control-ip`
4. Save the network interface settings.

#### Finish
1. Review the VM details.
2. Click **Create**.
3. Wait for the VM status to become running.

### Step 6 — Connect to the VM using browser SSH

1. Stay in **Compute Engine > VM instances**.
2. Find `saas-control-01`.
3. Click the **SSH** button in the row.
4. A browser terminal window should open.

If browser SSH does not work, you may need to finish GCP OS Login or SSH-key setup. For a first deployment, browser SSH is the easiest starting point.

---

## 6. DNS setup for `lenquant.com`

You now need both SaaS hostnames to point to the SaaS VM static IP.

Required records:

- `crm.lenquant.com` → SaaS VM IP
- `crm-api.lenquant.com` → SaaS VM IP

You have two common options.

---

### Option A — Your DNS is managed outside GCP

If your domain is managed at Namecheap, GoDaddy, Cloudflare, or another registrar/DNS provider:

1. Log into that provider.
2. Open the DNS management page for `lenquant.com`.
3. Create these **A** records:

| Type | Host | Value |
| --- | --- | --- |
| A | `crm` | `YOUR_SAAS_STATIC_IP` |
| A | `crm-api` | `YOUR_SAAS_STATIC_IP` |

4. Save the records.
5. Wait for propagation.

---

### Option B — You want to use Cloud DNS in GCP

Only do this if you are actually moving authoritative DNS into GCP.

1. Open **Navigation menu > Network Services > Cloud DNS**.
2. Click **Create zone**.
3. Enter:
   - **Zone type:** `Public`
   - **Zone name:** `lenquant-com`
   - **DNS name:** `lenquant.com.`
   - **Description:** `Lenquant public DNS`
4. Click **Create**.
5. Open the zone and click **Add standard**.
6. Add these records:

#### Record 1
- **DNS name:** `crm.lenquant.com.`
- **Resource record type:** `A`
- **TTL:** `300`
- **IPv4 address:** `YOUR_SAAS_STATIC_IP`

#### Record 2
- **DNS name:** `crm-api.lenquant.com.`
- **Resource record type:** `A`
- **TTL:** `300`
- **IPv4 address:** `YOUR_SAAS_STATIC_IP`

7. Save both records.
8. Copy the Cloud DNS nameservers shown for the zone.
9. Go to your domain registrar and replace the current nameservers with the Cloud DNS nameservers.
10. Wait for propagation.

---

### Step 7 — Verify DNS from your local computer

On Windows PowerShell or Command Prompt, run:

```powershell
nslookup crm.lenquant.com
nslookup crm-api.lenquant.com
```

Expected result:
- both hostnames resolve to the same SaaS VM static IP

If you have `dig` available:

```bash
dig crm.lenquant.com +short
dig crm-api.lenquant.com +short
```

Do not move to TLS setup until both names resolve correctly.

---

## 7. Prepare the VM runtime

From the browser SSH terminal connected to the VM, run these commands.

### Step 8 — Update the host

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 9 — Install base packages

```bash
sudo apt install -y git curl nginx software-properties-common build-essential
```

### Step 10 — Install Python support

This project requires **Python 3.11 or newer**.

If the VM already has `python3` at version `3.11+`, use the built-in Python and do **not** force-install `python3.11`.

On newer Ubuntu images such as Ubuntu 26.04, this is the correct approach.

Run:

```bash
sudo apt install -y python3 python3-venv python3-pip
```

Verify:

```bash
python3 --version
```

Expected result:
- `Python 3.11.x` or newer is acceptable
- `Python 3.14.x` on Ubuntu 26.04 is acceptable

If `python3 --version` is lower than `3.11`, stop and install a newer Python version before continuing.

### Step 11 — Install Node.js 20

The frontend uses Next.js 15, so install a modern Node version.

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

Verify:

```bash
node --version
npm --version
nginx -v
```

---

## 8. Create the deployment layout on the VM

### Step 12 — Create directories

```bash
sudo mkdir -p /opt/saas-control/repo
sudo mkdir -p /opt/saas-control/shared/env
sudo mkdir -p /opt/saas-control/shared/logs
sudo mkdir -p /opt/saas-control/shared/nginx
sudo mkdir -p /opt/saas-control/scripts
sudo chown -R $USER:$USER /opt/saas-control
```

Expected layout:

```txt
/opt/saas-control/
  repo/
  shared/
    env/
    logs/
    nginx/
  scripts/
```

### Step 13 — Clone the repository

Replace `YOUR_REPO_URL` with the real git URL.

```bash
git clone YOUR_REPO_URL /opt/saas-control/repo
```

If the repo already exists and you are redeploying:

```bash
cd /opt/saas-control/repo
git pull
```

---

## 9. Place the production env files on the VM

You said you will handle the production environment variables yourself. Store them outside git.

### Step 14 — Create the env files

Backend env file:

```bash
nano /opt/saas-control/shared/env/backend.env
```

Frontend env file:

```bash
nano /opt/saas-control/shared/env/frontend.env
```

### What to put into these files

Use the variable names from:

- `backend/.env.example`
- `frontend/.env.example`

Do **not** commit these VM files back into git.

### Important values to double-check manually

Backend side:
- environment should be production-like, not test
- database URL should point to the intended production database
- ERPNext mode should remain safe for this phase
- production-like environments should not silently fall back to mock

Frontend side:
- API base URL should point to `https://crm-api.lenquant.com`
- any public site URL values should use `https://crm.lenquant.com`

---

## 10. Deploy the backend on the VM

### Step 15 — Create the backend virtual environment

Use the VM's default `python3` if it is already `3.11+`.

```bash
python3 -m venv /opt/saas-control/shared/backend-venv
```

### Step 16 — Install backend dependencies

```bash
cd /opt/saas-control/repo/backend
/opt/saas-control/shared/backend-venv/bin/pip install --upgrade pip
/opt/saas-control/shared/backend-venv/bin/pip install .
```

### Step 17 — Apply database migrations

Run this from the backend directory so Alembic resolves paths correctly:

```bash
cd /opt/saas-control/repo/backend
export $(grep -v '^#' /opt/saas-control/shared/env/backend.env | xargs)
/opt/saas-control/shared/backend-venv/bin/alembic upgrade head
```

### Step 18 — Seed reference data if needed

```bash
cd /opt/saas-control/repo/backend
export $(grep -v '^#' /opt/saas-control/shared/env/backend.env | xargs)
PYTHONPATH=/opt/saas-control/repo/backend /opt/saas-control/shared/backend-venv/bin/python -m app.db.seed
```

If your target database is already initialized and seeded, skip this step.

### Step 19 — Test the backend directly on the VM

```bash
cd /opt/saas-control/repo/backend
export $(grep -v '^#' /opt/saas-control/shared/env/backend.env | xargs)
PYTHONPATH=/opt/saas-control/repo/backend /opt/saas-control/shared/backend-venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Leave it running briefly and open a second SSH session, then test:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/integrations/erpnext/runtime
```

Expected behavior:
- `/` returns 200
- `/health` returns 200
- `/integrations/erpnext/runtime` returns 200

Stop the temporary uvicorn test with `Ctrl+C` after checking it.

---

## 11. Deploy the frontend on the VM

### Step 20 — Install frontend dependencies and build

```bash
cd /opt/saas-control/repo/frontend
npm install
```

Then build:

```bash
cd /opt/saas-control/repo/frontend
export $(grep -v '^#' /opt/saas-control/shared/env/frontend.env | xargs)
npm run build
```

### Step 21 — Test the frontend directly on the VM

```bash
cd /opt/saas-control/repo/frontend
export $(grep -v '^#' /opt/saas-control/shared/env/frontend.env | xargs)
npm run start -- --hostname 127.0.0.1 --port 3000
```

Open a second SSH session and test:

```bash
curl http://127.0.0.1:3000/
curl http://127.0.0.1:3000/login
```

Expected behavior:
- both endpoints return HTML successfully

Stop the temporary frontend test with `Ctrl+C`.

---

## 12. Create `systemd` services

This makes the app start on boot and restart after failures.

### Step 22 — Create the backend service file

```bash
sudo nano /etc/systemd/system/saas-backend.service
```

Paste:

```ini
[Unit]
Description=SaaS Control Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/saas-control/repo/backend
EnvironmentFile=/opt/saas-control/shared/env/backend.env
ExecStart=/bin/bash -lc 'PYTHONPATH=/opt/saas-control/repo/backend /opt/saas-control/shared/backend-venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000'
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

If your VM username is not `ubuntu`, replace it with the actual Linux user.

### Step 23 — Create the frontend service file

```bash
sudo nano /etc/systemd/system/saas-frontend.service
```

Paste:

```ini
[Unit]
Description=SaaS Control Frontend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/saas-control/repo/frontend
EnvironmentFile=/opt/saas-control/shared/env/frontend.env
ExecStart=/usr/bin/npm run start -- --hostname 127.0.0.1 --port 3000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Again, replace `ubuntu` if your Linux user is different.

### Step 24 — Enable and start both services

```bash
sudo systemctl daemon-reload
sudo systemctl enable saas-backend
sudo systemctl enable saas-frontend
sudo systemctl start saas-backend
sudo systemctl start saas-frontend
```

### Step 25 — Verify service health

```bash
sudo systemctl status saas-backend --no-pager
sudo systemctl status saas-frontend --no-pager
```

Check logs if needed:

```bash
sudo journalctl -u saas-backend --no-pager -n 100
sudo journalctl -u saas-frontend --no-pager -n 100
```

---

## 13. Configure Nginx

### Step 26 — Install Certbot packages now

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Step 27 — Create the Nginx site config

```bash
sudo nano /etc/nginx/sites-available/saas-control
```

Paste this config:

```nginx
server {
    listen 80;
    server_name crm.lenquant.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

server {
    listen 80;
    server_name crm-api.lenquant.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 28 — Enable the site

```bash
sudo ln -s /etc/nginx/sites-available/saas-control /etc/nginx/sites-enabled/saas-control
```

If the symlink already exists, skip this.

### Step 29 — Remove the default site if needed

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

### Step 30 — Test and reload Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Step 31 — Check HTTP before TLS

From your local computer browser, try:

- `http://crm.lenquant.com`
- `http://crm-api.lenquant.com/health`

If DNS is correct and the services are up, these should respond over plain HTTP.

---

## 14. Enable HTTPS with Let's Encrypt

Do this only after DNS is correct and HTTP is already working.

### Step 32 — Run Certbot

```bash
sudo certbot --nginx -d crm.lenquant.com -d crm-api.lenquant.com
```

When prompted:
- enter your email address
- agree to the terms
- choose the option to redirect HTTP to HTTPS

### Step 33 — Verify certificate installation

```bash
sudo nginx -t
sudo systemctl reload nginx
sudo certbot certificates
```

### Step 34 — Verify HTTPS in the browser

Open:

- `https://crm.lenquant.com`
- `https://crm-api.lenquant.com/health`
- `https://crm-api.lenquant.com/integrations/erpnext/runtime`

Expected:
- browser certificate is valid
- no certificate warnings
- pages load over HTTPS

---

## 15. Final smoke tests

Run all of these after HTTPS is live.

### Public and app routes

Open these in a browser:

- `https://crm.lenquant.com/`
- `https://crm.lenquant.com/pricing`
- `https://crm.lenquant.com/contact`
- `https://crm.lenquant.com/demo`
- `https://crm.lenquant.com/login`
- `https://crm.lenquant.com/app`
- `https://crm.lenquant.com/app/organizations`
- `https://crm.lenquant.com/app/tenants`
- `https://crm.lenquant.com/app/settings`

### Backend routes

Open in browser or run with `curl`:

```bash
curl https://crm-api.lenquant.com/health
curl https://crm-api.lenquant.com/integrations/erpnext/runtime
```

Expected backend behavior for this phase:
- backend is reachable
- database is ready
- ERPNext runtime mode is explicit
- production-like environments should not silently fall back to mock
- live ERPNext cutover is still not implemented in this phase

### Service checks on the VM

```bash
sudo systemctl status saas-backend --no-pager
sudo systemctl status saas-frontend --no-pager
sudo systemctl status nginx --no-pager
```

---

## 16. Restart procedure

Use this after code updates, env changes, or VM reboot.

### Restart commands

```bash
sudo systemctl restart saas-backend
sudo systemctl restart saas-frontend
sudo systemctl reload nginx
```

### Post-restart checks

```bash
sudo systemctl status saas-backend --no-pager
sudo systemctl status saas-frontend --no-pager
sudo systemctl status nginx --no-pager
curl https://crm-api.lenquant.com/health
curl https://crm-api.lenquant.com/integrations/erpnext/runtime
```

---

## 17. Basic update procedure for a new release

When you want to deploy new code later:

```bash
cd /opt/saas-control/repo
git pull
```

Then update backend:

```bash
cd /opt/saas-control/repo/backend
/opt/saas-control/shared/backend-venv/bin/pip install .
export $(grep -v '^#' /opt/saas-control/shared/env/backend.env | xargs)
/opt/saas-control/shared/backend-venv/bin/alembic upgrade head
```

Then update frontend:

```bash
cd /opt/saas-control/repo/frontend
export $(grep -v '^#' /opt/saas-control/shared/env/frontend.env | xargs)
npm install
npm run build
```

Then restart services:

```bash
sudo systemctl restart saas-backend
sudo systemctl restart saas-frontend
sudo systemctl reload nginx
```

Then rerun smoke tests.

---

## 18. Rollback basics

If a deployment breaks the SaaS app:

1. SSH into the VM.
2. Go to the repo:

```bash
cd /opt/saas-control/repo
```

3. Identify the previous known-good revision.
4. Check it out.
5. Rebuild backend and frontend.
6. Restart services.
7. Recheck:
   - `https://crm.lenquant.com`
   - `https://crm-api.lenquant.com/health`
   - `https://crm-api.lenquant.com/integrations/erpnext/runtime`

### Minimum rollback triggers

Rollback if:
- login is broken
- public routes are down
- `/health` is failing
- frontend assets are broken broadly
- Nginx serves persistent 5xx errors

---

## 19. What is still not done after this doc

Even after following this document, the following work is still outside Phase 16:

- ERPNext deployment on its own VM
- ERPNext demo site and tenant site creation
- live SaaS ↔ ERPNext cutover
- real ERPNext credential/reference activation
- pilot-client onboarding and go-live

---

## 20. Quick reference checklist

### GCP Console clicks

- Project selector → choose project
- Navigation menu > Billing
- Navigation menu > APIs & Services > Library
- Navigation menu > VPC network > IP addresses
- Navigation menu > Compute Engine > VM instances
- Navigation menu > Network Services > Cloud DNS

### Required SaaS DNS records

- `crm.lenquant.com` → SaaS VM static IP
- `crm-api.lenquant.com` → SaaS VM static IP

### Internal ports

- frontend → `127.0.0.1:3000`
- backend → `127.0.0.1:8000`

### Public ports

- `80`
- `443`

### Main local service files on the VM

- `/opt/saas-control/shared/env/backend.env`
- `/opt/saas-control/shared/env/frontend.env`
- `/etc/systemd/system/saas-backend.service`
- `/etc/systemd/system/saas-frontend.service`
- `/etc/nginx/sites-available/saas-control`

### Main verification URLs

- `https://crm.lenquant.com`
- `https://crm.lenquant.com/login`
- `https://crm-api.lenquant.com/health`
- `https://crm-api.lenquant.com/integrations/erpnext/runtime`
