import Link from "next/link";
import { InfoCard } from "@/components/InfoCard";

export default function AppHomePage() {
  return (
    <div className="space-y-6">
      <section
        className="overflow-hidden rounded-[2rem] border p-8 lg:p-10"
        style={{
          borderColor: "var(--border)",
          backgroundColor: "var(--surface)",
          boxShadow: "0 24px 60px var(--shadow)",
        }}
      >
        <div className="max-w-3xl">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Overview
          </p>
          <h2
            className="mt-4 text-4xl font-semibold tracking-tight"
            style={{ color: "var(--text)" }}
          >
            One control room for customer onboarding, tenant visibility, and
            launch readiness.
          </h2>
          <p
            className="mt-4 max-w-2xl text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            Use the protected app to review organizations, inspect tenants,
            coordinate rollout work, and prepare the operational layer for a
            clean ERPNext cutover.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              href="/app/organizations"
              className="rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
              style={{
                backgroundColor: "var(--accent)",
                color: "var(--accent-foreground)",
                boxShadow: "0 16px 32px var(--shadow)",
              }}
            >
              Review organizations
            </Link>
            <Link
              href="/app/tenants"
              className="rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
            >
              Inspect tenants
            </Link>
          </div>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-3">
        <InfoCard
          eyebrow="Customer ops"
          title="Organizations first"
          description="Track accounts, ownership, status, and rollout context before environment-level work begins."
        />
        <InfoCard
          eyebrow="Tenant control"
          title="Clear environment visibility"
          description="Review tenant environments, provisioning posture, and domain information from the SaaS layer."
        />
        <InfoCard
          eyebrow="Cutover safety"
          title="Mock stays explicit"
          description="Local demos can keep mock ERPNext behavior, while production-like environments avoid silent mock fallback."
        />
      </div>
    </div>
  );
}
