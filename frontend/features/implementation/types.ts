export interface PortfolioTask { id: string; title: string; status: string; due_date: string | null; }
export interface PortfolioProject {
  id: string; organization_id: string; organization_name: string; tenant_id: string; tenant_slug: string;
  status: string; target_go_live_date: string | null; task_count: number; completed_task_count: number;
  progress_percent: number; blocker_count: number; overdue_task_count: number; tasks: PortfolioTask[]; tasks_truncated: boolean;
}
export interface ImplementationPortfolio { generated_at: string; project_count: number; blocker_count: number; overdue_task_count: number; truncated: boolean; projects: PortfolioProject[]; }
