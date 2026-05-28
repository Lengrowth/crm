import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingIcon,
  MarketingPageCta,
  ScrollReveal,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Drilling — LenERP",
  description:
    "LenERP is purpose-built for drilling companies. Manage daily field reports, rig operations, crew coordination, inventory, and finance in one connected platform.",
};

const workflows = [
  "Daily drilling reports: bit records, mud logs, and footage progress",
  "Crew coordination, shift handover, and dispatcher visibility",
  "Equipment checks, rig inspections, and maintenance scheduling",
  "Real-time cost tracking against AFE and job budgets",
];

const outcomes = [
  {
    icon: "flag" as const,
    title: "Real-time field visibility",
    description:
      "Office and management see live job progress, crew status, and equipment location without chasing daily reports.",
  },
  {
    icon: "eye" as const,
    title: "Cost control from spud to TD",
    description:
      "Track drilling costs against AFE in real time. Catch overruns early and close jobs with accurate financials.",
  },
  {
    icon: "shield" as const,
    title: "Built for how rigs actually operate",
    description:
      "Workflows match the daily rhythm of drilling operations — not generic software forced onto field teams.",
  },
];

export default function DrillingPage() {
  return (
    <div className="space-y-16 lg:space-y-24">
      {/* Hero */}
      <MarketingCard
        className="relative overflow-hidden rounded-[2.5rem] px-8 py-14 sm:px-12 sm:py-16 lg:px-16 lg:py-20"
        tone="accent"
      >
        <div className="max-w-2xl">
          <p
            className="marketing-reveal text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            Flagship vertical
          </p>
          <h1
            className="marketing-reveal mt-5 text-5xl font-semibold tracking-[-0.06em] sm:text-6xl lg:text-7xl marketing-gradient-text"
            style={{ animationDelay: "60ms" }}
          >
            The CRM & ERP built for drilling companies.
          </h1>
          <p
            className="marketing-reveal mt-6 max-w-xl text-lg leading-8"
            style={{ color: "var(--muted)", animationDelay: "120ms" }}
          >
            Run your entire drilling business in one platform — CRM,
            daily reports, crew coordination, inventory, and finance
            connected from first job to final invoice.
          </p>
          <div
            className="marketing-reveal mt-8 flex flex-wrap gap-3"
            style={{ animationDelay: "180ms" }}
          >
            <MarketingButtonLink href="/demo">
              Request a drilling demo
            </MarketingButtonLink>
            <MarketingButtonLink href="/contact" variant="secondary">
              Get in touch
            </MarketingButtonLink>
          </div>
        </div>
      </MarketingCard>

      {/* Field workflows + why it matters */}
      <ScrollReveal>
        <section className="grid gap-10 lg:grid-cols-2 lg:items-start">
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              Field workflows
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              Visibility that matches how drilling teams actually work.
            </h2>
            <div className="mt-8 space-y-4">
              {workflows.map((item, i) => (
                <ScrollReveal key={item} delay={i * 0.07}>
                  <div className="flex items-start gap-4">
                    <span
                      className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border text-[color:var(--accent)]"
                      style={{
                        background: "color-mix(in srgb, var(--accent) 8%, var(--surface))",
                        borderColor: "color-mix(in srgb, var(--accent) 22%, var(--border))",
                      }}
                    >
                      <MarketingIcon icon="check" className="h-3.5 w-3.5" />
                    </span>
                    <p
                      className="text-sm leading-6"
                      style={{ color: "var(--text)" }}
                    >
                      {item}
                    </p>
                  </div>
                </ScrollReveal>
              ))}
            </div>
          </div>

          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              Why it works
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              Every part of the operation, connected.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              From the drill floor to the finance team — LenERP connects
              field data, job progress, inventory, and costs so nothing falls
              through the gap between operations and the office.
            </p>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              When a drilling report is filed, costs update. When a job closes,
              the invoice is ready. No spreadsheets, no manual consolidation.
            </p>
          </div>
        </section>
      </ScrollReveal>

      {/* Outcomes */}
      <ScrollReveal>
        <div className="grid gap-5 lg:grid-cols-3 marketing-stagger">
          {outcomes.map((item) => (
            <div
              key={item.title}
              className="marketing-module-card marketing-panel rounded-[1.75rem] p-6"
            >
              <span
                className="marketing-module-icon flex h-10 w-10 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--accent)]"
                style={{ background: "var(--surface-strong)" }}
              >
                <MarketingIcon icon={item.icon} className="h-5 w-5" />
              </span>
              <h3
                className="mt-4 text-lg font-semibold tracking-[-0.02em]"
                style={{ color: "var(--text)" }}
              >
                {item.title}
              </h3>
              <p
                className="mt-2 text-sm leading-6"
                style={{ color: "var(--muted)" }}
              >
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </ScrollReveal>

      <MarketingPageCta />
    </div>
  );
}
