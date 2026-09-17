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
}

export interface ModuleBundle {
  id: string;
  bundle_key: string;
  version: number;
  name: string;
  description: string | null;
  source: string;
  modules: Array<{ code: string; name: string; sort_order: number }>;
}

export interface ModuleAudit {
  id: string;
  created_at: string;
  actor_user_id: string | null;
  organization_id: string;
  operation: string;
  previous_requested: Record<string, unknown>;
  new_requested: Record<string, unknown>;
  previous_effective: Record<string, unknown>;
  new_effective: Record<string, unknown>;
  source_type: string;
  source_ref: string | null;
  reason: string | null;
  idempotency_key: string;
  result: string;
}
