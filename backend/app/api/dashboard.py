from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.domain import SaaSUser
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import dashboard_service

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
) -> DashboardSummary:
    return dashboard_service.build_summary(session, current_user)
