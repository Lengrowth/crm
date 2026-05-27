export interface BillingSummary {
  planName: string;
  subscriptionStatus: "trialing" | "active" | "past_due" | "cancelled" | "unpaid" | "manual";
  monthlyPriceCents: number;
  renewalDate?: string;
}
