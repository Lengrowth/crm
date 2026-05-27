export type OrganizationStatus = "lead" | "trial" | "active" | "suspended" | "cancelled" | "archived";

export interface OrganizationSummary {
  id: string;
  name: string;
  legalName: string | null;
  industry: string | null;
  country: string | null;
  timezone: string | null;
  billingEmail: string | null;
  status: OrganizationStatus;
  createdAt: string;
  updatedAt: string;
}

export interface OrganizationDraft {
  name: string;
  legalName?: string | null;
  industry?: string | null;
  country?: string | null;
  timezone?: string | null;
  billingEmail?: string | null;
  status?: OrganizationStatus;
}
