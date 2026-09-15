#!/usr/bin/env python3
"""Rehearse immutable slot semantics without touching a real service or database."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


class SlotRehearsal:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.releases = root / "releases"
        self.staging = root / "staging"
        self.production = root / "production"
        self.releases.mkdir()
        self.staging.mkdir()
        self.production.mkdir()

    @staticmethod
    def _write_atomic(path: Path, value: str) -> None:
        temporary = path.with_suffix(path.suffix + ".next")
        temporary.write_text(value + "\n", encoding="utf-8")
        temporary.replace(path)

    def create_candidate(self, release_id: str, complete: bool = True) -> Path:
        candidate = self.releases / release_id
        candidate.mkdir()
        (candidate / "release-manifest.json").write_text(
            json.dumps(
                {
                    "release_id": release_id,
                    "environment": "staging",
                    "hostname": "staging.example.test",
                    "feature_flags": {},
                }
            ),
            encoding="utf-8",
        )
        if complete:
            (candidate / ".candidate-complete").write_text("ok\n", encoding="utf-8")
        return candidate

    def pointer(self, lane: Path, name: str = "current") -> str | None:
        path = lane / name
        return path.read_text(encoding="utf-8").strip() if path.exists() else None

    def preflight(self, candidate: Path) -> None:
        if not (candidate / ".candidate-complete").is_file():
            raise RuntimeError("candidate failed preflight")
        manifest = json.loads((candidate / "release-manifest.json").read_text(encoding="utf-8"))
        if manifest.get("environment") != "staging":
            raise RuntimeError("candidate environment is not staging")
        if "lengrowth.com" in manifest.get("hostname", ""):
            raise RuntimeError("staging candidate used the temporary hostname")

    @staticmethod
    def staging_smoke_passed(candidate: Path) -> bool:
        marker = candidate / ".staging-smoke-passed"
        return marker.is_file() and marker.read_text(encoding="utf-8").strip() == candidate.name

    def deploy(self, lane: Path, candidate: Path, health_ok: bool = True) -> str:
        self.preflight(candidate)
        old = self.pointer(lane)
        old_previous = self.pointer(lane, "previous")
        self._write_atomic(lane / "current", candidate.name)
        if not health_ok:
            if old:
                self._write_atomic(lane / "current", old)
            else:
                (lane / "current").unlink(missing_ok=True)
            if old_previous:
                self._write_atomic(lane / "previous", old_previous)
            return "rolled_back"
        (candidate / ".staging-smoke-passed").write_text(candidate.name + "\n", encoding="utf-8")
        if old and old != candidate.name:
            self._write_atomic(lane / "previous", old)
        return "switched"

    def rollback(self, lane: Path) -> None:
        previous = self.pointer(lane, "previous")
        if previous is None:
            raise RuntimeError("previous release pointer is missing")
        self._write_atomic(lane / "current", previous)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="plat-p0-slots-") as directory:
        rehearsal = SlotRehearsal(Path(directory))
        known_good = rehearsal.create_candidate("known-good")
        candidate = rehearsal.create_candidate("candidate-a")
        failed = rehearsal.create_candidate("candidate-failed")
        incomplete = rehearsal.create_candidate("candidate-incomplete", complete=False)

        rehearsal._write_atomic(rehearsal.staging / "current", known_good.name)
        rehearsal._write_atomic(rehearsal.production / "current", "production-known-good")
        assert rehearsal.deploy(rehearsal.staging, candidate) == "switched"
        assert rehearsal.staging_smoke_passed(candidate)
        first_current = rehearsal.pointer(rehearsal.staging)
        assert rehearsal.deploy(rehearsal.staging, candidate) == "switched"
        assert rehearsal.pointer(rehearsal.staging) == first_current == "candidate-a"
        assert rehearsal.pointer(rehearsal.staging, "previous") == "known-good"

        try:
            rehearsal.deploy(rehearsal.staging, incomplete)
        except RuntimeError:
            pass
        else:
            raise AssertionError("failed preflight received traffic")
        assert rehearsal.pointer(rehearsal.staging) == "candidate-a"

        assert rehearsal.deploy(rehearsal.staging, failed, health_ok=False) == "rolled_back"
        assert not rehearsal.staging_smoke_passed(failed)
        assert rehearsal.pointer(rehearsal.staging) == "candidate-a"
        rehearsal.rollback(rehearsal.staging)
        assert rehearsal.pointer(rehearsal.staging) == "known-good"
        assert rehearsal.pointer(rehearsal.production) == "production-known-good"

        first_deploy_lane = rehearsal.root / "first-deploy"
        first_deploy_lane.mkdir()
        assert rehearsal.deploy(first_deploy_lane, failed, health_ok=False) == "rolled_back"
        assert rehearsal.pointer(first_deploy_lane) is None

    print("slot rehearsal passed: idempotency, preflight rejection, staging-smoke evidence, health rollback, first-deploy safety, manual rollback, and production isolation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
