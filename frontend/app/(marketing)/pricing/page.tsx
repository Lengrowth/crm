import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Pricing",
  description:
    "Pilot-ready pricing for a SaaS control plane that manages onboarding, tenant operations, and ERPNext rollout preparation.",
};

const plans = [
  {
    name: "Starter",
    price: "$99 / month",
    description:
      "For a single pilot team that needs the SaaS shell, one production path, and implementation visibility.",
    highlights: [
      "1 organization workspace",
      "Core modules",
      "Demo and onboarding support",
    ],
  },
  {
    name: "Growth",
    price: "$249 / month",
    description:
      "For growing operations teams that need multiple modules, stronger tenant controls, and rollout coordination.",
    highlights: [
      "Multiple modules",
      "Tenant readiness tracking",
      "Operational support workflows",
    ],
    featured: true,
  },
  {
    name: "Pilot rollout",
    price: "Custom",
    description:
      "For implementation-heavy deployments where onboarding, migration planning, and environment readiness matter most.",
    highlights: [
      "Guided rollout plan",
      "Launch readiness review",
      "Custom onboarding path",
    ],
  },
];

export default function PricingPage() {
  return (
    <div className="space-y-8">
      <section className="max-w-3xl">
        <p
          className="text-xs font-semibold uppercase tracking-[0.24em]"
          style={{ color: "var(--muted)" }}
        >
          Pricing
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Simple launch pricing for pilot teams and early rollout engagements.
        </h1>
        <p className="mt-4 text-sm leading-7" style={{ color: "var(--muted)" }}>
          Pricing is positioned for demos, pilots, and guided implementations.
          Live billing-provider automation is a later phase, but the commercial
          story is ready for real conversations now.
        </p>
      </section>

      <div className="grid gap-6 lg:grid-cols-3">
        {plans.map((plan) => (
          <article
            key={plan.name}
            className="rounded-[2rem] border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: plan.featured
                ? "var(--surface-strong)"
                : "var(--surface)",
              boxShadow: plan.featured ? "0 24px 50px var(--shadow)" : "none",
            }}
          >
            <div className="flex items-baseline justify-between gap-4">
              <h2
                className="text-2xl font-semibold"
                style={{ color: "var(--text)" }}
              >
                {plan.name}
              </h2>
              <p
                className="text-sm font-semibold uppercase tracking-[0.2em]"
                style={{ color: "var(--muted)" }}
              >
                {plan.price}
              </p>
            </div>
            <p
              className="mt-4 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {plan.description}
            </p>
            <ul
              className="mt-4 space-y-2 text-sm leading-6"
              style={{ color: "var(--muted)" }}
            >
              {plan.highlights.map((item) => (
                <li key={item}>• {item}</li>
              ))}
            </ul>
            <Link
              href="/demo"
              className="mt-6 inline-flex rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface)",
                color: "var(--text)",
              }}
            >
              Discuss this plan
            </Link>
          </article>
        ))}
      </div>
    </div>
  );
}
