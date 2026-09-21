from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.db.seed import seed_reference_data
from app.models.domain import Module, Organization, OrganizationModule


def run_alembic(db_url: str, command: str, revision: str) -> None:
    environment = os.environ.copy()
    environment["DATABASE_URL"] = db_url
    subprocess.run([sys.executable, "-m", "alembic", "-c", "alembic.ini", command, revision], cwd=Path(__file__).parents[1], env=environment, check=True, capture_output=True, text=True)


def test_phase3_upgrade_preserves_legacy_assignment_and_reupgrade_is_safe():
    with tempfile.TemporaryDirectory() as directory:
        db_path = Path(directory) / "legacy.db"
        db_url = f"sqlite:///{db_path.as_posix()}"
        run_alembic(db_url, "upgrade", "20260528_0007")
        connection = sqlite3.connect(db_path)
        now = "2026-09-17T00:00:00+00:00"
        organization_id = "legacy-org-00000000-0000-0000-0000-000000000001"
        module_id = "legacy-module-0000-0000-0000-000000000001"
        connection.execute("insert into organizations (id, created_at, updated_at, name, status) values (?, ?, ?, ?, ?)", (organization_id, now, now, "Legacy Company", "active"))
        connection.execute("insert into modules (id, created_at, updated_at, code, name, category, is_active) values (?, ?, ?, ?, ?, ?, ?)", (module_id, now, now, "inventory", "Inventory", "core", 1))
        connection.execute("insert into organization_modules (id, created_at, updated_at, organization_id, module_id, status, settings_json) values (?, ?, ?, ?, ?, ?, ?)", ("legacy-assignment-0000-0000-0000-000000000001", now, now, organization_id, module_id, "enabled", "{}"))
        disabled_org_id = "legacy-org-00000000-0000-0000-0000-000000000002"
        disabled_module_id = "legacy-module-0000-0000-0000-000000000002"
        connection.execute("insert into organizations (id, created_at, updated_at, name, status) values (?, ?, ?, ?, ?)", (disabled_org_id, now, now, "Legacy Disabled Company", "active"))
        connection.execute("insert into modules (id, created_at, updated_at, code, name, category, is_active) values (?, ?, ?, ?, ?, ?, ?)", (disabled_module_id, now, now, "legacy_disabled", "Legacy Disabled", "core", 1))
        connection.execute("insert into organization_modules (id, created_at, updated_at, organization_id, module_id, status, settings_json) values (?, ?, ?, ?, ?, ?, ?)", ("legacy-assignment-0000-0000-0000-000000000002", now, now, disabled_org_id, disabled_module_id, "disabled", "{}"))
        connection.commit()
        connection.close()
        run_alembic(db_url, "upgrade", "head")
        engine = create_engine(db_url, future=True)
        Session = sessionmaker(bind=engine, future=True)
        session = Session()
        try:
            seed_reference_data(session)
            legacy = session.execute(select(Module).where(Module.code == "inventory")).scalar_one()
            assignment = session.execute(select(OrganizationModule).where(OrganizationModule.organization_id == organization_id, OrganizationModule.module_id == legacy.id)).scalar_one()
            assert assignment.status == "enabled"
            disabled = session.execute(select(OrganizationModule).where(OrganizationModule.organization_id == disabled_org_id, OrganizationModule.module_id == disabled_module_id)).scalar_one()
            assert disabled.status == "disabled"
            assert disabled.explicit_state == "disabled"
            assert disabled.requested_state == "disabled"
            assert disabled.entitled_state == "not_entitled"
            assert legacy.alias_of == "stock"
            assert session.execute(select(Organization).where(Organization.id == organization_id)).scalar_one().name == "Legacy Company"
        finally:
            session.close()
            engine.dispose()
        run_alembic(db_url, "downgrade", "20260528_0007")
        run_alembic(db_url, "upgrade", "head")
        connection = sqlite3.connect(db_path)
        assert connection.execute("select count(*) from organization_modules where organization_id = ?", (organization_id,)).fetchone()[0] == 1
        assert connection.execute("select version_num from alembic_version").fetchone()[0] == "20260921_0014"
        connection.close()
