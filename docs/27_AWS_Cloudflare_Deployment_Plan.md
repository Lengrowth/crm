# 27 — AWS + Cloudflare Deployment Plan

**LenERP SaaS Control Plane + ERPNext**
**Date:** 2026-08-28

---

## Overview

Deploy two systems on a single AWS EC2 instance fronted by Cloudflare:

| System | Description |
|--------|-------------|
| **LenERP control plane** | FastAPI backend + Next.js 15 frontend |
| **ERPNext** | Frappe/ERPNext multi-site via bench |

**Infrastructure shape:** Single `t3.large` EC2 (Ubuntu 22.04) — ERPNext + FastAPI + Next.js, all behind nginx. Cloudflare handles DNS, SSL termination, and proxying. No RDS needed for demo (ERPNext uses MariaDB on EC2; control plane keeps SQLite).

---

## Subdomain Map

| Domain | Routing |
|--------|---------|
| `lenerp.lengrowth.com` | EC2 → nginx → Next.js :3000 |
| `api.lenerp.lengrowth.com` | EC2 → nginx → FastAPI :8000 |
| `*.erp.lengrowth.com` | EC2 → bench-managed nginx (per-tenant ERPNext sites) |

`*.erp.lengrowth.com` is more specific than the existing `*.lengrowth.com` wildcard — no conflict in Cloudflare DNS.

---

## Phase 1 — Cloudflare DNS

1. In the Cloudflare dashboard for `lengrowth.com`, add three A records — all **proxied (orange cloud)**:

   ```
   A    lenerp              →  <EC2 Elastic IP>
   A    api.lenerp          →  <EC2 Elastic IP>
   A    *.erp               →  <EC2 Elastic IP>
   ```

   > Elastic IP does not exist yet. Park `1.1.1.1` as placeholder; update after Phase 2.

2. Set SSL/TLS mode to **Full (strict)** for the `lengrowth.com` zone.

3. In **SSL → Origin Certificates**, issue a Cloudflare origin certificate covering:
   - `*.lengrowth.com`
   - `*.erp.lengrowth.com`

   Download the certificate and private key — install them on EC2 in Phase 3.

---

## Phase 2 — AWS EC2 Provisioning

```bash
# Create security group
aws ec2 create-security-group \
  --group-name lenerp-sg \
  --description "LenERP demo server"

# Inbound rules:
#   Port 22   — your IP only
#   Port 80   — Cloudflare IP ranges (https://www.cloudflare.com/ips/)
#   Port 443  — Cloudflare IP ranges

# Launch instance (check AMI ID for your region — below is Ubuntu 22.04 us-east-1)
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.large \
  --key-name your-key \
  --security-group-ids sg-xxxx \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":40}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=lenerp-demo}]'

# Allocate Elastic IP and associate
aws ec2 allocate-address --domain vpc
aws ec2 associate-address --instance-id i-xxxx --allocation-id eipalloc-xxxx
```

After this step, go back to Phase 1 and update the three Cloudflare DNS records with the Elastic IP.

**Add 4 GB swap** (ERPNext spikes benefit from it):

```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Phase 3 — ERPNext via Bench Easy Install

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-minimal python3-pip git

# Download and run ERPNext easy-install
# Installs: bench, frappe, erpnext, MariaDB, Redis, nginx, supervisor
wget https://raw.githubusercontent.com/frappe/bench/develop/easy-install.py

python3 easy-install.py \
  --prod \
  --user frappe \
  --sitename erp.lengrowth.com \
  --email admin@lengrowth.com \
  --app erpnext
```

This takes 15–30 minutes. When complete:

- ERPNext is live at `erp.lengrowth.com` on port 80/443 via bench-managed nginx
- MariaDB and Redis running as system services
- `frappe` user owns everything under `/home/frappe/frappe-bench/`

**Install the Cloudflare origin certificate:**

```bash
sudo mkdir -p /etc/nginx/ssl
sudo nano /etc/nginx/ssl/cf-origin.pem   # paste certificate from Cloudflare dashboard
sudo nano /etc/nginx/ssl/cf-origin.key   # paste private key

# Enable bench multi-site DNS routing
sudo -u frappe bash -c "cd /home/frappe/frappe-bench && bench config dns_multitenant on"
sudo nginx -t && sudo systemctl reload nginx
```

---

## Phase 4 — Multi-Site ERPNext Config

Each new client tenant gets its own Frappe site:

```bash
cd /home/frappe/frappe-bench

# Create a new tenant site
sudo -u frappe bench new-site client1.erp.lengrowth.com \
  --db-name client1erp \
  --admin-password <strong-password>

# Install ERPNext on that site
sudo -u frappe bench --site client1.erp.lengrowth.com install-app erpnext

# Regenerate nginx config and reload
sudo -u frappe bench setup nginx
sudo nginx -t && sudo systemctl reload nginx
sudo supervisorctl reload
```

Repeat for additional tenants. Cloudflare's `*.erp.lengrowth.com` wildcard routes all subdomains to the EC2; bench's nginx `server_name` handles per-site routing internally.

---

## Phase 5 — Control Plane (FastAPI + Next.js) on EC2

### Backend (FastAPI)

```bash
sudo apt install -y python3.11 python3.11-venv

git clone https://github.com/<your-org>/<repo>.git /opt/lenerp
cd /opt/lenerp/backend

python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .

cp .env.example .env
# Edit .env — set ERPNEXT_MODE, FRONTEND_BASE_URL, CORS_ORIGINS (see Phase 6)

alembic upgrade head
python -m app.db.seed
```

Create systemd service:

```bash
sudo tee /etc/systemd/system/lenerp-api.service <<EOF
[Unit]
Description=LenERP FastAPI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/lenerp/backend
EnvironmentFile=/opt/lenerp/backend/.env
ExecStart=/opt/lenerp/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now lenerp-api
```

### Frontend (Next.js)

```bash
sudo apt install -y nodejs npm

cd /opt/lenerp/frontend
npm ci
NEXT_PUBLIC_API_URL=https://api.lenerp.lengrowth.com npm run build
```

Create systemd service:

```bash
sudo tee /etc/systemd/system/lenerp-web.service <<EOF
[Unit]
Description=LenERP Next.js
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/lenerp/frontend
Environment=PORT=3000
Environment=NEXT_PUBLIC_API_URL=https://api.lenerp.lengrowth.com
ExecStart=/usr/bin/npm run start
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now lenerp-web
```

### nginx vhosts

Add alongside bench's generated config:

```bash
sudo tee /etc/nginx/conf.d/lenerp.conf <<'EOF'
server {
    listen 443 ssl;
    server_name lenerp.lengrowth.com;

    ssl_certificate     /etc/nginx/ssl/cf-origin.pem;
    ssl_certificate_key /etc/nginx/ssl/cf-origin.key;

    location / {
        proxy_pass         http://127.0.0.1:3000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $http_cf_connecting_ip;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto https;
    }
}

server {
    listen 443 ssl;
    server_name api.lenerp.lengrowth.com;

    ssl_certificate     /etc/nginx/ssl/cf-origin.pem;
    ssl_certificate_key /etc/nginx/ssl/cf-origin.key;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $http_cf_connecting_ip;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto https;
    }
}
EOF

sudo nginx -t && sudo systemctl reload nginx
```

---

## Phase 6 — Wire Control Plane to ERPNext

In ERPNext: log in to `erp.lengrowth.com` as Administrator → **Settings → API Access** → generate API Key + Secret.

Update `/opt/lenerp/backend/.env`:

```env
ERPNEXT_MODE=live
ERPNEXT_BASE_URL=https://erp.lengrowth.com
ERPNEXT_API_KEY=<from ERPNext>
ERPNEXT_API_SECRET=<from ERPNext>
CORS_ORIGINS=https://lenerp.lengrowth.com
FRONTEND_BASE_URL=https://lenerp.lengrowth.com
SECURITY_HEADERS_ENABLED=true
RATE_LIMIT_ENABLED=true
RATE_LIMIT_MAX_REQUESTS=120
RATE_LIMIT_WINDOW_SECONDS=60
```

```bash
sudo systemctl restart lenerp-api
```

Smoke test: open `https://lenerp.lengrowth.com`, log in, create a tenant, verify the control plane calls ERPNext successfully.

---

## Phase 7 — CI/CD Update

Register a GitHub Actions self-hosted runner on the EC2. The existing workflow targets label `saas-control` — no workflow changes needed.

```bash
mkdir ~/actions-runner && cd ~/actions-runner

# Check https://github.com/actions/runner/releases for latest version
curl -o actions-runner-linux-x64.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.x.x/actions-runner-linux-x64-2.x.x.tar.gz
tar xzf ./actions-runner-linux-x64.tar.gz

# Get registration token: GitHub repo → Settings → Actions → Runners → New self-hosted runner
./config.sh \
  --url https://github.com/<org>/<repo> \
  --token <token> \
  --labels saas-control \
  --name lenerp-demo-01

sudo ./svc.sh install
sudo ./svc.sh start
```

Pushes to `main` now trigger automatic deploy via `.github/workflows/deploy-saas-control.yml`.

---

## Phase 8 — Hardening (before real traffic)

| Item | Action |
|------|--------|
| **Cloudflare WAF** | Enable managed ruleset; add rate-limit rule on `/auth/*` (10 req/min per IP) |
| **Security groups** | Confirm HTTP/HTTPS inbound is Cloudflare IPs only — no direct public access |
| **EC2 backups** | AWS Data Lifecycle Manager: daily AMI snapshot, 7-day retention |
| **MariaDB backups** | Cron: `mysqldump --all-databases` nightly, upload to S3 |
| **ERPNext updates** | `sudo -u frappe bash -c "cd /home/frappe/frappe-bench && bench update"` periodically |

---

## Estimated Timeline

| Phase | Effort |
|-------|--------|
| 1 — Cloudflare DNS | 15 min |
| 2 — EC2 provisioning | 20 min |
| 3 — ERPNext install | 30–45 min (automated, mostly waiting) |
| 4 — Multi-site config | 10 min per tenant |
| 5 — Control plane deploy | 30 min |
| 6 — Integration wire-up | 15 min |
| 7 — CI/CD | 15 min |
| **Total to live demo** | **~3 hours** |

---

## Related Docs

- `16_SaaS_Control_Plane_Deployment_On_GCP.md` — prior GCP approach (superseded by this doc)
- `17_ERPNext_Deployment_On_GCP.md` — prior GCP ERPNext approach (superseded by this doc)
- `backend/README.md` — backend local dev setup
- `scripts/deploy/deploy_saas_control.sh` — deploy script invoked by CI
