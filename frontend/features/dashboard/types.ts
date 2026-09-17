export interface DashboardAction { label: string; href: string; tone: "info" | "warning" | "danger" | "success"; }
export interface DashboardSummary {
  generated_at: string;
  organization_count: number;
  organization_status_counts: Record<string, number>;
  tenant_count: number;
  tenant_status_counts: Record<string, number>;
  provisioning_status_counts: Record<string, number>;
  failed_job_count: number;
  provisioning_failures: Array<{ id: string; tenant_slug: string | null; status: string | null; updated_at: string | null }>;
  implementation_blocker_count: number;
  overdue_task_count: number;
  domain_warning_count: number;
  domain_warnings: Array<{ id: string; domain: string | null; tenant_slug: string | null; status: string | null; ssl_status: string | null }>;
  next_actions: DashboardAction[];
}
