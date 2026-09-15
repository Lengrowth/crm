# Temporary-to-Final Domain Cutover Checklist

The current hostname is an implementation dependency to inventory, not a permanent ownership boundary. Do not change public DNS during the first rehearsal.

## Before the cutover

- [ ] Record the Champion-controlled registrar, DNS, Cloudflare, AWS, TLS, backup, monitoring, and service-account owners.
- [ ] Add final staging hostname(s) using configuration only; do not change application logic.
- [ ] Verify nginx `server_name`, origin TLS/SNI, ERP host settings, allowed hosts, and health URLs.
- [ ] Verify authentication/session cookie domain, secure/SameSite settings, CSRF/CORS origins, login redirects, and callbacks.
- [ ] Verify generated links, email templates, password-reset/verification links, API clients, webhooks, files, and background jobs.
- [ ] Verify monitoring, alert URLs, backup metadata, and operator runbooks.
- [ ] Confirm temporary credentials have been rotated and secret values removed from ordinary documentation before Champion data handling.
- [ ] Create database/site-config/public/private-file backups and verify off-host copies.
- [ ] Record candidate release, previous compatible release, database revision, data recovery point, and rollback owner.

## Cutover

- [ ] Freeze changes and record the exact candidate manifest.
- [ ] Validate DNS and TLS from an external vantage point.
- [ ] Bind the final hostname and test public, login, authenticated app, API, ERP runtime, files, callbacks, and workers.
- [ ] Keep `erp.lengrowth.com` as a documented redirect/compatibility route only for the approved transition period.
- [ ] Observe logs, queues, backups, monitoring, and representative workflows.

## Rollback

- [ ] Restore the previous hostname/configuration pointer if DNS or application smoke fails.
- [ ] Switch code to the previous compatible immutable release.
- [ ] Restore database/files only under the approved data-recovery plan; code rollback alone does not undo data changes.
- [ ] Record the decision, evidence, duration, owner, and follow-up before retrying.
