import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingPageCta,
  MarketingSectionIntro,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Pricing",
  description:
    "Clear commercial packaging for pilot teams, operational rollouts, and implementation-heavy deployments using the LenQuant control plane.",
};

const plans = [
  {
    name: "Pilot",
    price: "From $99 / month",
    description:
      "For a single pilot workspace that needs the product surface, core workflows, and a clean place to manage rollout readiness.",
    highlights: [
      "One organization workspace",
      "Core SaaS control features",
      "Launch-oriented onboarding support",
      "Best for early pilots and internal validation",
    ],
  },
  {
    name: "Operations",
    price: "From $249 / month",
    description:
      "For teams packaging multiple modules, coordinating tenant operations, and needing a stronger control room around delivery.",
    highlights: [
      "Multiple modules and tenant records",
      "Implementation visibility",
      "Operational readiness tracking",
      "Best for active rollout conversations",
    ],
    featured: true,
  },
  {
    name: "Guided rollout",
    price: "Custom",
    description:
      "For implementation-led engagements where onboarding, data planning, environment preparation, and launch sequencing need direct support.",
    highlights: [
      "Commercial and implementation alignment",
      "Rollout planning and signoff support",
      "Tenant readiness and launch coordination",
      "Best for serious pilots and staged go-live work",
    ],
  },
];

const pricingNotes = [
  "ERPNext runtime cutover is not bundled as an automatic background step.",
  "Implementation support is scoped deliberately so teams know what is included and what is guided work.",
  "Pricing can be adapted for vertical depth, pilot scope, or multi-tenant rollout complexity.",
];

export default function PricingPage() {
  return (
    <div className="space-y-8 sm:space-y-10 lg:space-y-12">
      <MarketingCard
        className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10"
        tone="accent"
      >
        <MarketingSectionIntro
          eyebrow="Pricing"
          title="Commercial structure that matches how rollout work actually happens."
          description="LenQuant pricing keeps the SaaS product offer clear while leaving implementation-heavy work visible. You get a credible product package for pilots and a straightforward path into guided rollout conversations."
        />
      </MarketingCard>

      <div className="grid gap-5 lg:grid-cols-3">
        {plans.map((plan) => (
          <MarketingCard
            key={plan.name}
            className="rounded-[2rem] p-7"
            tone={plan.featured ? "accent" : "default"}
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <p
                  className="text-xs font-semibold uppercase tracking-[0.24em]"
                  style={{ color: "var(--muted)" }}
                >
                  {plan.featured ? "Recommended" : "Plan"}
                </p>
                <h2
                  className="mt-3 text-3xl font-semibold tracking-[-0.04em]"
                  style={{ color: "var(--text)" }}
                >
                  {plan.name}
                </h2>
              </div>
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
              className="mt-6 space-y-3 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {plan.highlights.map((item) => (
                <li key={item}>• {item}</li>
              ))}
            </ul>
            <div className="mt-7">
              <MarketingButtonLink
                href="/demo"
                variant={plan.featured ? "primary" : "secondary"}
              >
                Discuss this plan
              </MarketingButtonLink>
            </div>
          </MarketingCard>
        ))}
      </div>

      <section className="grid gap-6 lg:grid-cols-[1fr_0.95fr]">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            What is included
          </p>
          <h2
            className="mt-4 text-3xl font-semibold tracking-[-0.04em]"
            style={{ color: "var(--text)" }}
          >
            The subscription covers the control plane. Guided work is scoped
            openly.
          </h2>
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <div className="rounded-[1.5rem] border border-[color:var(--border)] bg-[color:var(--surface-strong)] p-5">
              <p
                className="text-sm font-semibold"
                style={{ color: "var(--text)" }}
              >
                Included in the product
              </p>
              <ul
                className="mt-3 space-y-2 text-sm leading-7"
                style={{ color: "var(--muted)" }}
              >
                <li>• Workspace, organization, and tenant administration</li>
                <li>• Module packaging and readiness visibility</li>
                <li>• Public-site and demo-led commercial flow</li>
              </ul>
            </div>
            <div className="rounded-[1.5rem] border border-[color:var(--border)] bg-[color:var(--surface-strong)] p-5">
              <p
                className="text-sm font-semibold"
                style={{ color: "var(--text)" }}
              >
                Scoped as guided rollout work
              </p>
              <ul
                className="mt-3 space-y-2 text-sm leading-7"
                style={{ color: "var(--muted)" }}
              >
                <li>• Implementation planning and rollout design</li>
                <li>• Tenant launch sequencing and coordination</li>
                <li>• ERPNext cutover work when the runtime path is ready</li>
              </ul>
            </div>
          </div>
        </MarketingCard>

        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="muted">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Pricing notes
          </p>
          <ul
            className="mt-5 space-y-4 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            {pricingNotes.map((item) => (
              <li
                key={item}
                className="rounded-[1.25rem] border border-[color:var(--border)] bg-[color:var(--surface)] px-4 py-4"
              >
                {item}
              </li>
            ))}
          </ul>
        </MarketingCard>
      </section>

      <MarketingPageCta />
    </div>
  );
}
