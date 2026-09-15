# Local/EC2 staging lane

This is the reproducible staging-lane contract for `PLAT-P0`. It is separate
from production in process, ports, data, files, configuration, and hostname.
The first rehearsal uses the host-header equivalent `staging.example.test`; it
does not require public DNS.

## Isolation contract

| Boundary | Staging | Production |
|---|---|---|
| Control-plane releases | `/opt/saas-control-staging/releases` | `/opt/saas-control/releases` |
| Active pointer | `/opt/saas-control-staging/current` | `/opt/saas-control/current` |
| Backend port | `18001` | `8001` |
| Frontend port | `13001` | `3000` |
| Control-plane DB | separate staging PostgreSQL/SQLite URL | production-only URL |
| ERP site/database/files | separate staging bench/site and backup set | production bench/site and backup set |
| Environment files | `/opt/saas-control-staging/shared/env/*` | `/opt/saas-control/shared/env/*` |
| Host policy | private access or `staging.example.test` host-header allowlist | approved production hostnames |
| Services/workers | `saas-control-staging-*` units and queues | production units and queues |

Do not copy production secrets or Champion data into this lane. Use synthetic
records until the credential exception is closed and secure data receipt is
approved. Run `bootstrap_ec2.sh` once as root on the approved EC2 to create the
dedicated staging user, virtual environment, environment files, and systemd
units. The lane is not considered operationally established until the target
host proves these boundaries with service, process, port, file, database,
backup, and access evidence. The ERP site/database/files still require a
separate disposable Frappe site; the production site must never be reused.

## Configuration

- Copy `backend.env.example` and `frontend.env.example` to the staging secret
  directory; fill values through the approved secret store.
- Keep `SAAS_BACKEND_INTERNAL_URL` on the private staging port.
- Keep the public staging hostname in configuration, not application source.
- Use a separate ERP site and database name; never point staging at the
  production site.
- Configure `AUTH_TOKEN_FILE` from a synthetic staging operator account when
  the smoke script is run with `REQUIRE_AUTH_SMOKE=true`; never put that token
  in Git, logs, or this repository.

## Verification commands

```bash
ss -ltnp | grep -E ':13001|:18001'
systemctl status saas-control-staging-backend saas-control-staging-frontend
curl -fsS -H 'Host: staging.example.test' http://127.0.0.1:13001/
curl -fsS -H 'Host: staging.example.test' http://127.0.0.1:18001/health
```

The documented production host is temporary implementation infrastructure;
final Champion domain ownership and cutover are tracked separately.
