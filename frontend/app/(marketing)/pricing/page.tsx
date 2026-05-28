import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingIcon,
  MarketingPageCta,
  ScrollReveal,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Pricing — LenERP",
  description:
    "LenERP is an enterprise CRM & ERP platform. Pricing is custom and includes implementation, onboarding, and ongoing support. Contact us to get started.",
};

const included = [
  "Full CRM & ERP platform (all modules)",
  "Accounting, sales, procurement, inventory, and manufacturing",
  "Projects, POS, quality, support, and field operations",
  "Custom domain and white-label branding",
  "Dedicated implementation and onboarding",
  "Data migration and historical import",
  "Training for your team",
  "Ongoing support and platform updates",
  "Reporting and management dashboards",
  "Multi-currency and global tax compliance",
];

export default function PricingPage() {
  return (
    <div className="space-y-16 lg:space-y-24">
      {/* Hero */}
      <div className="max-w-2xl">
        <p
          className="marketing-reveal text-xs font-semibold uppercase tracking-[0.28em]"
          style={{ color: "var(--accent)" }}
        >
          Pricing
        </p>
        <h1
          className="marketing-reveal mt-4 text-5xl font-semibold tracking-[-0.05em] sm:text-6xl"
          style={{ color: "var(--text)", animationDelay: "60ms" }}
        >
          One plan. Everything included.
        </h1>
        <p
          className="marketing-reveal mt-5 max-w-lg text-lg leading-8"
          style={{ color: "var(--muted)", animationDelay: "120ms" }}
        >
          LenERP is an enterprise product. Every engagement covers the full
          platform — all modules, all industries — plus implementation,
          onboarding, and ongoing support scoped to your business.
        </p>
      </div>

      {/* Single enterprise card — full width two-column */}
      <ScrollReveal>
        <MarketingCard className="rounded-[2rem] p-8 sm:p-10 lg:p-12" tone="accent">
          <div className="grid gap-10 lg:grid-cols-[1fr_1.4fr] lg:items-start">
            {/* Left: identity + CTA */}
            <div className="flex flex-col">
              <p
                className="text-xs font-semibold uppercase tracking-[0.24em]"
                style={{ color: "var(--accent)" }}
              >
                Enterprise
              </p>
              <h2
                className="mt-4 text-4xl font-semibold sm:text-5xl"
                style={{ color: "var(--text)" }}
              >
                Custom pricing
              </h2>
              <p
                className="mt-2 text-sm"
                style={{ color: "var(--muted)" }}
              >
                Quoted per engagement
              </p>
              <p
                className="mt-6 text-sm leading-7"
                style={{ color: "var(--muted)" }}
              >
                A single commercial agreement covering the software, a
                dedicated implementation, and your team&apos;s ongoing support. No
                hidden extras — what you see in the platform is what you get.
              </p>
              <div className="mt-8">
                <MarketingButtonLink href="/demo" variant="primary">
                  Talk to us
                </MarketingButtonLink>
              </div>
            </div>

            {/* Right: feature checklist */}
            <div
              className="rounded-2xl p-6 sm:p-8"
              style={{
                background: "color-mix(in srgb, var(--accent) 5%, var(--surface-strong))",
                border: "1px solid color-mix(in srgb, var(--accent) 16%, var(--border))",
              }}
            >
              <p
                className="text-xs font-semibold uppercase tracking-[0.22em] mb-5"
                style={{ color: "var(--accent)" }}
              >
                Everything included
              </p>
              <ul className="grid gap-3 sm:grid-cols-2">
                {included.map((item) => (
                  <li key={item} className="flex items-start gap-3">
                    <span
                      className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded"
                      style={{
                        background: "color-mix(in srgb, var(--accent) 16%, var(--surface))",
                        border: "1px solid color-mix(in srgb, var(--accent) 30%, var(--border))",
                        color: "var(--accent)",
                      }}
                    >
                      <MarketingIcon icon="check" className="h-3 w-3" />
                    </span>
                    <span className="text-sm leading-6" style={{ color: "var(--muted)" }}>
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </MarketingCard>
      </ScrollReveal>

      <div className="marketing-divider-accent" />

      {/* Why enterprise */}
      <ScrollReveal>
        <section className="grid gap-10 lg:grid-cols-2 lg:items-center">
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              Why enterprise
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              A CRM & ERP is not a subscription. It’s a transformation.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              Getting your business onto a modern CRM and ERP requires real
              implementation work — data migration, process design, training,
              and cutover. We include all of that because doing it right is
              the only way the platform delivers value.
            </p>
          </div>

          <div className="space-y-5">
            {[
              {
                icon: "spark" as const,
                title: "Implementation included",
                description:
                  "We scope, plan, and deliver the full rollout — not just a licence key.",
              },
              {
                icon: "shield" as const,
                title: "No hidden scope",
                description:
                  "Everything is agreed upfront. Data migration, training, and go-live support are part of the deal.",
              },
              {
                icon: "chart" as const,
                title: "Ongoing partnership",
                description:
                  "Platform updates, support, and expansion modules are included in your continued engagement.",
              },
            ].map((item, i) => (
              <ScrollReveal key={item.title} delay={i * 0.08}>
                <div className="flex items-start gap-4">
                  <span
                    className="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--accent)]"
                    style={{ background: "var(--surface)" }}
                  >
                    <MarketingIcon icon={item.icon} className="h-4 w-4" />
                  </span>
                  <div>
                    <h3 className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                      {item.title}
                    </h3>
                    <p className="mt-1 text-sm leading-6" style={{ color: "var(--muted)" }}>
                      {item.description}
                    </p>
                  </div>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </section>
      </ScrollReveal>

      <MarketingPageCta />
    </div>
  );
}
