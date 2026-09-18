"""Long-running control-plane provisioning worker entry point."""

from __future__ import annotations

import logging
import os
import time

from app.db.session import SessionLocal
from app.workers.provisioning_worker import run_next_job


logger = logging.getLogger(__name__)


def main() -> None:
    poll_seconds = max(0.5, float(os.environ.get("PROVISIONING_WORKER_POLL_SECONDS", "2")))
    logger.info("Provisioning worker started.")
    while True:
        try:
            with SessionLocal() as session:
                run_next_job(session)
        except KeyboardInterrupt:
            logger.info("Provisioning worker stopped.")
            return
        except Exception:
            logger.exception("Provisioning worker iteration failed safely.")
        time.sleep(poll_seconds)


if __name__ == "__main__":
    main()
