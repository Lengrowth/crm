import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingPageCta,
  MarketingSectionIntro,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Drilling",
  description:
    "Explore LenQuant's flagship drilling story: a control plane for onboarding, field execution readiness, tenant preparation, and implementation visibility around ERPNext-backed operations.",
};

const drillingWorkflows = [
  "Daily field reporting and job progress visibility",
  "Crew coordination and dispatcher handoff",
  "Equipment checks, inspections, and readiness status",
  "Safety-sensitive rollout planning and operator signoff",
];

const drillingOutcomes = [
  {
    title: "More credible pilot conversations",
    description:
      "The product feels tailored to drilling operations instead of sounding like generic ERP language with a new logo.",
  },
  {
    title: "Stronger implementation discipline",
    description:
      "Teams can map the rollout, the tenant setup, and the operational model before runtime cutover becomes a risk.",
  },
  {
    title: "Clearer customer trust",
    description:
      "Operators can see that the platform understands field reality, not just software abstractions.",
  },
];

export default function DrillingPage() {
  return (
    <div className="space-y-8 sm:space-y-10 lg:space-y-12">
      <MarketingCard
        className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10"
        tone="accent"
      >
        <MarketingSectionIntro
          eyebrow="Flagship vertical"
          title="A drilling-specific rollout story with field-ready structure and a cleaner product boundary."
          description="LenQuant starts with drilling because the operational reality is demanding: crews, equipment, safety, dispatch pressure, and implementation complexity all need visibility before go-live."
        />
      </MarketingCard>

      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Why this vertical fits first
          </p>
          <h2
            className="mt-4 text-3xl font-semibold tracking-[-0.04em]"
            style={{ color: "var(--text)" }}
          >
            Drilling forces the product to be operationally honest.
          </h2>
          <p
            className="mt-4 text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            If a platform can support the planning, visibility, and launch
            discipline that drilling teams expect, it earns the right to expand
            into adjacent industries with confidence.
          </p>
        </MarketingCard>

        <div className="grid gap-4 sm:grid-cols-2">
          {drillingWorkflows.map((workflow) => (
            <MarketingCard
              key={workflow}
              className="rounded-[1.75rem] p-5"
              tone="muted"
            >
              <p
                className="text-sm font-semibold leading-6"
                style={{ color: "var(--text)" }}
              >
                {workflow}
              </p>
            </MarketingCard>
          ))}
        </div>
      </section>

      <div className="grid gap-5 lg:grid-cols-3">
        {drillingOutcomes.map((item) => (
          <MarketingCard
            key={item.title}
            className="rounded-[1.75rem] p-6"
            tone="default"
          >
            <h3
              className="text-xl font-semibold"
              style={{ color: "var(--text)" }}
            >
              {item.title}
            </h3>
            <p
              className="mt-3 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {item.description}
            </p>
          </MarketingCard>
        ))}
      </div>

      <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <p
              className="text-xs font-semibold uppercase tracking-[0.24em]"
              style={{ color: "var(--muted)" }}
            >
              Operational takeaway
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em]"
              style={{ color: "var(--text)" }}
            >
              The public story, the rollout workflow, and the runtime plan all
              become easier to trust when drilling is presented intentionally.
            </h2>
          </div>
          <div className="flex flex-wrap gap-3">
            <MarketingButtonLink href="/demo">
              Request a drilling demo
            </MarketingButtonLink>
            <MarketingButtonLink href="/contact" variant="secondary">
              Discuss rollout fit
            </MarketingButtonLink>
          </div>
        </div>
      </MarketingCard>

      <MarketingPageCta />
    </div>
  );
}
