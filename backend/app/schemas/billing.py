from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PlanOut(BaseModel):
    id: str
    name: str
    slug: str
    price_cents: int
    currency: str
    description: Optional[str]


class PlanCreateRequest(BaseModel):
    name: str
    slug: str
    price_cents: int
    currency: str = "USD"
    description: Optional[str] = None


class SubscriptionOut(BaseModel):
    id: str
    organization_id: str
    tenant_id: Optional[str]
    plan_id: str
    status: str
    started_at: Optional[datetime]
    current_period_end: Optional[datetime]
    ended_at: Optional[datetime]


class SubscribeRequest(BaseModel):
    plan_slug: str
    tenant_id: Optional[str] = None


class InvoiceLine(BaseModel):
    description: str
    amount_cents: int
    quantity: int = 1


class InvoiceOut(BaseModel):
    id: str
    organization_id: str
    tenant_id: Optional[str]
    amount_cents: int
    currency: str
    status: str
    issued_at: Optional[datetime]
    paid_at: Optional[datetime]
    lines: List[InvoiceLine]


class InvoiceCreateRequest(BaseModel):
    amount_cents: Optional[int] = None
    currency: Optional[str] = None
    lines: Optional[List[InvoiceLine]] = None


class WebhookPayload(BaseModel):
    provider: str
    event: str
    data: dict
