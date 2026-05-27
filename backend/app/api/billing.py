from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session, require_platform_admin
from app.schemas.billing import (
    InvoiceCreateRequest,
    InvoiceOut,
    PlanOut,
    SubscribeRequest,
    SubscriptionOut,
    WebhookPayload,
)
from app.schemas.billing import (
    PlanOut as PlanCreateOut,
)
from app.services.billing_service import BillingError, BillingService, PlanNotFound

router = APIRouter(prefix="/billing", tags=["billing"])
service = BillingService()


@router.get("/plans", response_model=list[PlanOut])
def list_plans(session: Session = Depends(get_db_session)):
    plans = service.list_plans(session)
    return [PlanOut(**p.__dict__) for p in plans]


@router.post(
    "/plans",
    response_model=PlanOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_platform_admin)],
)
def create_plan(payload: PlanOut, session: Session = Depends(get_db_session)):
    plan = service.create_plan(
        session,
        payload.name,
        payload.slug,
        payload.price_cents,
        payload.currency,
        payload.description,
    )
    return PlanOut(**plan.__dict__)


@router.post(
    "/organizations/{organization_id}/subscribe",
    response_model=SubscriptionOut,
    status_code=status.HTTP_201_CREATED,
)
def subscribe_organization(
    organization_id: str,
    payload: SubscribeRequest,
    session: Session = Depends(get_db_session),
):
    try:
        sub = service.subscribe_organization(
            session, organization_id, payload.plan_slug, payload.tenant_id
        )
    except PlanNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except BillingError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    return SubscriptionOut(**sub.__dict__)


@router.get(
    "/organizations/{organization_id}/subscription", response_model=SubscriptionOut
)
def get_subscription(organization_id: str, session: Session = Depends(get_db_session)):
    sub = service.get_subscription_for_organization(session, organization_id)
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )
    return SubscriptionOut(**sub.__dict__)


@router.post(
    "/organizations/{organization_id}/invoices",
    response_model=InvoiceOut,
    status_code=status.HTTP_201_CREATED,
)
def create_invoice(
    organization_id: str,
    payload: InvoiceCreateRequest | None = None,
    session: Session = Depends(get_db_session),
):
    # Find subscription for organization
    sub = service.get_subscription_for_organization(session, organization_id)
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found for organization",
        )
    invoice = service.generate_invoice_for_subscription(
        session,
        sub.id,
        amount_cents=payload.amount_cents if payload else None,
        lines=[l.model_dump() for l in payload.lines]
        if payload and payload.lines
        else None,
    )
    return InvoiceOut(**invoice.__dict__)


@router.get(
    "/organizations/{organization_id}/invoices/{invoice_id}", response_model=InvoiceOut
)
def get_invoice(
    organization_id: str, invoice_id: str, session: Session = Depends(get_db_session)
):
    from app.models.billing import BillingInvoice

    invoice = session.get(BillingInvoice, invoice_id)
    if invoice is None or invoice.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found"
        )
    return InvoiceOut(**invoice.__dict__)


@router.post("/webhook")
def webhook(payload: WebhookPayload, session: Session = Depends(get_db_session)):
    try:
        result = service.process_webhook(session, payload.model_dump())
    except BillingError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    return result
