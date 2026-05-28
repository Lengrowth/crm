import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingIcon,
  MarketingIconBadge,
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
    <div className="space-y-10 lg:space-y-14">
      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr] lg:items-start">
        <MarketingCard
          className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10"
          tone="accent"
        >
          <MarketingSectionIntro
            eyebrow="Industries"
            title="Start with drilling. Expand with the same control model across operations-heavy teams."
            description="LenQuant is designed to feel specific, not vague. The first proof point is drilling, but the SaaS control layer is intentionally reusable across other implementation-heavy, field-led, and asset-aware operating models."
          />
          <div className="mt-6 flex flex-wrap gap-3">
            <MarketingIconBadge icon="shield" label="Vertical credibility" />
            <MarketingIconBadge icon="spark" label="Reusable control model" />
          </div>
        </MarketingCard>

        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default" interactive>
          <div className="flex items-start gap-4">
            <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-[color:var(--border)] bg-[color:var(--surface-strong)] text-[color:var(--text)]">
              <MarketingIcon icon="chart" className="h-5 w-5" />
            </span>
            <div>
              <p
                className="text-xs font-semibold uppercase tracking-[0.24em]"
                style={{ color: "var(--muted)" }}
              >
                Vertical strategy
              </p>
              <h2 className="mt-3 text-3xl font-semibold tracking-[-0.04em]" style={{ color: "var(--text)" }}>
                One flagship vertical should make the whole product feel more real.
              </h2>
            </div>
          </div>
          <p className="mt-5 text-sm leading-7" style={{ color: "var(--muted)" }}>
            A tight industry story helps the site avoid generic claims. Drilling leads, then the same operational language can extend into adjacent teams with similar rollout and visibility needs.
          </p>
        </MarketingCard>
      </section>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        {industries.map((industry) => (
          <MarketingCard
            key={industry.title}
            className="rounded-[1.75rem] p-6"
            tone="default"
            interactive
          >
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl border border-[color:var(--border)] bg-[color:var(--surface-strong)] text-[color:var(--text)]">
                <MarketingIcon icon="dot" className="h-4 w-4" />
              </span>
              <h2 className="text-xl font-semibold" style={{ color: "var(--text)" }}>
                {industry.title}
              </h2>
            </div>
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
          <div className="mt-5 space-y-3 text-sm leading-7" style={{ color: "var(--muted)" }}>
            {[
              "Keep the same account, tenant, and implementation model.",
              "Swap in vertical-fit modules and operating workflows.",
              "Preserve the runtime boundary so rollout stays deliberate.",
            ].map((item) => (
              <div key={item} className="flex items-start gap-3 rounded-[1.2rem] border border-[color:var(--border)] bg-[color:var(--surface)] px-4 py-4">
                <span className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-full border border-[color:var(--border)] text-[color:var(--text)]">
                  <MarketingIcon icon="shield" className="h-3.5 w-3.5" />
                </span>
                <p>{item}</p>
              </div>
            ))}
          </div>
        </MarketingCard>
      </section>

      <MarketingPageCta />
    </div>
  );
}
