# Cloudflare R2 backup automation

The production backup destination is Cloudflare R2 bucket
`lenerp-phase0-backups`, not AWS S3. The repository contains the reproducible
automation under `ops/production/`:

- `saas-control-r2-backup.sh` runs the ERPNext `bench backup --with-files`,
  creates a consistent SQLite snapshot of the control plane, uploads all
  objects to a timestamped R2 prefix, and downloads each object once to verify
  SHA-256 equality.
- `saas-control-r2-backup.service` runs one backup.
- `saas-control-r2-backup.timer` runs it daily at 02:30 UTC with a 15-minute
  jitter and catches up after downtime.

## One-time owner action

Create a Cloudflare R2 S3 credential in the Cloudflare dashboard:

1. Open **Storage & databases → R2 → Overview → Manage** next to **API Tokens**.
2. Create an **Account API token** if this is an organization-owned automation,
   or a **User API token** if the owner wants it tied to one person.
3. Select **Object Read & Write** and scope it to only
   `lenerp-phase0-backups`.
4. Copy the Access Key ID and Secret Access Key once. Do not paste them into
   GitHub, chat, this repository, or ordinary documentation.
5. Open temporary SSH access to the EC2 and install them in
   `/etc/saas-control/r2-backup.env` with owner `root`, group `root`, and mode
   `0600`. This bucket reports the EU jurisdiction (`EEUR`), so use the
   endpoint
   `https://96e76c10fcf1d0d5970e17cf5c7008c8.eu.r2.cloudflarestorage.com`.

Cloudflare documents that R2 S3 credentials can be bucket-scoped and that the
S3 endpoint uses the account ID: <https://developers.cloudflare.com/r2/api/tokens/>
and <https://developers.cloudflare.com/r2/examples/aws/aws-cli/>.

## Install and verify on EC2

After the token is installed, run as root:

```bash
install -m 0755 ops/production/saas-control-r2-backup.sh /usr/local/sbin/saas-control-r2-backup
install -m 0644 ops/production/saas-control-r2-backup.service /etc/systemd/system/saas-control-r2-backup.service
install -m 0644 ops/production/saas-control-r2-backup.timer /etc/systemd/system/saas-control-r2-backup.timer
systemctl daemon-reload
systemctl enable --now saas-control-r2-backup.timer
systemctl start saas-control-r2-backup.service
systemctl status --no-pager saas-control-r2-backup.timer
journalctl -u saas-control-r2-backup.service -n 50 --no-pager
```

The log must end with `R2 backup and byte-hash verification passed`. Do not
log or print the environment file.

## Independent restore operator

The owner-confirmed second independent restore operator is Pedro
(`pedrocdiegues@gmail.com`). He can access the Cloudflare R2 bucket and EC2
restore runbook independently of the primary operator. No credentials are
stored in this repository.
