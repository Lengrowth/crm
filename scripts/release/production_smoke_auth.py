"""Create and remove a disposable production smoke identity.

The production promotion workflow uses this only for authenticated release
smoke checks. It creates a uniquely named synthetic user and organization,
writes only the short-lived bearer token to a 0600 runtime file, and removes
the exact rows again in an always-run cleanup step. Token values are never
printed.
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
from app.models.domain import (
    AuthSession,
    AuthToken,
    Organization,
    OrganizationMembership,
    SaaSUser,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("prepare", "cleanup"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--email", required=True)
        subparser.add_argument("--organization", required=True)
        if command == "prepare":
            subparser.add_argument("--token-file", required=True)
    return parser.parse_args()


def prepare(args: argparse.Namespace) -> None:
    email = args.email.lower()
    now = datetime.now(timezone.utc)
    token = generate_session_token()

    with SessionLocal() as session:
        if session.execute(select(SaaSUser).where(SaaSUser.email == email)).scalar_one_or_none():
            raise SystemExit(f"refusing to reuse existing smoke email: {email}")
        if session.execute(
            select(Organization).where(Organization.name == args.organization)
        ).scalar_one_or_none():
            raise SystemExit(
                f"refusing to reuse existing smoke organization: {args.organization}"
            )

        user = SaaSUser(
            email=email,
            full_name="Phase 0 Production Smoke Operator",
            password_hash=None,
            status="active",
            is_platform_admin=True,
            email_verified_at=now,
        )
        organization = Organization(name=args.organization, status="lead")
        session.add_all([user, organization])
        session.flush()
        session.add(
            OrganizationMembership(
                organization_id=organization.id,
                user_id=user.id,
                role="owner",
            )
        )
        session.add(
            AuthSession(
                user_id=user.id,
                session_token_hash=hash_session_token(token),
                expires_at=now + timedelta(hours=1),
            )
        )
        session.commit()

    token_path = Path(args.token_file)
    token_path.parent.mkdir(parents=True, exist_ok=True)
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
    print("production smoke identity prepared")


def cleanup(args: argparse.Namespace) -> None:
    email = args.email.lower()
    with SessionLocal() as session:
        user = session.execute(
            select(SaaSUser).where(SaaSUser.email == email)
        ).scalar_one_or_none()
        organization = session.execute(
            select(Organization).where(Organization.name == args.organization)
        ).scalar_one_or_none()
        if user is not None:
            session.execute(delete(AuthSession).where(AuthSession.user_id == user.id))
            session.execute(delete(AuthToken).where(AuthToken.user_id == user.id))
            session.execute(
                delete(OrganizationMembership).where(
                    OrganizationMembership.user_id == user.id
                )
            )
            session.delete(user)
        if organization is not None:
            session.execute(
                delete(OrganizationMembership).where(
                    OrganizationMembership.organization_id == organization.id
                )
            )
            session.delete(organization)
        session.commit()
    print("production smoke identity cleaned")


def main() -> None:
    args = parse_args()
    if args.command == "prepare":
        prepare(args)
    else:
        cleanup(args)


if __name__ == "__main__":
    main()
