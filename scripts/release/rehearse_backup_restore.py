#!/usr/bin/env python3
"""Rehearse control-plane database/config/public/private-file recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


BACKEND = Path(__file__).resolve().parents[2] / "backend"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def alembic_upgrade(database: Path, revision: str) -> None:
    environment = os.environ.copy()
    environment["DATABASE_URL"] = f"sqlite:///{database.resolve().as_posix()}"
    subprocess.run(
        [sys.executable, "-m", "alembic", "-c", "alembic.ini", "upgrade", revision],
        cwd=BACKEND,
        env=environment,
        check=True,
    )


def create_fixture(root: Path) -> tuple[Path, Path, Path, Path]:
    root.mkdir(parents=True, exist_ok=True)
    database = root / "control-plane.db"
    config = root / "site_config.json"
    public_files = root / "public-files"
    private_files = root / "private-files"
    public_files.mkdir()
    private_files.mkdir()
    config.write_text('{"environment":"staging","hostname":"staging.example.test"}\n', encoding="utf-8")
    (public_files / "logo.txt").write_text("synthetic-public-file\n", encoding="utf-8")
    (private_files / "attachment.txt").write_text("synthetic-private-file\n", encoding="utf-8")
    connection = sqlite3.connect(database)
    try:
        connection.execute("CREATE TABLE evidence (id INTEGER PRIMARY KEY, value TEXT NOT NULL)")
        connection.execute("INSERT INTO evidence (value) VALUES (?)", ("synthetic-control-record",))
        connection.commit()
    finally:
        connection.close()
    return database, config, public_files, private_files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("only --self-test is available until a target backup destination is authorized")

    with tempfile.TemporaryDirectory(prefix="plat-p0-backup-") as directory:
        root = Path(directory)
        database, config, public_files, private_files = create_fixture(root / "source")
        alembic_upgrade(database, "20260522_0001")
        backup = root / "backup"
        restored = root / "restored"
        backup.mkdir()
        restored.mkdir()

        backup_database = backup / database.name
        source = sqlite3.connect(database)
        destination = sqlite3.connect(backup_database)
        try:
            source.backup(destination)
            destination.commit()
        finally:
            source.close()
            destination.close()
        shutil.copy2(config, backup / config.name)
        copy_tree(public_files, backup / public_files.name)
        copy_tree(private_files, backup / private_files.name)

        restored_database = restored / database.name
        shutil.copy2(backup_database, restored_database)
        shutil.copy2(backup / config.name, restored / config.name)
        copy_tree(backup / public_files.name, restored / public_files.name)
        copy_tree(backup / private_files.name, restored / private_files.name)

        alembic_upgrade(restored_database, "head")

        connection = sqlite3.connect(restored_database)
        try:
            row = connection.execute("SELECT value FROM evidence WHERE id = 1").fetchone()
            migration = connection.execute(
                "SELECT version_num FROM alembic_version"
            ).fetchone()
            organizations_table = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'organizations'"
            ).fetchone()
        finally:
            connection.close()
        assert row == ("synthetic-control-record",)
        assert migration == ("20260528_0007",)
        assert organizations_table == ("organizations",)
        assert json.loads((restored / config.name).read_text(encoding="utf-8"))["hostname"] == "staging.example.test"
        assert sha256(public_files / "logo.txt") == sha256(restored / public_files.name / "logo.txt")
        assert sha256(private_files / "attachment.txt") == sha256(restored / private_files.name / "attachment.txt")

    print("backup/restore rehearsal passed: restored control-plane database upgraded to head, data preserved, and site configuration/public/private files verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
