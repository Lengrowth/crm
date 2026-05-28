import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingIcon,
  MarketingPageCta,
  ScrollReveal,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Champion Well Drilling — Water Drilling Operations",
  description:
    "A field-ready CRM & ERP landing page for Champion Well Drilling covering drilling jobs, pump installs, water treatment, maintenance, inventory, and job costing.",
};

const services = [
  "Water well drilling for residential, commercial, and agricultural customers",
  "Pump installation, pressure tanks, and pressure switch service",
  "Water testing and water treatment system installs",
  "24/7 maintenance, leak response, and emergency service",
  "Directional drilling and below-frost-line water line installation",
];

const modules = [
  {
    icon: "building" as const,
    title: "CRM",
    description:
      "Capture quote requests, keep a customer history, and track every property, well, and service conversation in one place.",
  },
  {
    icon: "chart" as const,
    title: "Sales & Quotations",
    description:
      "Create estimates for new wells, pump replacements, water treatment work, and emergency service calls without rebuilding the same quote each time.",
  },
  {
    icon: "flag" as const,
    title: "Projects & Job Dispatch",
    description:
      "Turn every drilling or service request into a scheduled job with crew assignments, notes, checklists, and completion status.",
  },
  {
    icon: "eye" as const,
    title: "GPS Field Tracking",
    description:
      "Real-time location of crews, rigs, and vehicles. Automatic job site check-in and check-out so dispatch always has an accurate picture of who is where.",
  },
  {
    icon: "grid" as const,
    title: "QR Product Ordering",
    description:
      "Field workers scan a product QR code on site, submit an order from their phone, and Champion routes it to the right supplier at the right price.",
  },
  {
    icon: "layers" as const,
    title: "Inventory & Stock",
    description:
      "Track pumps, tanks, pipe, fittings, treatment parts, drilling supplies, and spare components so crews have what they need before they leave the yard.",
  },
  {
    icon: "shield" as const,
    title: "Procurement",
    description:
      "Reorder consumables, manage suppliers, and keep critical drilling and service stock available for both planned work and emergency calls.",
  },
  {
    icon: "chart" as const,
    title: "Accounting",
    description:
      "Connect job costing, invoicing, deposits, and accounts receivable so completed work turns into accurate financials faster.",
  },
  {
    icon: "spark" as const,
    title: "Reporting & Dashboards",
    description:
      "See job margin, open quotes, service response times, inventory movement, and crew productivity in real time.",
  },
];

const improvements = [
  {
    icon: "eye" as const,
    title: "Better visibility from office to field",
    description:
      "Office staff can see which jobs are scheduled, which crew is assigned, what parts are needed, and whether the job is complete.",
  },
  {
    icon: "clock" as const,
    title: "Faster response on service calls",
    description:
      "Emergency pump failures, low pressure issues, and water treatment problems can be logged, dispatched, and tracked without chasing paper notes.",
  },
  {
    icon: "bolt" as const,
    title: "Cleaner day-to-day job execution",
    description:
      "Crew checklists, inspection notes, and site photos keep every drilling and maintenance visit consistent and easier to hand off.",
  },
  {
    icon: "link" as const,
    title: "Connected job costing and invoicing",
    description:
      "Parts, labour, and job time flow into the invoice so Champion can bill accurately and understand the margin on each job type.",
  },
];

const implementation = [
  {
    num: "01",
    title: "Map Champion's workflows",
    description:
      "We start with drilling, pump installs, water testing, water treatment, maintenance, and emergency service so the system reflects how your team actually works.",
  },
  {
    num: "02",
    title: "Configure the core modules",
    description:
      "We set up CRM, quotations, jobs, inventory, procurement, accounting, and dashboards around your real services, parts, and approval flow.",
  },
  {
    num: "03",
    title: "Move the important data in",
    description:
      "Customers, sites, equipment, service history, and stock items are loaded so the team starts with useful records instead of an empty system.",
  },
  {
    num: "04",
    title: "Train office and field teams",
    description:
      "We run role-based training for dispatch, sales, service, and management so everyone knows exactly how to use the new process.",
  },
  {
    num: "05",
    title: "Launch in phases and refine",
    description:
      "We go live in a controlled rollout, then improve forms, reports, and automations based on what the team actually uses every day.",
  },
];

export default function ChampionWellDrillingPage() {
  return (
    <div className="space-y-16 lg:space-y-24">
      <MarketingCard
        className="relative overflow-hidden rounded-[2.5rem] px-8 py-14 sm:px-12 sm:py-16 lg:px-16 lg:py-20"
        tone="accent"
      >
        <div className="max-w-3xl">
          <p
            className="marketing-reveal text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            Champion Well Drilling
          </p>
          <h1
            className="marketing-reveal mt-5 text-5xl font-semibold tracking-[-0.06em] sm:text-6xl lg:text-7xl marketing-gradient-text"
            style={{ animationDelay: "60ms" }}
          >
            A field-ready CRM & ERP for water drilling operations.
          </h1>
          <p
            className="marketing-reveal mt-6 max-w-2xl text-lg leading-8"
            style={{ color: "var(--muted)", animationDelay: "120ms" }}
          >
            Designed around the way Champion Well Drilling works: new well
            drilling, pump installation, water testing, water treatment,
            emergency maintenance, and the office work that ties it all
            together.
          </p>
          <div
            className="marketing-reveal mt-8 flex flex-wrap gap-3"
            style={{ animationDelay: "180ms" }}
          >
            <MarketingButtonLink href="/demo">
              Book a discovery call
            </MarketingButtonLink>
            <MarketingButtonLink href="/contact" variant="secondary">
              Get in touch
            </MarketingButtonLink>
          </div>
        </div>
      </MarketingCard>

      <ScrollReveal>
        <section className="grid gap-12 lg:grid-cols-2 lg:items-start">
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              What Champion does
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              One operation. Many moving parts.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              Champion runs a full water service operation — new well drilling,
              pump systems, water testing, treatment, scheduled maintenance,
              emergency response, and directional drilling. Each service line
              has its own scheduling, parts, and billing needs.
            </p>
            <div className="mt-8 space-y-4">
              {services.map((item, i) => (
                <ScrollReveal key={item} delay={i * 0.07}>
                  <div className="flex items-start gap-4">
                    <span
                      className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border text-[color:var(--accent)]"
                      style={{
                        background:
                          "color-mix(in srgb, var(--accent) 8%, var(--surface))",
                        borderColor:
                          "color-mix(in srgb, var(--accent) 22%, var(--border))",
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

          <div className="marketing-panel rounded-[1.75rem] p-6 sm:p-8">
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              Day-to-day impact
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              Less chasing paper. More time on site.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              The goal is to make the office faster, crews better prepared, and
              jobs easier to close. That means fewer missed details, faster
              quotes, tighter stock control, and better visibility into every
              well, pump, and service call.
            </p>
            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              {improvements.map((item) => (
                <div
                  key={item.title}
                  className="rounded-[1.4rem] border p-4"
                  style={{
                    borderColor: "var(--border)",
                    background: "var(--surface-strong)",
                  }}
                >
                  <span className="flex h-9 w-9 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--accent)]" style={{ background: "var(--surface)" }}>
                    <MarketingIcon icon={item.icon} className="h-4 w-4" />
                  </span>
                  <h3
                    className="mt-4 text-sm font-semibold"
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
          </div>
        </section>
      </ScrollReveal>

      <div className="marketing-divider" />

      <ScrollReveal>
        <section>
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            Modules we would use
          </p>
          <h2
            className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
            style={{ color: "var(--text)" }}
          >
            One system for the office, the yard, and the field.
          </h2>
          <p
            className="mt-4 max-w-2xl text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            These are the core modules that would support Champion Well
            Drilling's quoting, dispatch, service history, job costing, and
            financial control.
          </p>

          <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 marketing-stagger">
            {modules.map((item, i) => (
              <ScrollReveal key={item.title} delay={i * 0.05}>
                <div className="marketing-module-card marketing-panel rounded-[1.75rem] p-6 h-full">
                  <span
                    className="flex h-10 w-10 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--accent)]"
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
              </ScrollReveal>
            ))}
          </div>
        </section>
      </ScrollReveal>

      <ScrollReveal>
        <section className="grid gap-6 lg:grid-cols-2">
          <div className="marketing-panel rounded-[1.75rem] p-6 sm:p-8">
            <span
              className="flex h-10 w-10 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--accent)]"
              style={{ background: "var(--surface-strong)" }}
            >
              <MarketingIcon icon="eye" className="h-5 w-5" />
            </span>
            <h3
              className="mt-4 text-xl font-semibold tracking-[-0.02em]"
              style={{ color: "var(--text)" }}
            >
              GPS field tracking
            </h3>
            <p className="mt-3 text-sm leading-6" style={{ color: "var(--muted)" }}>
              The office can see where every crew and rig is without making a
              phone call. Job site arrivals and departures are logged
              automatically, so dispatch knows who is available and how long
              each visit takes.
            </p>
            <ul className="mt-6 space-y-2.5">
              {[
                "Live map of all crews and vehicles",
                "Automatic check-in and check-out at job sites",
                "Route history for every service call",
                "Idle time and mileage visible to office and management",
              ].map((f) => (
                <li key={f} className="flex items-center gap-2.5">
                  <span
                    className="h-1.5 w-1.5 shrink-0 rounded-full"
                    style={{ background: "var(--accent)" }}
                  />
                  <span className="text-sm" style={{ color: "var(--muted)" }}>
                    {f}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <div className="marketing-panel rounded-[1.75rem] p-6 sm:p-8">
            <span
              className="flex h-10 w-10 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--accent)]"
              style={{ background: "var(--surface-strong)" }}
            >
              <MarketingIcon icon="grid" className="h-5 w-5" />
            </span>
            <h3
              className="mt-4 text-xl font-semibold tracking-[-0.02em]"
              style={{ color: "var(--text)" }}
            >
              QR code product ordering
            </h3>
            <p className="mt-3 text-sm leading-6" style={{ color: "var(--muted)" }}>
              Every product in the catalogue has a QR code. A field worker scans
              it on site, a lightweight mobile page opens, and they submit a
              parts or supply order directly from the field. Champion's team
              reviews the request, applies the right price for that customer or
              job, and routes the order to the correct supplier or partner.
            </p>
            <ul className="mt-6 space-y-2.5">
              {[
                "Mobile-first order page — scan, tap, done",
                "Variable pricing per customer, job type, or partner agreement",
                "Orders route automatically to the right supplier",
                "Full order status visible to office from request to delivery",
              ].map((f) => (
                <li key={f} className="flex items-center gap-2.5">
                  <span
                    className="h-1.5 w-1.5 shrink-0 rounded-full"
                    style={{ background: "var(--accent)" }}
                  />
                  <span className="text-sm" style={{ color: "var(--muted)" }}>
                    {f}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </section>
      </ScrollReveal>

      <div className="marketing-divider-accent" />

      <ScrollReveal>
        <section className="grid gap-12 lg:grid-cols-2 lg:items-start">
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              How we would implement it
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              A phased rollout built around Champion's actual work.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              We would not force a generic ERP process onto your team. Instead,
              we would shape the system around your drilling, pump, treatment,
              and service operations, then launch it in a controlled rollout so
              the business keeps moving while the new system comes online.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <MarketingButtonLink href="/contact">
                Get in touch
              </MarketingButtonLink>
              <MarketingButtonLink href="/demo" variant="secondary">
                See the platform in action
              </MarketingButtonLink>
            </div>
          </div>

          <div className="space-y-6">
            {implementation.map((item, i) => (
              <ScrollReveal key={item.num} delay={i * 0.08}>
                <div className="marketing-timeline-item">
                  <span className="marketing-step-num shrink-0">{item.num}</span>
                  <div className="pt-1.5">
                    <h3
                      className="font-semibold"
                      style={{ color: "var(--text)" }}
                    >
                      {item.title}
                    </h3>
                    <p
                      className="mt-1 text-sm leading-6"
                      style={{ color: "var(--muted)" }}
                    >
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
