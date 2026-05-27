import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingPageCta,
  MarketingSectionIntro,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Modules",
  description:
    "See how LenQuant packages CRM, field operations, drilling, inventory, reporting, and rollout visibility into a reusable control-plane product model.",
};

const modules = [
  {
    title: "CRM",
    description:
      "Keep customer, account, and commercial visibility inside the SaaS layer instead of scattering it across implementation notes.",
  },
  {
    title: "Field Ops",
    description:
      "Support job coordination, execution flow, and operator visibility for teams running work outside the office.",
  },
  {
    title: "Drilling",
    description:
      "Start with a flagship vertical that needs clear daily workflows, equipment context, and launch discipline.",
  },
  {
    title: "Inventory",
    description:
      "Manage materials, stock-sensitive workflows, and readiness signals that affect deployment success.",
  },
  {
    title: "Reporting",
    description:
      "Make operational progress, support health, and implementation posture visible to leadership and delivery teams.",
  },
  {
    title: "White label and domains",
    description:
      "Prepare branded tenant experiences, domain operations, and rollout-specific customer presentation from one product surface.",
  },
];

export default function ModulesPage() {
  return (
    <div className="space-y-8 sm:space-y-10 lg:space-y-12">
      <MarketingCard
        className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10"
        tone="accent"
      >
        <MarketingSectionIntro
          eyebrow="Modules"
          title="A module system that supports repeatable delivery and stronger product packaging."
          description="Modules are not just a list of features. In LenQuant, they shape the commercial offer, the implementation plan, and the readiness model before anything reaches the ERP runtime."
        />
      </MarketingCard>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {modules.map((module) => (
          <MarketingCard
            key={module.title}
            className="rounded-[1.85rem] p-6"
            tone="default"
          >
            <h2
              className="text-2xl font-semibold tracking-[-0.03em]"
              style={{ color: "var(--text)" }}
            >
              {module.title}
            </h2>
            <p
              className="mt-3 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {module.description}
            </p>
          </MarketingCard>
        ))}
      </div>

      <section className="grid gap-6 lg:grid-cols-[1fr_0.95fr]">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Why the module model matters
          </p>
          <h2
            className="mt-4 text-3xl font-semibold tracking-[-0.04em]"
            style={{ color: "var(--text)" }}
          >
            Product packaging, implementation flow, and rollout coordination
            stay aligned.
          </h2>
          <ul
            className="mt-5 space-y-3 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            <li>
              • Teams can package the right offer for each customer without
              losing clarity.
            </li>
            <li>
              • Operators can see what is included, what is staged, and what
              still needs launch work.
            </li>
            <li>
              • ERPNext configuration remains the runtime expression of the
              product, not the only place the product exists.
            </li>
          </ul>
        </MarketingCard>

        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="muted">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Next actions
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <MarketingButtonLink href="/demo">
              See the module story live
            </MarketingButtonLink>
            <MarketingButtonLink href="/industries" variant="secondary">
              Match modules to industries
            </MarketingButtonLink>
          </div>
        </MarketingCard>
      </section>

      <MarketingPageCta />
    </div>
  );
}
