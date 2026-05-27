# 01 — GCP Infrastructure Runbook for ERPNext/Frappe SaaS MVP

**Project:** ERPNext/Frappe-based SaaS for field operations, drilling, construction, fleet, warehouse, and manual service companies  
**Owner:** Fernando Guerra / LenGrowth-LenQuant context  
**Last reviewed:** 2026-05-21  
**Primary goal:** get the first production-ready ERPNext/Frappe SaaS environment online on Google Cloud, without overbuilding.

---

## 0. The decision: start with one machine

At the beginning, use **one Google Cloud VM**.

```txt
Google Cloud VM
  ├── Docker / Docker Compose
  ├── Frappe / ERPNext containers
  ├── MariaDB container
  ├── Redis containers
  ├── Frappe workers
  ├── Frappe scheduler
  ├── Websocket service
  ├── Traefik or Nginx reverse proxy
  ├── SSL certificates
  ├── Your SaaS/admin control app, initially small
  └── Backups to Google Cloud Storage
```

Do **not** start with one VM per client. Frappe supports a multi-site model where many client “sites” run on one bench/server, and each site has its own database and configuration.

Your first real setup can look like this:

```txt
app.yourdomain.com                 -> SaaS/admin/control layer
client1.yourdomain.com             -> ERPNext site for client 1
demo.yourdomain.com                -> Demo ERPNext site
staging.yourdomain.com             -> Staging/test ERPNext site
ops.clientdomain.com               -> White-label custom domain for a client
```

Each ERP client should be a separate Frappe **site**:

```txt
client1.yourdomain.com
  ├── own database
  ├── own users
  ├── own files
  ├── own logo
  ├── own company settings
  └── own enabled modules
```

---

## 1. Recommended MVP architecture

### 1.1 Services

Use Frappe Docker as the base because it already gives the multi-container structure you need:

```txt
frontend        -> Nginx/static/reverse proxy layer inside Frappe Docker
backend         -> Python/Frappe backend
websocket       -> Socket.IO real-time service
scheduler       -> scheduled jobs
queue-short     -> short background jobs
queue-default   -> normal background jobs, depending on compose profile/version
queue-long      -> long background jobs
redis-cache     -> Redis cache
redis-queue     -> Redis background job queue
mariadb         -> MariaDB database
traefik/nginx   -> public HTTPS routing
```

Frappe Docker’s docs describe this same core architecture: frontend, backend, websocket, queue workers, scheduler, database, and Redis services.

### 1.2 Initial VM size

For the first demo + one small client:

```txt
Machine type: e2-standard-4 or equivalent
vCPU:         4
RAM:          16 GB
Boot disk:    150–200 GB balanced persistent disk
OS:           Ubuntu 24.04 LTS
Region:       europe-west3 or europe-west4
```

For very early testing only, you can try 2 vCPU / 8 GB RAM, but ERPNext can feel heavy. For a real client demo, start with **4 vCPU / 16 GB**.

### 1.3 Region

Recommended regions from Georgia/Tbilisi context:

```txt
europe-west3  -> Frankfurt
europe-west4  -> Netherlands
europe-west1  -> Belgium
```

Pick one and keep everything close together:

```txt
VM region
static IP region
backup bucket region/multi-region
snapshots
monitoring
```

### 1.4 Domain convention

Use one main SaaS domain and subdomains:

```txt
yourdomain.com                 -> marketing/main site
www.yourdomain.com             -> marketing/main site
app.yourdomain.com             -> SaaS admin/customer portal
erp.yourdomain.com             -> optional internal ERP route
demo.yourdomain.com            -> public demo/staging demo
client1.yourdomain.com         -> client 1 ERP
client2.yourdomain.com         -> client 2 ERP
```

For white-label clients:

```txt
ops.clientdomain.com           -> points to your VM/static IP
```

---

## 2. What to create in Google Cloud

You need these GCP resources:

```txt
1. Project
2. Billing attached
3. Compute Engine VM
4. Static external IP
5. Firewall rules for 80/443
6. Restricted SSH access
7. Cloud Storage bucket for backups
8. Optional Cloud DNS zone
9. Monitoring/Ops Agent
10. Service account for the VM
11. Optional snapshot schedule
```

You do **not** need Kubernetes at the start.

You do **not** need Cloud SQL at the start if you are comfortable with MariaDB on the VM.

You do **not** need custom VPC routing at the start. The default internet route is enough for a public VM. The important parts are firewall rules and DNS.

---

## 3. Create the GCP project

### 3.1 Console path

```txt
Google Cloud Console
  -> Project selector
  -> New Project
```

Suggested project name:

```txt
lengrowth-erp-prod
```

Suggested project ID:

```txt
lengrowth-erp-prod
```

GCP project IDs must be globally unique, so you may need something like:

```txt
lengrowth-erp-prod-001
```

### 3.2 Enable billing

```txt
Google Cloud Console
  -> Billing
  -> Link billing account
```

### 3.3 Enable APIs

Enable these APIs:

```txt
Compute Engine API
Cloud Storage API
Cloud DNS API, if using Cloud DNS
Cloud Monitoring API
Cloud Logging API
IAM API
```

You can use the Console, or CLI:

```bash
gcloud services enable compute.googleapis.com \
  storage.googleapis.com \
  dns.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com \
  iam.googleapis.com
```

---

## 4. Create the service account

Create a service account for the VM instead of using broad personal credentials on the server.

### 4.1 Console path

```txt
IAM & Admin
  -> Service Accounts
  -> Create Service Account
```

Suggested name:

```txt
erpnext-prod-vm-sa
```

Suggested ID:

```txt
erpnext-prod-vm-sa
```

### 4.2 Minimum roles for MVP

At the project level, avoid giving Owner/Editor.

Recommended:

```txt
Logs Writer
Monitoring Metric Writer
```

For backups, give permissions only on the backup bucket after you create it, not whole-project Storage Admin.

On the backup bucket, grant:

```txt
Storage Object Admin
```

This lets the VM upload backup files to that specific bucket.

### 4.3 VM access scope

When creating the VM, use the custom service account and set access scopes to allow Cloud API access. Google’s Compute Engine docs recommend controlling permissions using IAM roles.

---

## 5. Reserve a static external IP

Do this **before** or **during** VM creation.

### 5.1 Console path

```txt
VPC Network
  -> IP addresses
  -> Reserve external static IP address
```

Suggested name:

```txt
erpnext-prod-ip
```

Settings:

```txt
IP version: IPv4
Type: Regional
Region: same as VM, for example europe-west3
Network tier: Premium, unless cost forces Standard
```

Write down the IP:

```txt
STATIC_IP=xx.xx.xx.xx
```

You will use this IP in DNS A records.

---

## 6. Create the VM

### 6.1 Console path

```txt
Compute Engine
  -> VM instances
  -> Create instance
```

### 6.2 Recommended VM settings

```txt
Name:        erpnext-prod-01
Region:      europe-west3 or europe-west4
Zone:        any zone in that region
Machine:     e2-standard-4
OS:          Ubuntu 24.04 LTS
Boot disk:   150–200 GB balanced persistent disk
```

### 6.3 Networking

Network tags:

```txt
erpnext-web
erpnext-ssh
```

External IP:

```txt
Use the reserved static IP: erpnext-prod-ip
```

Firewall checkboxes:

```txt
Allow HTTP traffic:  yes
Allow HTTPS traffic: yes
```

Even if you use the checkboxes, still verify the firewall rules after creation.

### 6.4 Identity and API access

Service account:

```txt
erpnext-prod-vm-sa
```

Access scopes:

```txt
Allow full access to all Cloud APIs, then restrict using IAM roles.
```

---

## 7. Firewall rules

You need:

```txt
80/tcp   open to internet
443/tcp  open to internet
22/tcp   restricted, not open to the world
```

### 7.1 HTTP/HTTPS firewall rule

Console path:

```txt
VPC Network
  -> Firewall
  -> Create firewall rule
```

Settings:

```txt
Name: allow-erpnext-web
Network: default, unless you created a custom VPC
Direction: Ingress
Action: Allow
Targets: Specified target tags
Target tags: erpnext-web
Source IPv4 ranges: 0.0.0.0/0
Protocols and ports: tcp:80,tcp:443
```

This is normal for a public web app because Let’s Encrypt/Traefik needs HTTP/HTTPS to be reachable.

### 7.2 SSH firewall rule

Do **not** leave SSH open to the world forever.

Better options:

**Option A — Simple MVP:** restrict SSH to your current public IP.

```txt
Name: allow-erpnext-ssh-my-ip
Target tags: erpnext-ssh
Source IPv4 ranges: YOUR_PUBLIC_IP/32
Protocols and ports: tcp:22
```

**Option B — Better:** use Google IAP tunneling and do not expose SSH to the public internet.

For day one, Option A is easier. Later, move to IAP/OS Login.

### 7.3 Host firewall with UFW

Inside Ubuntu, you can also use UFW:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

If your GCP firewall already restricts SSH to your IP, UFW is a second layer.

---

## 8. DNS setup

You have two options.

### 8.1 Option A: DNS remains at GoDaddy/Cloudflare/etc.

This is easiest if your domain is already somewhere else.

Create A records pointing to the static IP:

```txt
Type: A
Name: @
Value: STATIC_IP
TTL: 300

Type: A
Name: www
Value: STATIC_IP
TTL: 300

Type: A
Name: app
Value: STATIC_IP
TTL: 300

Type: A
Name: demo
Value: STATIC_IP
TTL: 300

Type: A
Name: client1
Value: STATIC_IP
TTL: 300
```

For white-label clients:

```txt
Type: A
Name: ops
Value: YOUR_STATIC_IP
TTL: 300
```

If using Cloudflare proxy, set records to **DNS only** at first until SSL works. After HTTPS works, you can decide whether to proxy.

### 8.2 Option B: Use Cloud DNS

Console path:

```txt
Cloud DNS
  -> Create zone
```

Create a public zone:

```txt
Zone name: yourdomain-com
DNS name: yourdomain.com.
```

Then create A records for:

```txt
@
www
app
demo
client1
```

After creating the zone, Cloud DNS gives you nameservers. You must go to your domain registrar and replace the nameservers with the Cloud DNS nameservers.

### 8.3 Verify DNS

From your local machine:

```bash
nslookup app.yourdomain.com
nslookup demo.yourdomain.com
```

Or:

```bash
dig app.yourdomain.com +short
dig demo.yourdomain.com +short
```

Expected result:

```txt
STATIC_IP
```

Do not start SSL until DNS points correctly.

---

## 9. Initial server setup

SSH into the VM:

```bash
ssh YOUR_USER@STATIC_IP
```

Update packages:

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y git curl wget htop unzip jq ca-certificates gnupg lsb-release ufw
```

Set timezone if needed:

```bash
sudo timedatectl set-timezone Asia/Tbilisi
```

Create working directory:

```bash
sudo mkdir -p /opt/lengrowth-erp
sudo chown -R $USER:$USER /opt/lengrowth-erp
cd /opt/lengrowth-erp
```

Optional: create swap if RAM is tight. For 16 GB RAM, this is still useful.

```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
free -h
```

---

## 10. Install Docker and Docker Compose plugin

Use Docker’s official Ubuntu installation path.

```bash
# Remove conflicting packages if present
sudo apt-get remove -y docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc || true

# Install prerequisites
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# Add Docker official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Let your user run docker
sudo usermod -aG docker $USER
```

Log out and back in, then verify:

```bash
docker --version
docker compose version
docker run hello-world
```

---

## 11. Clone Frappe Docker

```bash
cd /opt/lengrowth-erp
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
cp example.env .env
```

Important:

```txt
Do not use pwd.yml for production.
pwd.yml is for disposable demo testing only.
For production/MVP, use compose.yaml + production overrides.
```

---

## 12. Configure `.env`

Open `.env`:

```bash
nano .env
```

Set values like this:

```env
ERPNEXT_VERSION=v16.19.1
DB_PASSWORD=REPLACE_WITH_LONG_RANDOM_PASSWORD
GUNICORN_THREADS=4
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=120
LETSENCRYPT_EMAIL=fernando@yourdomain.com
HTTP_PUBLISH_PORT=80
HTTPS_PUBLISH_PORT=443
SITES_RULE=Host(`demo.yourdomain.com`) || Host(`client1.yourdomain.com`) || Host(`app.yourdomain.com`)
```

Notes:

```txt
ERPNEXT_VERSION should be pinned. Do not use latest casually in production.
DB_PASSWORD must be strong and stored in your password manager.
SITES_RULE controls what hostnames Traefik routes to this Frappe stack.
When you add a new tenant domain, you will update SITES_RULE and redeploy/reload.
```

Generate a password:

```bash
openssl rand -base64 32
```

---

## 13. Start Frappe Docker production stack

Use Frappe Docker production compose files with MariaDB, Redis, and HTTPS.

```bash
cd /opt/lengrowth-erp/frappe_docker

docker compose \
  -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  -f overrides/compose.https.yaml \
  up -d
```

Check services:

```bash
docker compose ps
```

Check logs:

```bash
docker compose logs -f --tail=100
```

If the command complains about variables, re-open `.env` and fix them.

---

## 14. Create the first ERPNext site

The exact service name can vary by Frappe Docker version, but commonly you run bench commands inside the `backend` service/container.

Check container/service names:

```bash
docker compose ps
```

Then create a site. Replace placeholders:

```bash
docker compose exec backend bench new-site demo.yourdomain.com \
  --admin-password 'REPLACE_ADMIN_PASSWORD' \
  --db-root-password 'REPLACE_DB_PASSWORD' \
  --install-app erpnext
```

If `--install-app erpnext` fails because ERPNext is not available in the image, you are using the wrong image/build path. For production with custom apps, you will eventually build a custom image that includes ERPNext and your own app.

Run migration/build/cache clear:

```bash
docker compose exec backend bench --site demo.yourdomain.com migrate
docker compose exec backend bench --site demo.yourdomain.com clear-cache
docker compose exec backend bench --site demo.yourdomain.com clear-website-cache
```

Open:

```txt
https://demo.yourdomain.com
```

Login:

```txt
User: Administrator
Password: the admin password you set
```

---

## 15. Create additional tenant sites

Example for the first real client:

```bash
docker compose exec backend bench new-site client1.yourdomain.com \
  --admin-password 'REPLACE_CLIENT_ADMIN_PASSWORD' \
  --db-root-password 'REPLACE_DB_PASSWORD' \
  --install-app erpnext
```

Then install your custom app later:

```bash
docker compose exec backend bench --site client1.yourdomain.com install-app lengrowth_fieldops
```

For every new tenant, your process is:

```txt
1. Create DNS A record to static IP
2. Add hostname to SITES_RULE
3. Restart/redeploy Traefik/Frappe stack if required
4. Create Frappe site
5. Install ERPNext
6. Install your custom modules/app
7. Set logo/company/domain
8. Create client admin user
9. Test login
10. Run backup
```

---

## 16. SSL / HTTPS

### 16.1 Recommended MVP SSL

Use Frappe Docker’s HTTPS override with Traefik/Let’s Encrypt.

Requirements:

```txt
A records point to the VM static IP
Ports 80 and 443 are open in GCP firewall
Ports 80 and 443 are open in UFW
LETSENCRYPT_EMAIL is set
SITES_RULE includes the domain
```

Then restart/redeploy:

```bash
docker compose \
  -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  -f overrides/compose.https.yaml \
  up -d
```

Check logs:

```bash
docker compose logs -f --tail=200
```

Open:

```txt
https://demo.yourdomain.com
```

### 16.2 Common SSL failure causes

```txt
DNS not propagated
Wrong A record
Cloudflare proxy interfering during first certificate issue
Port 80 closed
Port 443 closed
Wrong SITES_RULE
Domain not matching Frappe site name
Too many certificate attempts hitting Let’s Encrypt rate limits
```

### 16.3 Cloudflare note

If using Cloudflare:

```txt
Initial setup: DNS only
After HTTPS works: optionally turn proxy on
SSL mode: Full Strict, once origin certificate is valid
```

Avoid “Flexible SSL” for app backends. It can cause redirect loops and insecure origin traffic.

---

## 17. Custom domains / white-label domains

For a white-label client domain:

```txt
ops.clientcompany.com -> A record -> YOUR_STATIC_IP
```

Then in Frappe, map the custom domain to the site. In non-Docker bench this is usually:

```bash
bench setup add-domain ops.clientcompany.com
```

With Docker, run through the backend container:

```bash
docker compose exec backend bench setup add-domain ops.clientcompany.com
```

If the command asks which site, choose the client’s site.

Then update `.env`:

```env
SITES_RULE=Host(`client1.yourdomain.com`) || Host(`ops.clientcompany.com`) || Host(`demo.yourdomain.com`)
```

Redeploy:

```bash
docker compose \
  -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  -f overrides/compose.https.yaml \
  up -d
```

Test:

```txt
https://ops.clientcompany.com
```

---

## 18. Backups

You need two backup types:

```txt
1. Application-level backups from Frappe/ERPNext
2. Disk-level snapshots from GCP
```

Application-level backups are better for restoring individual sites.
Disk snapshots are useful for disaster recovery of the whole VM.

### 18.1 Create Cloud Storage bucket

Console path:

```txt
Cloud Storage
  -> Buckets
  -> Create
```

Suggested bucket:

```txt
lengrowth-erpnext-prod-backups
```

Settings:

```txt
Location: same region or EU multi-region
Public access: Prevent public access
Versioning: Enable
Lifecycle: delete old noncurrent versions after 30–90 days
```

Grant the VM service account access to this bucket:

```txt
erpnext-prod-vm-sa -> Storage Object Admin on this bucket only
```

### 18.2 Manual Frappe backup

For one site:

```bash
docker compose exec backend bench --site demo.yourdomain.com backup --with-files
```

For all sites, depending on your bench version:

```bash
docker compose exec backend bench --site all backup --with-files
```

If `--site all` is not supported in your setup, loop through sites manually.

### 18.3 Find backup files

Inside Frappe, backups are generally stored under:

```txt
sites/{site}/private/backups/
```

In Docker, this path is inside the mounted sites volume/container. Verify with:

```bash
docker compose exec backend bash
cd /home/frappe/frappe-bench/sites
find . -type f -path '*private/backups*' | tail -20
```

### 18.4 Upload backups to GCS

Install Google Cloud CLI if it is not available, or use the VM’s default environment if it already has `gcloud`.

Test access:

```bash
gcloud storage buckets list
```

Copy backups:

```bash
gcloud storage cp /PATH/TO/BACKUP_FILE gs://lengrowth-erpnext-prod-backups/manual/
```

For Docker volumes, you may need a small backup script that copies files out of the container/volume first.

### 18.5 Simple backup script pattern

Create:

```bash
sudo nano /opt/lengrowth-erp/scripts/backup-all-sites.sh
```

Template:

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/opt/lengrowth-erp/frappe_docker"
BUCKET="gs://lengrowth-erpnext-prod-backups/frappe"
STAMP="$(date +%Y-%m-%d_%H-%M-%S)"

cd "$PROJECT_DIR"

# Create Frappe backups. Adjust command if your bench version does not support --site all.
docker compose exec -T backend bench --site all backup --with-files

# Copy backup files from container to a temporary host directory.
mkdir -p "/tmp/frappe-backups-$STAMP"
CONTAINER_ID="$(docker compose ps -q backend)"
docker cp "$CONTAINER_ID:/home/frappe/frappe-bench/sites" "/tmp/frappe-backups-$STAMP/sites"

# Upload only backup folders.
gcloud storage cp -r "/tmp/frappe-backups-$STAMP/sites" "$BUCKET/$STAMP/"

# Cleanup.
rm -rf "/tmp/frappe-backups-$STAMP"
```

Make executable:

```bash
sudo chmod +x /opt/lengrowth-erp/scripts/backup-all-sites.sh
```

Run manually:

```bash
/opt/lengrowth-erp/scripts/backup-all-sites.sh
```

Add cron:

```bash
crontab -e
```

Nightly backup at 03:30:

```cron
30 3 * * * /opt/lengrowth-erp/scripts/backup-all-sites.sh >> /var/log/frappe-backup.log 2>&1
```

### 18.6 GCP disk snapshot

Create a snapshot schedule:

```txt
Compute Engine
  -> Snapshots
  -> Snapshot schedules
  -> Create schedule
```

Recommended:

```txt
Daily snapshot
Keep 7–14 days
Attach to VM boot disk
```

This protects you from VM/disk failure, but still keep Frappe app-level backups.

---

## 19. Monitoring and logs

### 19.1 Install Ops Agent

Use Google’s Ops Agent on the VM for CPU, memory, disk, and system logs.

Console path:

```txt
Compute Engine
  -> VM instances
  -> erpnext-prod-01
  -> Observability
  -> Install Ops Agent
```

Or follow the CLI instructions from Google Cloud’s Ops Agent docs.

### 19.2 Docker health checks

Useful commands:

```bash
docker compose ps
docker compose logs -f --tail=200
docker stats
```

### 19.3 Disk usage

```bash
df -h
du -sh /opt/lengrowth-erp/*
docker system df
```

Do **not** blindly run this in production without understanding it:

```bash
docker system prune -a --volumes
```

It can remove unused images/volumes. Be careful with volumes.

### 19.4 Alerts to create

In Cloud Monitoring, create alerts for:

```txt
Disk usage > 80%
CPU > 85% for 10 minutes
Memory high / swap usage high
VM down
No backup object uploaded in last 24 hours
HTTP 5xx spike, later when load balancer/logging exists
```

---

## 20. Updating ERPNext/Frappe

Do not auto-update production casually.

Recommended process:

```txt
1. Snapshot VM
2. Run Frappe backup with files
3. Test update on staging site/server
4. Check release notes
5. Pull/build new image
6. Run migration on staging
7. Smoke test
8. Apply to production
9. Keep rollback path ready
```

Basic commands, depending on Docker setup:

```bash
cd /opt/lengrowth-erp/frappe_docker
git pull
# update .env version intentionally, not blindly

docker compose pull
# or rebuild custom images when you have your custom app

docker compose up -d

docker compose exec backend bench --site all migrate
```

If `--site all` is not supported, migrate sites one by one.

---

## 21. Custom app deployment path

At first, deploy plain ERPNext.

Then create a custom app:

```txt
lengrowth_fieldops
```

Eventually build a custom Docker image that includes:

```txt
frappe
erpnext
lengrowth_fieldops
optional integration apps
```

Do not edit ERPNext core directly.

Preferred structure:

```txt
ERPNext core app
  unchanged

lengrowth_fieldops custom app
  Drilling Jobs
  Work Orders
  Crew Scheduling
  Vehicles
  Field Reports
  Safety Checklists
  QuickBooks sync
  SaaS/tenant settings
```

Install custom app on a site:

```bash
docker compose exec backend bench --site client1.yourdomain.com install-app lengrowth_fieldops
docker compose exec backend bench --site client1.yourdomain.com migrate
```

---

## 22. SaaS/admin app on the same VM

At the start, the SaaS layer can be one of these:

### Option A — simple Frappe admin site

Create a site:

```txt
app.yourdomain.com
```

Install your admin/control app there.

This admin site stores:

```txt
Tenants
Plans
Enabled modules
Domains
Billing status
Provisioning jobs
Backups
Release versions
```

### Option B — Next.js admin app

Run a small Next.js app on the same VM:

```txt
app.yourdomain.com -> Next.js SaaS control panel
client1.yourdomain.com -> Frappe/ERPNext site
```

This is good if your main SaaS/marketing stack is already Next.js.

For the first client, Option A is simpler because Frappe already gives auth, forms, roles, records, and admin UI.

---

## 23. Network/routing summary

### 23.1 GCP routes

For a simple public VM, you usually do not need custom routes.

You need:

```txt
Default VPC route to internet gateway
Firewall allow 80/443 to target tag erpnext-web
Restricted firewall rule for SSH
DNS A records pointing to static IP
Reverse proxy rules inside Docker/Traefik
```

### 23.2 Public routing

```txt
Browser
  -> DNS A record
  -> GCP static external IP
  -> GCP firewall allows 443
  -> VM
  -> Traefik/Nginx
  -> Frappe frontend/backend
  -> correct site by hostname
```

### 23.3 Internal routing

```txt
Frappe frontend
  -> backend service
  -> MariaDB
  -> Redis cache
  -> Redis queue
  -> websocket
  -> workers
```

---

## 24. First production checklist

Before giving access to a client:

```txt
[ ] Static IP reserved and attached
[ ] DNS A records correct
[ ] HTTP/HTTPS firewall open
[ ] SSH restricted
[ ] Docker installed
[ ] Frappe Docker running
[ ] MariaDB password strong
[ ] First site created
[ ] ERPNext installed
[ ] HTTPS working
[ ] Admin password stored in password manager
[ ] Backups tested manually
[ ] Backup bucket private
[ ] Disk snapshot schedule enabled
[ ] Monitoring/Ops Agent installed
[ ] Disk alert created
[ ] Basic client roles created
[ ] Demo/test user created
[ ] No test passwords left
[ ] No secrets committed to Git
```

---

## 25. When to start changing/customizing ERPNext

Do it in this order:

### Phase 1 — Plain ERPNext online

Goal:

```txt
Can I access ERPNext at https://demo.yourdomain.com?
```

Do not customize yet.

### Phase 2 — Basic company setup

Inside ERPNext:

```txt
Company
Currency
Chart of accounts
Users
Roles
Customers
Items
Warehouses
Quotation/invoice template
```

### Phase 3 — Manual drilling workflow using existing modules

Try to represent the drilling business using existing ERPNext objects:

```txt
Customer
Lead
Quotation
Project
Task
Employee
Asset
Stock Entry
Sales Invoice
```

This teaches you what ERPNext already covers.

### Phase 4 — Add custom fields only

Add custom fields to existing DocTypes:

```txt
Project: drilling type, site location, expected depth
Asset: rig type, vehicle plate, maintenance notes
Task: crew, planned date, field status
```

### Phase 5 — Create custom app

Only after you see repeated needs, create:

```txt
lengrowth_fieldops
```

Add real custom DocTypes:

```txt
Drilling Job
Borehole Log
Crew Assignment
Rig Assignment
Daily Field Report
Safety Checklist
Field Photo
Material Usage
Customer Sign-off
```

### Phase 6 — Automate provisioning

After one or two client implementations, automate:

```txt
Create site
Install app
Apply industry template
Set logo
Set modules
Create admin user
Connect billing
```

Do not build the full SaaS automation before the first workflow works.

---

## 26. When to split infrastructure later

Stay on one VM until there is pressure.

Split when:

```txt
You have multiple paying clients
One client needs dedicated resources
CPU/RAM/disk pressure is consistent
Backups are too large
You need separate staging/prod
Upgrades are risky
You need stronger isolation
```

Possible future architecture:

```txt
VM 1: SaaS main site + admin app
VM 2: ERP tenants 1–20
VM 3: ERP tenants 21–40
VM 4: enterprise dedicated client
Managed Redis
Dedicated MariaDB server or managed MySQL-compatible path
Cloud Load Balancer
Cloud Armor
```

Do not start here. Design for it, but do not pay for it yet.

---

## 27. Important references

- Frappe Docker repository: https://github.com/frappe/frappe_docker
- Frappe Docker getting started: https://github.com/frappe/frappe_docker/blob/main/docs/getting-started.md
- Frappe multitenancy: https://docs.frappe.io/framework/user/en/bench/guides/setup-multitenancy
- Frappe `bench new-site`: https://docs.frappe.io/framework/user/en/bench/reference/new-site
- Frappe custom domains: https://docs.frappe.io/framework/user/en/bench/guides/adding-custom-domains
- Frappe background jobs: https://docs.frappe.io/framework/user/en/api/background_jobs
- Docker Engine on Ubuntu: https://docs.docker.com/engine/install/ubuntu/
- Docker Compose plugin: https://docs.docker.com/compose/install/linux/
- GCP static IPs: https://docs.cloud.google.com/compute/docs/ip-addresses/configure-static-external-ip-address
- GCP firewall rules: https://docs.cloud.google.com/firewall/docs/using-firewalls
- GCP Cloud DNS records: https://docs.cloud.google.com/dns/docs/records
- GCP snapshots: https://docs.cloud.google.com/compute/docs/disks/create-snapshots
- GCP Cloud Storage object versioning: https://docs.cloud.google.com/storage/docs/object-versioning
- GCP Ops Agent: https://docs.cloud.google.com/stackdriver/docs/solutions/agents/ops-agent
