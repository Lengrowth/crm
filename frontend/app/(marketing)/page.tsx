import type { Metadata } from "next";
import Link from "next/link";
import { PlaceholderCard } from "@/components/PlaceholderCard";

export const metadata: Metadata = {
  title: "ERP rollout control without losing the SaaS boundary",
  description:
    "Show leads and pilot clients a launch-ready control plane for onboarding, tenant operations, implementation visibility, and safe ERPNext rollout preparation.",
};

export default function HomePage() {
  return (
    <div className="space-y-8">
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
            SaaS Control Plane
          </p>
          <h1
            className="mt-4 text-4xl font-semibold tracking-tight lg:text-5xl"
            style={{ color: "var(--text)" }}
          >
            Control onboarding, tenants, and rollout readiness before live
            ERPNext cutover.
          </h1>
          <p
            className="mt-5 max-w-2xl text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            This platform owns the commercial and operational control layer:
            public website, authentication, organizations, tenants, modules,
            implementation tracking, and provisioning visibility. ERPNext
            remains the external tenant runtime and will be connected later
            through an explicit cutover path.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              href="/demo"
              className="rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
              style={{
                backgroundColor: "var(--accent)",
                color: "var(--accent-foreground)",
                boxShadow: "0 16px 32px var(--shadow)",
              }}
            >
              Request a demo
            </Link>
            <Link
              href="/pricing"
              className="rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
            >
              View pricing
            </Link>
            <Link
              href="/login"
              className="rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
            >
              Sign in
            </Link>
          </div>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-3">
        <PlaceholderCard
          eyebrow="Commercial control"
          title="Own the customer relationship"
          description="Track organizations, plans, modules, billing posture, and implementation status from one SaaS control layer."
        />
        <PlaceholderCard
          eyebrow="Operational visibility"
          title="Keep rollout work visible"
          description="Coordinate tenant readiness, provisioning status, white-label preparation, and onboarding milestones before launch."
        />
        <PlaceholderCard
          eyebrow="Safe boundary"
          title="Keep ERPNext external"
          description="Demo and pilot flows can use mock integration locally, while production-like environments stay protected from silent mock fallback."
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        <section
          className="rounded-[2rem] border p-8"
          style={{
            borderColor: "var(--border)",
            backgroundColor: "var(--surface-strong)",
          }}
        >
          <h2
            className="text-2xl font-semibold"
            style={{ color: "var(--text)" }}
          >
            What teams can manage from day one
          </h2>
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            {[
              "Organizations and SaaS users",
              "Tenant environments and domains",
              "Module catalog and entitlements",
              "Implementation milestones and handoff readiness",
              "Provisioning records and support visibility",
              "Billing state and launch operations",
            ].map((item) => (
              <div
                key={item}
                className="rounded-2xl border px-4 py-4 text-sm"
                style={{
                  borderColor: "var(--border)",
                  backgroundColor: "var(--surface)",
                }}
              >
                {item}
              </div>
            ))}
          </div>
        </section>
        <section
          className="rounded-[2rem] border p-8"
          style={{
            borderColor: "var(--border)",
            backgroundColor: "var(--surface-strong)",
            boxShadow: "0 18px 40px var(--shadow)",
          }}
        >
          <p
            className="text-xs font-semibold uppercase tracking-[0.2em]"
            style={{ color: "var(--muted)" }}
          >
            Pilot launch fit
          </p>
          <p
            className="mt-4 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            The current product is ready for serious launch demos and pilot
            conversations. It does not yet perform the live ERPNext cutover, but
            it does give operators and clients a clear view of how the SaaS
            layer will own onboarding, access, tenant metadata, and rollout
            coordination.
          </p>
        </section>
      </div>
    </div>
  );
}
