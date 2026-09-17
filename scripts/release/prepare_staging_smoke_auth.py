"""Create a disposable staging-only session for the release smoke test.

This never creates or changes a production account.  The account is synthetic,
has no password, and receives only a short-lived bearer session in the staging
control-plane database.  The bearer value is written to a runtime-only file
whose contents are never printed or committed.
"""

from __future__ import annotations

import argparse
import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import delete, select, update

from app.core.security import generate_session_token, hash_session_token
from app.db.session import SessionLocal
from app.models.domain import AuthSession, Organization, OrganizationMembership, SaaSUser


DEFAULT_EMAIL = "phase0-smoke@staging.example.test"
DEFAULT_ORGANIZATION = "Phase 0 Synthetic Workspace"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-file", required=True)
    parser.add_argument("--email", default=os.environ.get("STAGING_SMOKE_EMAIL", DEFAULT_EMAIL))
    parser.add_argument("--non-admin", action="store_true")
    parser.add_argument("--cleanup", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token_path = Path(args.token_file)
    token_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    token = generate_session_token()

    with SessionLocal() as session:
        if args.cleanup:
            user = session.execute(
                select(SaaSUser).where(SaaSUser.email == args.email.lower())
            ).scalar_one_or_none()
            if user is not None:
                session.execute(delete(AuthSession).where(AuthSession.user_id == user.id))
                session.execute(
                    delete(OrganizationMembership).where(OrganizationMembership.user_id == user.id)
                )
                session.delete(user)
                session.commit()
            print("staging smoke session cleaned")
            return

        user = session.execute(
            select(SaaSUser).where(SaaSUser.email == args.email.lower())
        ).scalar_one_or_none()
        if user is None:
            user = SaaSUser(
                email=args.email.lower(),
                full_name="Phase 1 Synthetic Non-Admin Smoke User" if args.non_admin else "Phase 0 Synthetic Smoke Operator",
                password_hash=None,
                status="active",
                is_platform_admin=not args.non_admin,
                email_verified_at=now,
            )
            session.add(user)
            session.flush()
        else:
            user.status = "active"
            user.is_platform_admin = not args.non_admin
            user.email_verified_at = user.email_verified_at or now

        organization = session.execute(
            select(Organization).where(Organization.name == DEFAULT_ORGANIZATION)
        ).scalar_one_or_none()
        if organization is None:
            organization = Organization(name=DEFAULT_ORGANIZATION, status="lead")
            session.add(organization)
            session.flush()

        membership = session.execute(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == organization.id,
                OrganizationMembership.user_id == user.id,
            )
        ).scalar_one_or_none()
        if membership is None:
            session.add(
                OrganizationMembership(
                    organization_id=organization.id,
                    user_id=user.id,
                    role="owner",
                )
            )

        session.execute(
            update(AuthSession)
            .where(AuthSession.user_id == user.id, AuthSession.revoked_at.is_(None))
            .values(revoked_at=now)
        )
        session.add(
            AuthSession(
                user_id=user.id,
                session_token_hash=hash_session_token(token),
                expires_at=now + timedelta(hours=1),
            )
        )
        session.commit()

    fd, temporary_path = tempfile.mkstemp(
        prefix=f".{token_path.name}.", dir=token_path.parent
    )
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(token)
        os.replace(temporary_path, token_path)
    finally:
        if os.path.exists(temporary_path):
            os.unlink(temporary_path)

    print("staging smoke session prepared")


if __name__ == "__main__":
    main()
