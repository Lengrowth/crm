# 22 — GitHub Actions SaaS Auto-Deploy Setup

**Project:** SaaS-first ERPNext control platform  
**Audience:** internal operators and founders  
**Scope:** automatic SaaS deployment on push to `main`  
**Last updated:** 2026-05-27

---

## 1. Purpose

This document explains how to set up **automatic deployment for the SaaS control plane** so that every push to `main` triggers a deployment on the SaaS VM.

This automation is for the SaaS VM only.

It assumes:

- the SaaS VM already exists
- the SaaS app already runs from `/opt/saas-control`
- the VM already has the repository cloned
- the VM can already pull from GitHub using the repo deploy key
- the frontend/backend services and Nginx already exist

This document does **not** automate ERPNext deployment or Phase 18 live cutover.

---

## 2. Recommended approach

For your current setup, the recommended approach is:

- run a **self-hosted GitHub Actions runner on the SaaS VM**
- let the workflow run locally on that VM
- let the VM pull the repo using its existing GitHub deploy key
- rebuild the app and restart the services on each push to `main`

### Why this is the best fit right now

- You already have a VM and a repo deploy key on that VM.
- You do not need to manage an extra SSH private key secret in GitHub Actions.
- You do not need GitHub to SSH into the VM over the public internet.
- It works well for a first production-style deployment.

---

## 3. What this automation will do

On every push to `main`, the workflow will:

1. run on the SaaS VM through a self-hosted runner
2. fetch the latest repo changes
3. reset the deployment working tree to the pushed commit SHA
4. install backend dependencies into the existing shared venv
5. run Alembic migrations
6. run the seed step
7. install frontend dependencies
8. build the frontend production bundle
9. restart `saas-backend`
10. restart `saas-frontend`
11. validate Nginx config and reload Nginx
12. run local health checks against:
   - `http://127.0.0.1:8000/health`
   - `http://127.0.0.1:8000/integrations/erpnext/runtime`
   - `http://127.0.0.1:3000/`

---

## 4. Files added in the repository

This setup uses:

- `.github/workflows/deploy-saas-control.yml`
- `scripts/deploy/deploy_saas_control.sh`

### Workflow trigger

The workflow triggers on:

- every push to `main`
- manual run from GitHub Actions with `workflow_dispatch`

### Runner label expected

The workflow expects a self-hosted runner with these labels:

- `self-hosted`
- `linux`
- `saas-control`

---

## 5. What must already exist on the VM

Before setting up the runner, all of the following must already exist on the VM:

- `/opt/saas-control/repo`
- `/opt/saas-control/shared/backend-venv`
- `/opt/saas-control/shared/env/backend.env`
- `/opt/saas-control/shared/env/frontend.env`
- `saas-backend.service`
- `saas-frontend.service`
- Nginx configured for:
  - `crm.lenquant.com`
  - `crm-api.lenquant.com`

Also confirm the VM can already pull from GitHub using the repo deploy key:

```bash
cd /opt/saas-control/repo
git remote -v
ssh -T git@github.com
```

Expected remote URL:

```text
git@github.com:BuildGrowthNow/crm.git
```

### Important security note

Your repo deploy key does **not** need write access for this workflow. Read-only access is enough and is recommended.

---

## 6. VM setup — allow service restarts without interactive sudo password

The GitHub Actions runner will need to restart services and reload Nginx. That means the runner user must be allowed to run those commands without an interactive password prompt.

This document assumes the runner will run as user:

- `fern2gue`

If you use another Linux user, replace it below.

### Step 1 — Check command paths

Run on the VM:

```bash
which systemctl
which nginx
```

Expected on Ubuntu:

- `/usr/bin/systemctl`
- `/usr/sbin/nginx`

### Step 2 — Create a sudoers file for deploy automation

Run:

```bash
sudo visudo -f /etc/sudoers.d/saas-control-deploy
```

Paste this line:

```text
fern2gue ALL=(root) NOPASSWD:/usr/bin/systemctl,/usr/sbin/nginx
```

Save and exit.

### Step 3 — Test the non-interactive sudo access

Run:

```bash
sudo -n /usr/bin/systemctl status nginx --no-pager
sudo -n /usr/sbin/nginx -t
```

If both work without asking for a password, the deploy runner has the required sudo access.

---

## 7. VM setup — install the self-hosted GitHub Actions runner

### Step 1 — Open the runner page in GitHub

In GitHub:

1. open the repository `BuildGrowthNow/crm`
2. click **Settings**
3. click **Actions**
4. click **Runners**
5. click **New self-hosted runner**
6. choose:
   - **Operating System:** Linux
   - **Architecture:** x64

GitHub will now show you a set of commands.

### Step 2 — Create the runner directory on the VM

Run on the VM:

```bash
sudo mkdir -p /opt/actions-runner
sudo chown -R fern2gue:fern2gue /opt/actions-runner
cd /opt/actions-runner
```

### Step 3 — Download the runner

Use the exact download URL shown by GitHub on the runner setup page.

It will look similar to this pattern:

```bash
curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/vX.Y.Z/actions-runner-linux-x64-X.Y.Z.tar.gz
tar xzf ./actions-runner-linux-x64.tar.gz
```

Use the version GitHub shows at setup time.

### Step 4 — Configure the runner

Run the exact `config.sh` command shown by GitHub.

It will look similar to:

```bash
./config.sh --url https://github.com/BuildGrowthNow/crm --token REPLACE_WITH_GITHUB_RUNNER_TOKEN
```

When prompted:

- **Runner group:** press Enter for the default
- **Runner name:** use `saas-control-01`
- **Labels:** enter `saas-control`
- **Work folder:** press Enter for the default `_work`

### Step 5 — Install the runner as a service

Run:

```bash
sudo ./svc.sh install fern2gue
sudo ./svc.sh start
```

### Step 6 — Confirm the runner is online in GitHub

Go back to:

- **GitHub > Repository > Settings > Actions > Runners**

You should now see a runner online with labels including:

- `self-hosted`
- `linux`
- `x64`
- `saas-control`

---

## 8. GitHub setup — workflow behavior

No GitHub repository secrets are required for this self-hosted runner approach.

The runner pulls work directly from GitHub and runs locally on the VM.

### What GitHub must allow

Check:

- **Repository > Settings > Actions > General**

Recommended values:

- Actions permissions: allow GitHub Actions
- Workflow permissions: **Read repository contents** is enough for this workflow

The workflow file already added to the repo is:

- `.github/workflows/deploy-saas-control.yml`

---

## 9. VM setup — make sure the deployed repo uses SSH remote

On the VM, run:

```bash
cd /opt/saas-control/repo
git remote -v
```

If the remote is not already SSH, set it to:

```bash
git remote set-url origin git@github.com:BuildGrowthNow/crm.git
```

Then verify:

```bash
git remote -v
```

Expected:

```text
origin  git@github.com:BuildGrowthNow/crm.git (fetch)
origin  git@github.com:BuildGrowthNow/crm.git (push)
```

Again: read-only access is enough for the VM deploy key even if the push URL is present.

---

## 10. First dry run on the VM before trusting automation

Before relying on GitHub Actions, run the deploy script manually on the VM once.

From the repo root on the VM:

```bash
cd /opt/saas-control/repo
chmod +x scripts/deploy/deploy_saas_control.sh
./scripts/deploy/deploy_saas_control.sh main
```

This confirms:

- the script can access the repo
- the env files are present
- migrations work
- builds work
- the services can be restarted
- the local health checks pass

Do not enable automatic deploys until the manual script run succeeds.

---

## 11. First GitHub Actions test

After the runner is online and the manual script succeeds:

1. push the workflow and script to `main`
2. open **GitHub > Actions**
3. open **Deploy SaaS Control Plane**
4. watch the job run on `saas-control-01`

If it passes, future pushes to `main` will deploy automatically.

---

## 12. Recommended operating rules

### Rule 1 — Only deploy from `main`

This workflow is intentionally limited to `main`.

Do not auto-deploy feature branches.

### Rule 2 — Do not edit `/opt/saas-control/repo` manually on the VM

The deploy script uses:

- `git fetch`
- `git checkout`
- `git reset --hard`

Treat `/opt/saas-control/repo` as a machine-managed checkout.

### Rule 3 — Keep env files outside git

Keep using:

- `/opt/saas-control/shared/env/backend.env`
- `/opt/saas-control/shared/env/frontend.env`

Do not commit production secrets into the repository.

### Rule 4 — Prefer read-only repo deploy keys on the VM

Write access is not needed for deployment pulls.

---

## 13. How rollback works with this setup

This workflow always deploys the pushed commit on `main`.

If you need to roll back, the safest GitHub-first path is:

1. revert the bad commit in GitHub
2. push the revert to `main`
3. let the workflow deploy the reverted state

For urgent manual rollback, SSH into the VM and run the deploy script against an older commit SHA after fetching it.

Example manual rollback shape:

```bash
cd /opt/saas-control/repo
git fetch --prune origin
./scripts/deploy/deploy_saas_control.sh main COMMIT_SHA_HERE
```

Only do manual SHA-based rollback if you understand exactly which commit you are deploying.

---

## 14. Troubleshooting checklist

### Runner does not appear in GitHub

Check on the VM:

```bash
cd /opt/actions-runner
sudo ./svc.sh status
```

### Workflow starts but fails to restart services

Check whether the sudoers rule was created correctly:

```bash
sudo -n /usr/bin/systemctl status nginx --no-pager
sudo -n /usr/sbin/nginx -t
```

### Workflow cannot pull from GitHub on the VM

Check the repo remote and deploy key:

```bash
cd /opt/saas-control/repo
git remote -v
ssh -T git@github.com
```

### Workflow fails on migrations

Run manually on the VM:

```bash
cd /opt/saas-control/repo/backend
export $(grep -v '^#' /opt/saas-control/shared/env/backend.env | xargs)
/opt/saas-control/shared/backend-venv/bin/alembic upgrade head
```

### Workflow fails on frontend build

Run manually on the VM:

```bash
cd /opt/saas-control/repo/frontend
export $(grep -v '^#' /opt/saas-control/shared/env/frontend.env | xargs)
npm install
npm run build
```

---

## 15. Summary of what you need to configure

### On the VM

- repo exists at `/opt/saas-control/repo`
- repo remote uses `git@github.com:BuildGrowthNow/crm.git`
- GitHub deploy key on the VM works
- env files exist in `/opt/saas-control/shared/env/`
- backend venv exists in `/opt/saas-control/shared/backend-venv`
- `saas-backend.service` exists
- `saas-frontend.service` exists
- Nginx exists and works
- self-hosted GitHub runner is installed under `/opt/actions-runner`
- runner user can use `sudo` non-interactively for `systemctl` and `nginx`

### In GitHub

- self-hosted runner is registered and online
- runner has label `saas-control`
- workflow file exists on `main`
- Actions are enabled for the repo

Once all of that is in place, every push to `main` will deploy the SaaS app automatically.
