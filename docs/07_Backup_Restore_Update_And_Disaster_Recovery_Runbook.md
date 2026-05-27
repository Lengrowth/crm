# 07 — Backup, Restore, Update, And Disaster Recovery Runbook

**Project:** ERPNext/Frappe SaaS operations  
**Audience:** Fernando / LenGrowth operations and technical team  
**Last updated:** 2026-05-21  
**Status:** Production operations runbook

---

## 1. Purpose

This document explains how to protect client data, restore tenants, update ERPNext/Frappe/custom apps, and recover from failures.

This is mandatory before paid clients.

You can survive bugs, bad deployments, and server issues if you have:

```txt
Reliable backups
Tested restores
Version records
Monitoring
Rollback plan
Disaster recovery procedure
```

You cannot survive data loss with clients.

---

## 2. Backup philosophy

Backups are not real until you test restore.

A backup plan must include:

```txt
What is backed up
Where it is stored
How often it runs
How long it is kept
Who can access it
How to restore it
How often restore is tested
```

For ERPNext/Frappe, backup must include:

```txt
Database
Public files
Private files
Site config, handled securely
Installed app versions
Custom app version
Docker image tag
Infrastructure notes
```

---

## 3. Backup types

### 3.1 Site-level backup

This protects one tenant/site.

Includes:

```txt
Database dump
Public files
Private files
```

Command pattern:

```bash
docker compose exec backend bench --site abc-drilling.yourdomain.com backup --with-files
```

or standard bench:

```bash
bench --site abc-drilling.yourdomain.com backup --with-files
```

### 3.2 Server-level snapshot

This protects the full VM disk.

Use for:

```txt
Fast recovery from VM failure
Before major updates
Before risky migrations
```

But do not rely only on VM snapshots. They are not a replacement for site-level backups.

### 3.3 Database-level backup

If MariaDB is separate, also use DB-level backups.

Useful for:

```txt
Large databases
Point-in-time restore, if configured
DB disaster recovery
```

### 3.4 File storage backup

Frappe stores uploaded files. Back up:

```txt
sites/site-name/public/files
sites/site-name/private/files
```

Private files can include sensitive documents. Protect access.

---

## 4. Backup schedule

Recommended MVP schedule:

```txt
Daily site-level backup with files
Weekly full VM snapshot
Before every production update: immediate backup
Before every tenant migration: immediate backup
Monthly restore test
```

For paid clients:

```txt
Daily backups minimum
Retention: 30 days minimum
Enterprise: 90+ days or contractual
Critical clients: more frequent backups
```

Example:

```txt
Daily 02:00: all site backups
Weekly Sunday 03:00: VM snapshot
Before deploy: manual backup
Monthly first Monday: restore test to staging
```

---

## 5. Backup storage

Use Google Cloud Storage.

Recommended bucket structure:

```txt
gs://your-erpnext-backups/
  production/
    sites/
      abc-drilling.yourdomain.com/
        2026/
          05/
            21/
              database.sql.gz
              public-files.tar
              private-files.tar
              metadata.json
      demo.yourdomain.com/
    server-snapshots/
    archived-sites/
  staging/
```

Metadata file:

```json
{
  "site": "abc-drilling.yourdomain.com",
  "backup_time": "2026-05-21T02:00:00Z",
  "frappe_version": "x",
  "erpnext_version": "x",
  "custom_app_version": "x",
  "docker_image": "registry/app:tag",
  "database_file": "database.sql.gz",
  "public_files": "public-files.tar",
  "private_files": "private-files.tar",
  "created_by": "scheduled-backup"
}
```

Enable:

```txt
Object versioning
Lifecycle policy
Restricted IAM
Encryption
Audit logs
```

---

## 6. Backup automation script

Example script outline:

```bash
#!/usr/bin/env bash
set -euo pipefail

SITE="$1"
DATE_PATH=$(date +"%Y/%m/%d/%H%M%S")
BACKUP_BUCKET="gs://your-erpnext-backups/production/sites/$SITE/$DATE_PATH"

docker compose exec backend bench --site "$SITE" backup --with-files

# Locate latest backup files.
# Exact paths may vary depending on your Frappe version/setup.
LOCAL_BACKUP_DIR="./sites/$SITE/private/backups"

gsutil -m cp "$LOCAL_BACKUP_DIR"/* "$BACKUP_BUCKET/"

echo "Backup completed for $SITE → $BACKUP_BUCKET"
```

Improve later:

```txt
Find exact backup filenames
Generate metadata.json
Upload metadata
Verify upload exists
Record backup in SaaS admin
Alert on failure
```

---

## 7. Backup verification

After every backup job:

```txt
[ ] Backup command exited successfully
[ ] Database backup file exists
[ ] Public files backup exists
[ ] Private files backup exists
[ ] Files uploaded to GCS
[ ] Backup size is reasonable
[ ] Metadata saved
[ ] SaaS backup record updated
[ ] Alert if failed
```

Warning signs:

```txt
Database backup size suddenly 0 or tiny
Private files backup missing
Upload failed
No backup for a site
Backup process takes much longer than usual
Disk almost full
```

---

## 8. Restore testing

Monthly, restore one tenant to staging.

### 8.1 Restore test goal

Confirm:

```txt
Backup file is usable
Database restores
Files restore
Site loads
Users/data exist
Custom app version is compatible
```

### 8.2 Restore test process

```txt
1. Pick a recent backup
2. Create staging restore site
3. Install same apps
4. Restore database and files
5. Run migrate if required
6. Load site
7. Check sample data
8. Record test result
```

### 8.3 Restore command pattern

Standard bench pattern:

```bash
bench --site restored-site.yourdomain.com restore /path/to/database.sql.gz \
  --with-public-files /path/to/public-files.tar \
  --with-private-files /path/to/private-files.tar
```

In Docker:

```bash
docker compose exec backend bench --site restored-site.yourdomain.com restore /path/to/database.sql.gz \
  --with-public-files /path/to/public-files.tar \
  --with-private-files /path/to/private-files.tar
```

Exact flags can vary by version; confirm with:

```bash
bench restore --help
```

---

## 9. Restore scenarios

### 9.1 Restore one accidentally damaged tenant

Use when:

```txt
Client deleted data
Bad import corrupted data
Bad customization affected one tenant
```

Process:

```txt
[ ] Stop user access or put tenant in maintenance mode
[ ] Take current backup before touching anything
[ ] Select restore point
[ ] Restore to staging first
[ ] Validate data
[ ] Restore production tenant if approved
[ ] Confirm with client
[ ] Record incident
```

### 9.2 Restore to a new site

Safer for testing:

```txt
abc-drilling-restore.yourdomain.com
```

This avoids overwriting production.

### 9.3 Restore production site

Dangerous. Requires approval.

```txt
[ ] Written approval
[ ] Current backup taken
[ ] Users notified
[ ] Maintenance window
[ ] Restore performed
[ ] Smoke test
[ ] Client confirmation
```

### 9.4 Full server recovery

Use if VM is lost.

Process:

```txt
1. Create new VM
2. Install Docker/compose
3. Pull same app images
4. Restore configuration/secrets
5. Restore MariaDB or create fresh DB
6. Restore sites from backups
7. Reattach DNS/static IP or update DNS
8. Issue SSL if needed
9. Run health checks
10. Notify clients
```

---

## 10. Update strategy

Updating includes:

```txt
Frappe version
ERPNext version
Your custom app version
Docker image version
MariaDB/Redis/container versions
OS packages
Reverse proxy/SSL stack
```

Do not update everything at once unless necessary.

---

## 11. Release process

### 11.1 Development

```txt
Build feature
Write tests
Run local migration
Test sample workflow
Update docs
Commit
Tag release candidate
```

### 11.2 Staging

```txt
Deploy to staging
Backup staging before migration
Run migration
Test ERPNext base flows
Test custom module flows
Test reports
Test permissions
Test background jobs
```

### 11.3 Production

```txt
Announce maintenance window if needed
Backup all affected tenants
Deploy image/code
Run migration in waves
Smoke test
Monitor logs
Mark release complete
```

---

## 12. Production update checklist

Before:

```txt
[ ] Release notes prepared
[ ] Staging tested
[ ] Backup verified
[ ] Rollback plan written
[ ] Migration risk assessed
[ ] Client impact known
[ ] Maintenance window selected if needed
```

During:

```txt
[ ] Put site(s) in maintenance if needed
[ ] Pull/build new images
[ ] Restart services
[ ] Run bench migrate
[ ] Clear cache if needed
[ ] Restart workers/scheduler
[ ] Test login
[ ] Test key workflows
```

After:

```txt
[ ] Monitor logs
[ ] Check scheduler
[ ] Check workers
[ ] Check background jobs
[ ] Check email sending
[ ] Check payment/billing webhooks
[ ] Check backup job still runs
[ ] Record version deployed
```

---

## 13. Migration waves

For multiple tenants:

```txt
Wave 0: local
Wave 1: staging
Wave 2: demo/internal tenant
Wave 3: first friendly client
Wave 4: low-risk clients
Wave 5: high-risk/enterprise clients
```

Do not run migrations across every paid client without testing.

---

## 14. Rollback plan

### 14.1 Code-only issue

If no database migration changed data:

```txt
Deploy previous image/version
Restart services
Smoke test
```

### 14.2 Database migration issue

You may need:

```txt
Restore from pre-update backup
Deploy previous image/version
Run smoke test
```

### 14.3 Data corruption

```txt
Stop affected tenant
Take current backup
Restore pre-incident backup to staging
Compare data
Restore production if approved
```

Always take a current backup before restoring, even if data is bad.

---

## 15. Monitoring

Monitor:

```txt
HTTP response
SSL certificate expiry
CPU
RAM
Disk usage
MariaDB health
Redis health
Worker status
Scheduler status
Queue backlog
Backup success
Email failures
Error logs
Payment webhook failures
```

Minimum alerts:

```txt
Site down
Disk > 80%
Memory pressure
Backup failed
SSL expiry soon
MariaDB unavailable
Redis unavailable
Workers down
Scheduler stopped
```

Useful commands:

```bash
docker compose ps
docker compose logs --tail=200 backend
docker compose logs --tail=200 scheduler
docker compose logs --tail=200 queue-default
docker compose exec backend bench --site site-name doctor
```

---

## 16. Disaster scenarios and response

### 16.1 Site is down

```txt
[ ] Check DNS
[ ] Check SSL
[ ] Check reverse proxy
[ ] Check containers
[ ] Check backend logs
[ ] Check database
[ ] Check Redis
[ ] Check disk space
[ ] Restart affected services if safe
[ ] Escalate if unresolved
```

### 16.2 Wrong tenant loads

This is serious.

```txt
[ ] Stop routing immediately
[ ] Check host/domain mapping
[ ] Check Frappe site config
[ ] Check reverse proxy labels/config
[ ] Check DNS records
[ ] Test each domain in incognito
[ ] Record incident
```

### 16.3 Disk full

```txt
[ ] Stop non-critical jobs
[ ] Check backup/log growth
[ ] Move old backups to GCS
[ ] Clean Docker unused images carefully
[ ] Increase disk size
[ ] Restart services
[ ] Add disk alert threshold
```

Commands:

```bash
df -h
du -sh *
docker system df
```

Be careful with:

```bash
docker system prune
```

Do not delete active volumes.

### 16.4 MariaDB down

```txt
[ ] Check container status
[ ] Check disk
[ ] Check logs
[ ] Restart db if safe
[ ] Verify data directory
[ ] Restore from backup if corrupted
```

### 16.5 Redis down

Impact:

```txt
Queues fail
Background jobs fail
Realtime/socket events fail
Caching problems
```

Actions:

```txt
[ ] Check Redis containers
[ ] Restart Redis
[ ] Restart workers
[ ] Check queue backlog
```

### 16.6 Bad deployment

```txt
[ ] Stop rollout
[ ] Keep affected tenants identified
[ ] Deploy previous image if code-only
[ ] Restore pre-deploy backup if data corrupted
[ ] Write postmortem
```

---

## 17. Security and access

Restrict:

```txt
SSH access
GCP IAM
Backup bucket access
Database credentials
Frappe Administrator password
Stripe secrets
Email provider secrets
QuickBooks tokens
```

Use:

```txt
SSH keys
2FA on cloud accounts
Least privilege IAM
Secret Manager
Encrypted backups
Audit logs
```

Do not share:

```txt
Server root password
Database root password
Administrator password
Backup bucket keys
Service account keys
```

---

## 18. Backup retention policy

Suggested:

```txt
Daily backups: 30 days
Weekly backups: 12 weeks
Monthly backups: 12 months
Archived cancelled tenant backups: according to contract
Enterprise: custom retention
```

Storage lifecycle:

```txt
After 30 days → cheaper storage class
After retention end → delete
Critical archived tenants → manual approval before deletion
```

---

## 19. Client data export

Clients may request data export.

Provide:

```txt
ERPNext export tools
CSV exports
PDF reports
Database backup only if contract allows
File attachments
Final invoice/accounting exports
```

Do not give raw database backups casually. They can contain sensitive data and internal system structure.

---

## 20. Incident report template

For every serious incident, record:

```txt
Incident ID
Date/time started
Date/time resolved
Affected tenants
Severity
What happened
Root cause
Customer impact
Actions taken
Data loss?
Restore used?
Prevention actions
Owner
```

Severity:

```txt
SEV1: site down/data exposure/data loss
SEV2: major workflow broken
SEV3: limited module issue
SEV4: minor bug/question
```

---

## 21. Monthly operations checklist

```txt
[ ] Restore test completed
[ ] Backup failures reviewed
[ ] Disk usage reviewed
[ ] SSL certificates checked
[ ] Security updates reviewed
[ ] Old logs cleaned
[ ] Tenant health reviewed
[ ] Open incidents reviewed
[ ] Staging updated
[ ] Documentation updated
```

---

## 22. Paid-client readiness checklist

Before accepting paid clients:

```txt
[ ] Daily backups automated
[ ] Restore tested
[ ] Monitoring active
[ ] SSL auto-renewal confirmed
[ ] Tenant provisioning documented
[ ] Support process ready
[ ] Update process tested
[ ] Role permissions reviewed
[ ] Admin credentials secured
[ ] Disaster recovery plan written
```

---

## 23. References

```txt
Frappe bench restore:
https://docs.frappe.io/framework/user/en/bench/reference/restore

Frappe bench commands:
https://docs.frappe.io/framework/user/en/bench/bench-commands

Frappe Docker:
https://github.com/frappe/frappe_docker

Frappe sites:
https://docs.frappe.io/framework/user/en/basics/sites

Frappe background jobs:
https://docs.frappe.io/framework/user/en/api/background_jobs
https://docs.frappe.io/framework/user/en/guides/app-development/running-background-jobs

Google Cloud Storage:
https://cloud.google.com/storage

Google Compute Engine snapshots:
https://cloud.google.com/compute/docs/disks/create-snapshots
```
