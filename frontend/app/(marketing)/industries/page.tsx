import type { Metadata } from "next";
import Image from "next/image";
import {
  MarketingButtonLink,
  MarketingIcon,
  MarketingPageCta,
  ScrollReveal,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Industries — LenERP",
  description:
    "LenERP works out of the box for manufacturing, distribution, services, retail, construction, field operations, and more. One ERP for any industry.",
};

const industries = [
  {
    icon: "bolt" as const,
    title: "Manufacturing",
    image: "/industry-manufacturing.png",
    description:
      "Multi-level BOM, production planning, work orders, job cards, subcontracting, quality checks, and manufacturing reports — end-to-end control of your production floor.",
  },
  {
    icon: "layers" as const,
    title: "Distribution & Wholesale",
    image: "/industry-distribution.png",
    description:
      "Order-to-cash, stock control across multiple warehouses, supplier management, serial and batch tracking, and real-time inventory visibility.",
  },
  {
    icon: "building" as const,
    title: "Services & Consulting",
    image: "/industry-services.webp",
    description:
      "Project tracking, timesheets, revenue recognition, expense management, and invoicing — all connected so every billable hour is captured.",
  },
  {
    icon: "grid" as const,
    title: "Retail & Point of Sale",
    image: "/pos-main.webp",
    description:
      "Cloud-based multi-store POS, shift management, stock replenishment, customer loyalty, and integrated accounting for retail businesses.",
  },
  {
    icon: "shield" as const,
    title: "Construction & Projects",
    image: "/projects-overview.png",
    description:
      "Project-based costing, procurement, subcontractor management, equipment tracking, and real-time budget vs. actual reporting.",
  },
  {
    icon: "flag" as const,
    title: "Field Operations & Drilling",
    image: "/manufacturing-job-card.webp",
    description:
      "Job dispatch, crew management, daily field reports, rig management, equipment tracking, and cost visibility for teams working in the field.",
  },
  {
    icon: "clock" as const,
    title: "Fleet & Asset Management",
    image: "/reports.png",
    description:
      "Vehicle tracking, maintenance scheduling, equipment history, asset utilisation reports, and depreciation management across your entire fleet.",
  },
  {
    icon: "spark" as const,
    title: "Education & Non-profit",
    image: "/industry-education.jpg",
    description:
      "Admissions, fee management, course tracking, donor management, grant tracking, and financial reporting for schools and non-profit organisations.",
  },
];

export default function IndustriesPage() {
  return (
    <div className="space-y-16 lg:space-y-24">
      {/* Hero */}
      <div className="max-w-2xl">
        <p
          className="marketing-reveal text-xs font-semibold uppercase tracking-[0.28em]"
          style={{ color: "var(--accent)" }}
        >
          Industries
        </p>
        <h1
          className="marketing-reveal mt-4 text-5xl font-semibold tracking-[-0.05em] sm:text-6xl"
          style={{ color: "var(--text)", animationDelay: "60ms" }}
        >
          Works out of the box for almost any industry.
        </h1>
        <p
          className="marketing-reveal mt-5 max-w-lg text-lg leading-8"
          style={{ color: "var(--muted)", animationDelay: "120ms" }}
        >
          LenERP is a comprehensive ERP that adapts to how your business
          works — whether you manufacture, distribute, service clients, run
          retail locations, or operate in the field.
        </p>
      </div>

      {/* Industry grid — with images */}
      <ScrollReveal>
        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-4 marketing-stagger">
          {industries.map((item) => (
            <div
              key={item.title}
              className="marketing-industry-card marketing-panel rounded-[1.75rem] overflow-hidden flex flex-col"
            >
              {item.image ? (
                <div className="h-36 overflow-hidden">
                  <Image
                    src={item.image}
                    alt={item.title}
                    width={400}
                    height={240}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                </div>
              ) : null}
              <div className="p-6 flex flex-col flex-1">
                <span
                  className="marketing-industry-icon flex h-10 w-10 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--text)]"
                  style={{ background: "var(--surface-strong)" }}
                >
                  <MarketingIcon icon={item.icon} className="h-5 w-5" />
                </span>
                <h2
                  className="mt-4 text-xl font-semibold tracking-[-0.02em]"
                  style={{ color: "var(--text)" }}
                >
                  {item.title}
                </h2>
                <p
                  className="mt-2 text-sm leading-6"
                  style={{ color: "var(--muted)" }}
                >
                  {item.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </ScrollReveal>

      <div className="marketing-divider" />

      {/* ── Manufacturing featured ─────────────────────────── */}
      <ScrollReveal>
        <section className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              Manufacturing
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              Production control from BOM to delivery.
            </h2>
            <p className="mt-4 text-base leading-7" style={{ color: "var(--muted)" }}>
              Run complex production schedules with multi-level bills of
              materials, work orders, job cards, and subcontracting — all linked
              to live stock levels and supplier lead times so every order ships
              on time.
            </p>
            <ul className="mt-6 space-y-2.5">
              {["Multi-level BOM & routing", "Production scheduling", "Work orders & job cards", "Subcontracting", "Manufacturing reports & KPIs"].map((f) => (
                <li key={f} className="flex items-center gap-2.5">
                  <span className="h-1.5 w-1.5 rounded-full shrink-0" style={{ background: "var(--accent)" }} />
                  <span className="text-sm" style={{ color: "var(--muted)" }}>{f}</span>
                </li>
              ))}
            </ul>
            <div className="mt-8">
              <MarketingButtonLink href="/demo">Book a manufacturing demo</MarketingButtonLink>
            </div>
          </div>
          <div className="overflow-hidden rounded-2xl border" style={{ borderColor: "var(--border)" }}>
            <Image
              src="/manufacturing-capacity.webp"
              alt="Manufacturing — capacity planning dashboard"
              width={760}
              height={500}
              className="w-full object-cover"
            />
          </div>
        </section>
      </ScrollReveal>

      <div className="marketing-divider" />

      {/* ── Distribution featured ──────────────────────────── */}
      <ScrollReveal>
        <section className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <div className="order-last lg:order-first overflow-hidden rounded-2xl border" style={{ borderColor: "var(--border)" }}>
            <Image
              src="/inventory-warehouses.png"
              alt="Distribution — multi-warehouse inventory"
              width={760}
              height={500}
              className="w-full object-cover"
            />
          </div>
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              Distribution & Wholesale
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              Stock visibility across every warehouse, in real time.
            </h2>
            <p className="mt-4 text-base leading-7" style={{ color: "var(--muted)" }}>
              Track inventory across multiple warehouses and locations, manage
              supplier relationships, process purchase orders, and fulfil
              customer orders — all from one connected platform that keeps your
              stock levels accurate and your margins protected.
            </p>
            <ul className="mt-6 space-y-2.5">
              {["Multi-warehouse stock control", "Serial & batch tracking", "Supplier management", "Order-to-cash workflow", "Real-time inventory reports"].map((f) => (
                <li key={f} className="flex items-center gap-2.5">
                  <span className="h-1.5 w-1.5 rounded-full shrink-0" style={{ background: "var(--accent)" }} />
                  <span className="text-sm" style={{ color: "var(--muted)" }}>{f}</span>
                </li>
              ))}
            </ul>
            <div className="mt-8">
              <MarketingButtonLink href="/demo">Book a distribution demo</MarketingButtonLink>
            </div>
          </div>
        </section>
      </ScrollReveal>

      <div className="marketing-divider-accent" />

      {/* Why one ERP */}
      <ScrollReveal>
        <section className="grid gap-10 lg:grid-cols-2 lg:items-center">
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              Why one platform
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              One ERP. Every industry. No compromises.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              Proprietary ERPs force you to pay for features you don't need
              and lack the ones you do. LenERP is comprehensive enough for
              any industry and flexible enough to match how your team actually
              works — with no per-user cost that compounds as you grow.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <MarketingButtonLink href="/modules">
                Explore all features
              </MarketingButtonLink>
              <MarketingButtonLink href="/demo" variant="secondary">
                Book an industry demo
              </MarketingButtonLink>
            </div>
          </div>

          <div className="space-y-5">
            {[
              "Full CRM, ERP, and reporting out of the box for every industry.",
              "Industry-specific modules that match how your team actually works.",
              "Low-code / no-code customisation — adapt forms, workflows, and reports without developers.",
              "One platform, one dataset — no matter how many sites, teams, or entities you run.",
            ].map((item, i) => (
              <ScrollReveal key={item} delay={i * 0.08}>
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
                    style={{ color: "var(--muted)" }}
                  >
                    {item}
                  </p>
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
