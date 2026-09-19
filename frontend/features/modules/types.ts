export interface ModuleSummary {
  id: string;
  code: string;
  name: string;
  category: string | null;
  description?: string | null;
  public_description?: string | null;
  internal_description?: string | null;
  is_active: boolean;
  is_marketed: boolean;
  display_order: number;
  dependency_codes: string[];
  incompatibility_codes: string[];
  required_app?: string | null;
  administrative_visibility: string;
  alias_of?: string | null;
}

export interface ModuleEffectiveItem {
  code: string;
  name: string;
  category: string | null;
  requested: boolean;
  entitled: boolean;
  marketed: boolean;
  explicit: boolean;
  source: string[];
  explanation: string[];
  application_state: "not_applicable" | "pending" | "applied" | "failed";
  verification_state: "pending" | "verified" | "failed";
  tenant_states: Array<Record<string, unknown>>;
  dependency_codes: string[];
  required_app?: string | null;
  minimum_app_version?: string | null;
  compatible_app_version?: string | null;
  states: Array<"requested" | "entitled" | "applied" | "verified" | "hidden" | "needs_attention">;
  state_reasons: string[];
  hidden: boolean;
  needs_attention: boolean;
}

export interface ModuleEffective {
  organization_id: string;
  requested_codes: string[];
  effective_codes: string[];
  items: ModuleEffectiveItem[];
  warnings: string[];
  generated_at: string;
}

export interface ModulePreview {
  organization_id: string;
  requested_enable_codes: string[];
  requested_disable_codes: string[];
  requested_clear_codes: string[];
  dependency_additions: string[];
  dependency_removals: string[];
  conflicts: string[];
  effective: ModuleEffective;
  warnings: string[];
  preview_hash: string;
  is_current: boolean;
  bundle_key?: string | null;
  bundle_version?: number | null;
  required_applications: string[];
  platform_required_applications?: string[];
  affected_tenants: Array<{ tenant_id: string; tenant_slug: string; environment: string; status: string; provisioning_status: string }>;
}

export interface ModuleBundle {
  id: string;
  bundle_key: string;
  version: number;
  name: string;
  description: string | null;
  source: string;
  modules: Array<{ code: string; name: string; sort_order: number; dependency_codes: string[]; required_app?: string | null; minimum_app_version?: string | null; compatible_app_version?: string | null }>;
  supersedes_version?: number | null;
  added_module_codes: string[];
  removed_module_codes: string[];
}

export interface ModuleAudit {
  id: string;
  created_at: string;
  actor_user_id: string | null;
  organization_id: string;
  tenant_id?: string | null;
  tenant_ids: string[];
  operation: string;
  previous_requested: Record<string, unknown>;
  new_requested: Record<string, unknown>;
  previous_effective: Record<string, unknown>;
  new_effective: Record<string, unknown>;
  source_type: string;
  source_ref: string | null;
  previous_bundle_key?: string | null;
  previous_bundle_version?: number | null;
  new_bundle_key?: string | null;
  new_bundle_version?: number | null;
  reason: string | null;
  idempotency_key: string;
  result: string;
}
