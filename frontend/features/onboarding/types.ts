export type OnboardingState = "draft" | "submitted" | "under_review" | "approved" | "provisioning" | "validation" | "ready" | "rejected" | "cancelled";

export type PublicOnboardingResult = {
  request_id: string;
  version: number;
  state: OnboardingState;
  applicant_visible_status: string;
  management_token?: string | null;
  replayed: boolean;
};

export type PublicOnboardingRead = {
  request_id: string;
  version: number;
  state: OnboardingState;
  applicant_visible_status: string;
  requested_modules: string[];
  bundle_key?: string | null;
  bundle_version?: number | null;
  submitted_at?: string | null;
  decision?: string | null;
  decision_reason?: string | null;
  converted: boolean;
  provisioning_status?: string | null;
};

export type OperatorOnboardingRead = {
  request_id: string;
  state: OnboardingState;
  applicant_visible_status: string;
  current_version: number;
  submitted_version?: number | null;
  approved_version?: number | null;
  snapshot: Record<string, unknown>;
  requested_modules: string[];
  bundle_key?: string | null;
  bundle_version?: number | null;
  organization_id?: string | null;
  tenant_id?: string | null;
  provisioning_job_id?: string | null;
  approved_at?: string | null;
  execution_authorized_at?: string | null;
  rejection_reason?: string | null;
};

export type ProvisioningStepRead = {
  id: string;
  step_key: string;
  ordinal: number;
  status: string;
  attempt_count: number;
  failure_category?: string | null;
  sanitized_error?: string | null;
  evidence_json: Record<string, unknown>;
  external_ref?: string | null;
  rollback_state: string;
};

export type ProvisioningJobDetailRead = {
  job_id: string;
  tenant_id: string;
  onboarding_request_id?: string | null;
  status: string;
  workflow_version: string;
  attempt_count: number;
  steps: ProvisioningStepRead[];
};

export type ProvisioningEventRead = {
  id: string;
  step_id: string;
  attempt: number;
  event_code: string;
  public_message: string;
  context_json: Record<string, unknown>;
  created_at: string;
};
