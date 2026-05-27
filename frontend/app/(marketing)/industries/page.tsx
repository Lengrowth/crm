import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingPageCta,
  MarketingSectionIntro,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Industries",
  description:
    "LenQuant starts with drilling and extends the same control-plane model across other operations-heavy verticals without losing the SaaS-to-runtime boundary.",
};

const industries = [
  {
    title: "Drilling",
    description:
      "The flagship vertical: equipment-aware, field-heavy, implementation-sensitive, and a strong proving ground for the product model.",
  },
  {
    title: "Field operations",
    description:
      "Dispatch, crews, daily execution, and support workflows that need structure before and after rollout.",
  },
  {
    title: "Fleet and assets",
    description:
      "Operational teams that need vehicle, equipment, maintenance, and asset visibility inside a broader delivery workflow.",
  },
  {
    title: "Inventory-led operations",
    description:
      "Stock, materials, and fulfillment-sensitive teams where rollout success depends on operational readiness, not just software access.",
  },
];

export default function IndustriesPage() {
  return (
    <div className="space-y-8 sm:space-y-10 lg:space-y-12">
      <MarketingCard
        className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10"
        tone="accent"
      >
        <MarketingSectionIntro
          eyebrow="Industries"
          title="Start with drilling. Expand with the same control model across operations-heavy teams."
          description="LenQuant is designed to feel specific, not vague. The first proof point is drilling, but the SaaS control layer is intentionally reusable across other implementation-heavy, field-led, and asset-aware operating models."
        />
      </MarketingCard>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        {industries.map((industry) => (
          <MarketingCard
            key={industry.title}
            className="rounded-[1.75rem] p-6"
            tone="default"
          >
            <h2
              className="text-xl font-semibold"
              style={{ color: "var(--text)" }}
            >
              {industry.title}
            </h2>
            <p
              className="mt-3 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {industry.description}
            </p>
          </MarketingCard>
        ))}
      </div>

      <section className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Why drilling leads
          </p>
          <h2
            className="mt-4 text-3xl font-semibold tracking-[-0.04em]"
            style={{ color: "var(--text)" }}
          >
            A strong flagship vertical makes the product more believable
            everywhere else.
          </h2>
          <p
            className="mt-4 text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            Drilling combines field execution, equipment context, safety
            pressure, rollout complexity, and implementation depth. If the
            product story works there, it carries more authority into adjacent
            operational verticals.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <MarketingButtonLink href="/drilling">
              Explore drilling
            </MarketingButtonLink>
            <MarketingButtonLink href="/demo" variant="secondary">
              Book an industry demo
            </MarketingButtonLink>
          </div>
        </MarketingCard>

        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="muted">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Expansion logic
          </p>
          <ul
            className="mt-5 space-y-3 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            <li>• Keep the same account, tenant, and implementation model.</li>
            <li>• Swap in vertical-fit modules and operating workflows.</li>
            <li>
              • Preserve the ERP runtime boundary so rollout stays deliberate.
            </li>
          </ul>
        </MarketingCard>
      </section>

      <MarketingPageCta />
    </div>
  );
}
