from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_candidate_manifest_records_blocked_hrms_and_exact_runtime_baseline(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    (candidate / "ops" / "staging").mkdir(parents=True)
    (candidate / "frontend").mkdir()
    (candidate / "backend").mkdir()
    shutil.copy2(ROOT / "ops" / "staging" / "application-dependencies.json", candidate / "ops" / "staging" / "application-dependencies.json")
    shutil.copy2(ROOT / "ops" / "staging" / "release-runtime-baseline.json", candidate / "ops" / "staging" / "release-runtime-baseline.json")

    output = candidate / "release-manifest.json"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "release" / "build_manifest.py"),
            "--root",
            str(candidate),
            "--output",
            str(output),
            "--release-id",
            "phase2-test",
            "--control-plane-commit",
            "a" * 40,
            "--environment",
            "staging",
            "--runtime-baseline",
            str(candidate / "ops" / "staging" / "release-runtime-baseline.json"),
            "--application-dependencies",
            str(candidate / "ops" / "staging" / "application-dependencies.json"),
        ],
        check=True,
        cwd=ROOT,
    )

    manifest = json.loads(output.read_text(encoding="utf-8"))
    hrms = manifest["application_records"]["hrms"]
    assert hrms["intended_version"] == "15.64.1"
    assert hrms["intended_commit"] == "e68a3deaa95ae5b2c3d743297d0a4ab505733fc1"
    assert hrms["verification_status"] == "not_verified"
    assert hrms["compatibility_status"] == "blocked"
    assert manifest["runtime_baseline"] == "ops/staging/release-runtime-baseline.json"
    assert manifest["installed_apps"]["lenerp_core"]["commit"] == "a7e47208baf6583295f5f2632f4787262cd3f475"
