import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from verify_phase4_evidence import (  # noqa: E402
    evidence_passed,
    metadata_matches,
    run_completed_before_promotion,
)


def _run(run_id: int = 123) -> dict[str, object]:
    return {
        "id": run_id,
        "run_started_at": "2026-09-18T16:40:00Z",
        "updated_at": "2026-09-18T16:45:00Z",
    }


def _evidence(*, recovery: bool = False) -> dict[str, object]:
    return {
        "status": "passed",
        "state": "ready",
        "worker_status": "success",
        "step_count": 15,
        "recovery_run": recovery,
        "cleanup": {
            "status": "passed",
            "external_site_cleanup_verified": True,
            "external_site_deleted": 1,
        },
    }


def test_success_and_recovery_payloads_require_full_cleanup_readback() -> None:
    assert evidence_passed(_evidence(), recovery=False)
    assert evidence_passed(_evidence(recovery=True), recovery=True)

    incomplete = _evidence()
    incomplete["cleanup"] = {"status": "passed"}
    assert not evidence_passed(incomplete, recovery=False)


def test_metadata_must_bind_artifact_to_exact_candidate_and_run() -> None:
    run = _run()
    metadata = {
        "evidence_version": 2,
        "candidate_sha": "a" * 40,
        "staging_run_id": 123,
        "workflow_file": ".github/workflows/deploy-saas-control.yml",
        "success_evidence_file": "phase4-synthetic-evidence.json",
        "recovery_evidence_file": "phase4-synthetic-recovery-evidence.json",
    }
    assert metadata_matches(metadata, release_id="a" * 40, run=run)
    assert not metadata_matches(metadata, release_id="b" * 40, run=run)
    assert not metadata_matches(metadata, release_id="a" * 40, run=_run(124))


def test_evidence_run_must_start_and_complete_before_promotion_request() -> None:
    promotion_time = datetime(2026, 9, 18, 16, 50, tzinfo=timezone.utc)
    assert run_completed_before_promotion(_run(), promotion_time)

    later = _run()
    later["run_started_at"] = "2026-09-18T16:57:38Z"
    assert not run_completed_before_promotion(later, promotion_time)

    late_completion = _run()
    late_completion["updated_at"] = "2026-09-18T16:54:33Z"
    assert not run_completed_before_promotion(late_completion, promotion_time)
