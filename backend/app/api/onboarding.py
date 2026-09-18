from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_platform_admin
from app.core.config import settings
from app.db.session import get_db_session
from app.models.domain import SaaSUser
from app.schemas.onboarding import (
    OperatorExecutionAuthorization,
    OperatorOnboardingRead,
    OperatorReviewAction,
    PublicOnboardingCreate,
    PublicOnboardingRead,
    PublicOnboardingResult,
    PublicOnboardingRevision,
    OperatorRetryRequest,
    ProvisioningEventRead,
    ProvisioningJobDetailRead,
)
from app.services.onboarding_service import (
    OnboardingAccessError,
    OnboardingConflict,
    OnboardingError,
    OnboardingNotFound,
    OnboardingTransitionError,
    phase4_onboarding_service,
)

router = APIRouter(tags=["onboarding"])


def require_onboarding_operator_view(actor: SaaSUser = Depends(require_platform_admin)) -> SaaSUser:
    if not settings.feature_flag_map.get("onboarding_operator_view", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Onboarding operator view is not enabled.")
    return actor


def _raise(exc: OnboardingError) -> None:
    if isinstance(exc, OnboardingNotFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    if isinstance(exc, OnboardingAccessError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    if isinstance(exc, OnboardingConflict):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if isinstance(exc, OnboardingTransitionError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


def _public_error(exc: OnboardingError) -> None:
    if isinstance(exc, OnboardingAccessError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found.") from exc
    _raise(exc)


@router.post("/public/onboarding-requests", response_model=PublicOnboardingResult, status_code=status.HTTP_201_CREATED)
def create_public_request(payload: PublicOnboardingCreate, session: Session = Depends(get_db_session)):
    try:
        return phase4_onboarding_service.create_public(session, payload)
    except OnboardingError as exc:
        _raise(exc)


@router.get("/public/onboarding-requests/{request_id}", response_model=PublicOnboardingRead)
def read_public_request(request_id: str, x_onboarding_token: Optional[str] = Header(default=None, alias="X-Onboarding-Token"), session: Session = Depends(get_db_session)):
    try:
        return phase4_onboarding_service.read_public(session, request_id, x_onboarding_token or "")
    except OnboardingError as exc:
        _public_error(exc)


@router.post("/public/onboarding-requests/{request_id}/revisions", response_model=PublicOnboardingResult)
def revise_public_request(request_id: str, payload: PublicOnboardingRevision, x_onboarding_token: Optional[str] = Header(default=None, alias="X-Onboarding-Token"), session: Session = Depends(get_db_session)):
    try:
        return phase4_onboarding_service.revise_public(session, request_id, x_onboarding_token or "", payload)
    except OnboardingError as exc:
        _public_error(exc)


@router.post("/public/onboarding-requests/{request_id}/submit", response_model=PublicOnboardingResult)
def submit_public_request(request_id: str, x_onboarding_token: Optional[str] = Header(default=None, alias="X-Onboarding-Token"), session: Session = Depends(get_db_session)):
    try:
        return phase4_onboarding_service.submit_public(session, request_id, x_onboarding_token or "")
    except OnboardingError as exc:
        _public_error(exc)


@router.get("/operator/onboarding-requests", response_model=list[OperatorOnboardingRead])
def list_operator_requests(state: Optional[str] = Query(default=None), limit: int = Query(default=100, ge=1, le=200), session: Session = Depends(get_db_session), _: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.list_operator(session, state=state, limit=limit)
    except OnboardingError as exc:
        _raise(exc)


@router.get("/operator/onboarding-requests/{request_id}", response_model=OperatorOnboardingRead)
def get_operator_request(request_id: str, session: Session = Depends(get_db_session), _: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.get_operator(session, request_id)
    except OnboardingError as exc:
        _raise(exc)


@router.post("/operator/onboarding-requests/{request_id}/under-review", response_model=OperatorOnboardingRead)
def begin_review(request_id: str, payload: OperatorReviewAction, session: Session = Depends(get_db_session), actor: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.begin_review(session, actor, request_id, payload)
    except OnboardingError as exc:
        _raise(exc)


@router.post("/operator/onboarding-requests/{request_id}/approve", response_model=OperatorOnboardingRead)
def approve_request(request_id: str, payload: OperatorReviewAction, session: Session = Depends(get_db_session), actor: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.approve(session, actor, request_id, payload)
    except OnboardingError as exc:
        _raise(exc)


@router.post("/operator/onboarding-requests/{request_id}/reject", response_model=OperatorOnboardingRead)
def reject_request(request_id: str, payload: OperatorReviewAction, session: Session = Depends(get_db_session), actor: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.reject(session, actor, request_id, payload)
    except OnboardingError as exc:
        _raise(exc)


@router.post("/operator/onboarding-requests/{request_id}/cancel", response_model=OperatorOnboardingRead)
def cancel_request(request_id: str, payload: OperatorReviewAction, session: Session = Depends(get_db_session), actor: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.cancel(session, actor, request_id, payload)
    except OnboardingError as exc:
        _raise(exc)


@router.post("/operator/onboarding-requests/{request_id}/convert", response_model=OperatorOnboardingRead)
def convert_request(request_id: str, session: Session = Depends(get_db_session), actor: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.convert(session, actor, request_id)
    except OnboardingError as exc:
        _raise(exc)


@router.post("/operator/onboarding-requests/{request_id}/authorize-execution", response_model=OperatorOnboardingRead)
def authorize_execution(request_id: str, payload: OperatorExecutionAuthorization, session: Session = Depends(get_db_session), actor: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.authorize_execution(session, actor, request_id, payload)
    except OnboardingError as exc:
        _raise(exc)


@router.get("/operator/provisioning-jobs/{job_id}", response_model=ProvisioningJobDetailRead)
def get_provisioning_job_detail(job_id: str, session: Session = Depends(get_db_session), _: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.job_detail(session, job_id)
    except OnboardingError as exc:
        _raise(exc)


@router.get("/operator/provisioning-jobs/{job_id}/events", response_model=list[ProvisioningEventRead])
def get_provisioning_job_events(job_id: str, limit: int = Query(default=200, ge=1, le=500), session: Session = Depends(get_db_session), _: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.job_events(session, job_id, limit)
    except OnboardingError as exc:
        _raise(exc)


@router.post("/operator/provisioning-jobs/{job_id}/retry", response_model=ProvisioningJobDetailRead)
def retry_provisioning_step(job_id: str, payload: OperatorRetryRequest, session: Session = Depends(get_db_session), actor: SaaSUser = Depends(require_onboarding_operator_view)):
    try:
        return phase4_onboarding_service.retry_step(session, actor, job_id, payload)
    except OnboardingError as exc:
        _raise(exc)
