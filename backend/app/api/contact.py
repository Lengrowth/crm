from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.contact import ContactRequest, ContactResponse
from app.services.communication_service import CommunicationError, communication_service

router = APIRouter()


@router.post("/marketing/contact", response_model=ContactResponse)
def marketing_contact(payload: ContactRequest):
    if not settings.resend_api_key:
        # Accept but do not fail hard in local dev; return a friendly response
        return ContactResponse(
            detail="Local capture: contact received (resend not configured)"
        )
    try:
        communication_service.send_contact_message(
            payload.name, payload.email, payload.message
        )
    except CommunicationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc
    return ContactResponse(detail="Contact message sent")


@router.post("/marketing/demo", response_model=ContactResponse)
def marketing_demo(payload: ContactRequest):
    if not settings.resend_api_key:
        return ContactResponse(
            detail="Local capture: demo request received (resend not configured)"
        )
    try:
        communication_service.send_demo_request(
            payload.name, payload.email, payload.message
        )
    except CommunicationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc
    return ContactResponse(detail="Demo request sent")
