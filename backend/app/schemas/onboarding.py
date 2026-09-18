from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


OnboardingState = Literal[
    "draft",
    "submitted",
    "under_review",
    "approved",
    "provisioning",
    "validation",
    "ready",
    "rejected",
    "cancelled",
]


class SafeRequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ExpectedUser(SafeRequestModel):
    name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(default=None, max_length=120)
    count: Optional[str] = Field(default=None, max_length=20)


class OnboardingPayload(SafeRequestModel):
    company_name: str = Field(min_length=2, max_length=255)
    legal_name: Optional[str] = Field(default=None, max_length=255)
    industry: Optional[str] = Field(default=None, max_length=120)
    country: Optional[str] = Field(default=None, max_length=120)
    timezone: Optional[str] = Field(default=None, max_length=120)
    billing_email: Optional[EmailStr] = None
    administrator_name: str = Field(min_length=2, max_length=255)
    administrator_email: EmailStr
    requested_modules: list[str] = Field(default_factory=list, max_length=32)
    bundle_key: Optional[str] = Field(default=None, min_length=2, max_length=64)
    bundle_version: Optional[int] = Field(default=None, ge=1, le=100000)
    branding: dict[str, str] = Field(default_factory=dict)
    expected_users: list[ExpectedUser] = Field(default_factory=list, max_length=100)
    data_import_needs: Optional[str] = Field(default=None, max_length=2000)
    desired_domain: Optional[str] = Field(default=None, max_length=255)
    desired_infrastructure: Literal["isolated_staging", "isolated_synthetic"] = "isolated_synthetic"
    billing_contact: Optional[EmailStr] = None
    implementation_notes: Optional[str] = Field(default=None, max_length=4000)
    applicant_revision: int = Field(default=1, ge=1, le=100000)

    @field_validator("requested_modules")
    @classmethod
    def normalize_modules(cls, values: list[str]) -> list[str]:
        normalized = [value.strip().lower() for value in values if value.strip()]
        if len(set(normalized)) != len(normalized):
            raise ValueError("requested_modules must not contain duplicates.")
        return normalized

    @field_validator("branding")
    @classmethod
    def validate_branding(cls, values: dict[str, str]) -> dict[str, str]:
        allowed = {"display_name", "primary_color", "logo_ref", "favicon_ref"}
        unknown = set(values) - allowed
        if unknown:
            raise ValueError("branding contains an unsupported field.")
        return {key: value[:255] for key, value in values.items()}

    @field_validator("desired_domain")
    @classmethod
    def normalize_domain(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        normalized = value.strip().lower()
        if not normalized:
            return None
        if not normalized.replace(".", "").replace("-", "").isalnum() or ".." in normalized:
            raise ValueError("desired_domain must be a hostname, not a URL or path.")
        return normalized


class PublicOnboardingCreate(SafeRequestModel):
    idempotency_key: str = Field(min_length=8, max_length=128)
    payload: OnboardingPayload


class PublicOnboardingRevision(SafeRequestModel):
    idempotency_key: str = Field(min_length=8, max_length=128)
    payload: OnboardingPayload


class PublicOnboardingResult(BaseModel):
    request_id: str
    version: int
    state: OnboardingState
    applicant_visible_status: str
    management_token: Optional[str] = None
    replayed: bool = False


class PublicOnboardingRead(BaseModel):
    request_id: str
    version: int
    state: OnboardingState
    applicant_visible_status: str
    requested_modules: list[str]
    bundle_key: Optional[str] = None
    bundle_version: Optional[int] = None
    submitted_at: Optional[datetime] = None
    decision: Optional[str] = None
    decision_reason: Optional[str] = None
    converted: bool = False
    provisioning_status: Optional[str] = None


class OperatorReviewAction(SafeRequestModel):
    version: int = Field(ge=1)
    reason: str = Field(min_length=3, max_length=500)


class OperatorExecutionAuthorization(SafeRequestModel):
    version: int = Field(ge=1)
    confirmation: Literal["authorize_isolated_synthetic_execution"]
    reason: str = Field(min_length=3, max_length=500)


class OperatorOnboardingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    request_id: str
    state: OnboardingState
    applicant_visible_status: str
    current_version: int
    submitted_version: Optional[int] = None
    approved_version: Optional[int] = None
    snapshot: dict[str, object]
    requested_modules: list[str]
    bundle_key: Optional[str] = None
    bundle_version: Optional[int] = None
    organization_id: Optional[str] = None
    tenant_id: Optional[str] = None
    provisioning_job_id: Optional[str] = None
    approved_at: Optional[datetime] = None
    execution_authorized_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None


class ProvisioningStepRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    step_key: str
    ordinal: int
    status: str
    attempt_count: int
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    next_attempt_at: Optional[datetime] = None
    worker_id: Optional[str] = None
    failure_category: Optional[str] = None
    sanitized_error: Optional[str] = None
    evidence_json: dict[str, object]
    external_ref: Optional[str] = None
    rollback_state: str


class ProvisioningJobDetailRead(BaseModel):
    job_id: str
    tenant_id: str
    onboarding_request_id: Optional[str] = None
    status: str
    workflow_version: str
    attempt_count: int
    next_attempt_at: Optional[datetime] = None
    lease_expires_at: Optional[datetime] = None
    steps: list[ProvisioningStepRead]


class OperatorRetryRequest(SafeRequestModel):
    step_key: str = Field(min_length=3, max_length=64)
    confirmation: Optional[Literal["retry_safe_step", "confirm_irreversible_step"]] = None
    reason: str = Field(min_length=3, max_length=500)


class ProvisioningEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    step_id: str
    attempt: int
    event_code: str
    public_message: str
    context_json: dict[str, object]
    created_at: datetime
