from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal
from app.integrations.erpnext_runtime import get_erpnext_runtime_summary
from app.models.domain import Module
from app.services.release_metadata import get_release_metadata

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    database_status = "unknown"
    service_status = "ok"

    try:
        with SessionLocal() as session:
            session.execute(select(func.count(Module.id))).scalar_one()
        database_status = "ready"
    except SQLAlchemyError:
        database_status = "not_ready"
        service_status = "degraded"

    erpnext_runtime = get_erpnext_runtime_summary()

    return {
        "status": service_status,
        "service": "saas-control-backend",
        "database": database_status,
        "erpnext_mode": erpnext_runtime["mode"],
        "erpnext_policy": erpnext_runtime["policy"],
    }


@router.get("/runtime/release")
def runtime_release() -> dict[str, object]:
    """Return safe release identity and server-controlled flags only."""
    return get_release_metadata()
