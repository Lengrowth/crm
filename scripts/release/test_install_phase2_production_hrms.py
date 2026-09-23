from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "release" / "install_phase2_production_hrms.sh"
VERIFY = ROOT / "scripts" / "release" / "verify_backup_manifest.sh"
EXPECTED = {
    "frappe": "edae775dd36b6c4ad7acab10230262bd74040765",
    "erpnext": "945e825bee3d0d645f6cb59bcaab90fcbfb98ce3",
    "hrms": "e68a3deaa95ae5b2c3d743297d0a4ab505733fc1",
}


pytestmark = pytest.mark.skipif(
    sys.platform == "win32" or shutil.which("bash") is None,
    reason="POSIX bash is required for release script scenarios",
)


def write_executable(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8", newline="\n")
    path.chmod(0o755)


def fixture(tmp_path: Path, mode: str) -> tuple[dict[str, str], Path]:
    bench = tmp_path / "bench"
    (bench / "sites").mkdir(parents=True)
    (bench / "sites" / "apps.txt").write_text("frappe\nerpnext\nhrms\nlenerp_core\n", encoding="utf-8")
    for app in ("frappe", "erpnext", "hrms", "lenerp_core"):
        (bench / "apps" / app / ".git").mkdir(parents=True)
    (bench / "apps" / "lenerp_core" / "SOURCE_COMMIT.txt").write_text("8d77cec7504d22f9c0a235034777e31fa07fc62\n", encoding="utf-8")
    release_root = tmp_path / "releases"
    candidate_source = release_root / "candidate" / "ops" / "staging" / "lenerp_core"
    candidate_source.mkdir(parents=True)
    (candidate_source / "SOURCE_COMMIT.txt").write_text("8d77cec7504d22f9c0a235034777e31fa07fc62\n", encoding="utf-8")
    backup = tmp_path / "backup"
    (backup / "erp").mkdir(parents=True)
    files = [backup / "erp" / "site-database.sql.gz", backup / "erp" / "site-files.tar", backup / "erp" / "site-private-files.tar"]
    for file in files:
        file.write_text(file.name, encoding="utf-8")
    manifest = backup / "manifest.sha256"
    manifest.write_text("\n".join(f"{hashlib.sha256(file.read_bytes()).hexdigest()}  {file.name}" for file in files) + "\n", encoding="utf-8")
    evidence = tmp_path / "backup.json"
    evidence.write_text(json.dumps({"local_backup_dir": str(backup)}), encoding="utf-8")
    log = tmp_path / "calls.log"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()

    write_executable(bin_dir / "sudo", """#!/bin/sh
set -eu
if [ "$1" = "-n" ]; then shift; fi
if [ "$1" = "-u" ]; then shift 2; fi
exec "$@"
""")
    write_executable(bin_dir / "supervisorctl", f"""#!/bin/sh
echo supervisorctl >> '{log}'
""")
    write_executable(bin_dir / "git", f"""#!/bin/sh
set -eu
case "$*" in
  *frappe*) echo {EXPECTED['frappe']};;
  *erpnext*) echo {EXPECTED['erpnext']};;
  *hrms*) if [ "${{FAKE_GIT_MODE:-exact}}" = wrong ]; then echo wrong; else echo {EXPECTED['hrms']}; fi;;
  *) echo wrong;;
esac
""")
    write_executable(bin_dir / "bench", f"""#!/bin/sh
set -eu
echo "$*" >> '{log}'
state='{tmp_path / 'hrms.state'}'
mode='{mode}'
case "$*" in
  *"list-apps"*)
    echo 'frappe 15.119.1'
    echo 'erpnext 15.120.0'
    echo 'lenerp_core 0.2.0'
    if [ -f "$state" ] || [ "$mode" = exact ] || [ "$mode" = wrong_version ]; then
      if [ "$mode" = wrong_version ]; then echo 'hrms 15.63.0'; else echo 'hrms 15.64.1'; fi
    fi
    ;;
  *"install-app hrms"*)
    touch "$state"
    if [ "$mode" = install_fail ]; then exit 9; fi
    ;;
  *"migrate"*)
    if [ "$mode" = migrate_fail ]; then exit 10; fi
    ;;
  *"execute frappe.client.get_count"*Role*) echo 9;;
  *"execute frappe.client.get_count"*Workspace*) echo 3;;
  *"restore"*) echo restore >> '{log}';;
esac
""")
    env = os.environ.copy()
    env.update({"PATH": f"{bin_dir}{os.pathsep}{env.get('PATH', '')}", "OUTPUT_FILE": str(tmp_path / "output.json"), "BACKUP_EVIDENCE_FILE": str(evidence), "RELEASE_ID": "candidate", "PRODUCTION_RELEASE_ROOT": str(release_root), "ERP_BENCH_DIR": str(bench), "ERP_SITE": "erp.synthetic.example", "SUDO_BIN": str(bin_dir / "sudo"), "SUPERVISORCTL_BIN": str(bin_dir / "supervisorctl"), "FAKE_GIT_MODE": "wrong" if mode == "wrong_source" else "exact"})
    return env, log


def run_case(tmp_path: Path, mode: str) -> tuple[subprocess.CompletedProcess[str], Path]:
    env, log = fixture(tmp_path, mode)
    result = subprocess.run([shutil.which("bash") or "bash", str(SCRIPT)], cwd=ROOT, env=env, text=True, capture_output=True)
    return result, log


def test_absent_hrms_is_installed_once_and_read_back(tmp_path: Path):
    result, log = run_case(tmp_path, "absent")
    assert result.returncode == 0, result.stderr
    calls = log.read_text(encoding="utf-8")
    assert calls.count("install-app hrms") == 1
    assert "migrate" in calls and "supervisorctl" in calls


def test_exact_hrms_replay_does_not_reinstall(tmp_path: Path):
    result, log = run_case(tmp_path, "exact")
    assert result.returncode == 0, result.stderr
    assert "install-app hrms" not in log.read_text(encoding="utf-8")


def test_wrong_version_fails_before_mutation(tmp_path: Path):
    result, log = run_case(tmp_path, "wrong_version")
    assert result.returncode != 0
    calls = log.read_text(encoding="utf-8")
    assert "no mutation was attempted" in result.stderr
    assert "setup requirements" not in calls and "migrate" not in calls


def test_failed_install_restores_verified_backup(tmp_path: Path):
    result, log = run_case(tmp_path, "install_fail")
    assert result.returncode != 0
    assert "restore" in log.read_text(encoding="utf-8")


def test_wrong_source_fails_before_mutation(tmp_path: Path):
    result, log = run_case(tmp_path, "wrong_source")
    assert result.returncode != 0
    assert "no mutation was attempted" in result.stderr
    assert "migrate" not in log.read_text(encoding="utf-8")
