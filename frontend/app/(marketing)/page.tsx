import type { Metadata } from "next";
import Image from "next/image";
import ModuleTabs from "@/components/ModuleTabs";
import HeroGridSvg from "@/components/HeroGridSvg";
import {
  MarketingBackdrop,
  MarketingButtonLink,
  MarketingCard,
  MarketingIcon,
  MarketingPageCta,
  ScrollReveal,
  type MarketingIconName,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "LenERP — The only ERP you'll ever need",
  description:
    "LenERP is a full-featured CRM & ERP platform covering accounting, sales, procurement, inventory, manufacturing, projects, and more. Built for any business, any industry.",
};

const problems = [
  {
    icon: "spark" as MarketingIconName,
    title: "Proprietary ERPs are expensive and rigid",
    description:
      "SAP, Oracle, and NetSuite drain budgets and lock you in. Businesses deserve a modern, open, and flexible alternative.",
  },
  {
    icon: "chart" as MarketingIconName,
    title: "Disconnected apps create blind spots",
    description:
      "Multiple tools that don't talk to each other lead to manual work, poor visibility, and broken traceability across the business.",
  },
  {
    icon: "shield" as MarketingIconName,
    title: "Growth should not mean more software costs",
    description:
      "Per-user pricing compounds as you grow. Your ERP should scale with your business, not hold it back.",
  },
];

const steps = [
  {
    num: "01",
    title: "Capture and manage customers",
    description:
      "Full CRM pipeline: leads, opportunities, quotes, and deal history — from first contact to signed contract.",
  },
  {
    num: "02",
    title: "Run your operations",
    description:
      "Manufacturing, field services, procurement, and project management — all inside the same system.",
  },
  {
    num: "03",
    title: "Control inventory and stock",
    description:
      "Warehouses, serial and batch tracking, stock ledger, and procurement visibility across every location.",
  },
  {
    num: "04",
    title: "Close, invoice, and report",
    description:
      "Accounting, invoicing, financial statements, and management dashboards — fully connected to operations.",
  },
];

const capabilities = [
  {
    icon: "building" as MarketingIconName,
    title: "CRM",
    description:
      "Leads, opportunities, quotations, multi-territory sales, SLA management, and customer communications in one pipeline.",
  },
  {
    icon: "chart" as MarketingIconName,
    title: "Accounting",
    description:
      "General ledger, accounts payable/receivable, financial statements, fixed assets, and global tax compliance.",
  },
  {
    icon: "spark" as MarketingIconName,
    title: "Sales",
    description:
      "Order-to-cash, sales orders, invoicing, pricing rules, print formats, and integrated payments.",
  },
  {
    icon: "shield" as MarketingIconName,
    title: "Procurement",
    description:
      "Procure-to-pay cycle, material requests, purchase orders, multi-level approvals, and supplier scorecards.",
  },
  {
    icon: "layers" as MarketingIconName,
    title: "Inventory & Stock",
    description:
      "Item master, warehouses, serial and batch tracking, stock ledger, and inventory reports across every location.",
  },
  {
    icon: "bolt" as MarketingIconName,
    title: "Manufacturing",
    description:
      "Multi-level BOM, production planning, work orders, job cards, subcontracting, and quality checks.",
  },
  {
    icon: "clock" as MarketingIconName,
    title: "Projects",
    description:
      "Project and task tracking, revenue recognition, expense tracking, timesheets, and cashflow management.",
  },
  {
    icon: "grid" as MarketingIconName,
    title: "Reporting & Dashboards",
    description:
      "Customisable reports, management dashboards, cost analysis, and real-time KPIs for leadership and teams.",
  },
];


export default function HomePage() {
  return (
    <div className="space-y-20 lg:space-y-32">
      {/* ── Hero ───────────────────────────────────────────── */}
      <MarketingCard
        className="relative overflow-hidden rounded-[2.5rem] px-8 py-16 sm:px-12 sm:py-20 lg:px-16 lg:py-24"
        tone="accent"
      >
        <MarketingBackdrop />
        <HeroGridSvg />

        {/* Full-bleed product screenshot — right half, bleeds to card edge */}
        <div className="pointer-events-none absolute inset-y-0 right-0 hidden w-[50%] translate-x-20 lg:block">
          <Image
            src="/dashboard.png"
            alt="LenERP — business dashboard overview"
            fill
            sizes="58vw"
            className="object-cover object-left-top opacity-75"
            priority
          />
        </div>

        {/* Left: text content */}
        <div className="relative max-w-xl">
          <p
            className="marketing-reveal text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            LenERP
          </p>
          <h1
            className="marketing-reveal mt-5 text-6xl font-semibold sm:text-7xl lg:text-8xl marketing-gradient-text"
            style={{ animationDelay: "60ms" }}
          >
            The only ERP you'll ever need.
          </h1>
          <p
            className="marketing-reveal mt-6 max-w-lg text-lg leading-8"
            style={{ color: "var(--muted)", animationDelay: "120ms" }}
          >
            Accounts, CRM, sales, procurement, inventory, manufacturing,
            projects, and more — in one modern platform built for any
            business, any industry.
          </p>
          <div
            className="marketing-reveal mt-8 flex flex-wrap gap-3"
            style={{ animationDelay: "180ms" }}
          >
            <MarketingButtonLink href="/demo">Book a demo</MarketingButtonLink>
            <MarketingButtonLink href="/modules" variant="secondary">
              Explore features
            </MarketingButtonLink>
          </div>
        </div>
      </MarketingCard>

      {/* ── Module tabs showcase ──────────────────────────── */}
      <ScrollReveal>
        <section>
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            The platform
          </p>
          <h2
            className="mt-4 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl"
            style={{ color: "var(--text)" }}
          >
            Every module your business needs, in one place.
          </h2>
          <p
            className="mt-4 max-w-2xl text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            LenERP covers the entire business — from CRM to accounting,
            procurement to manufacturing, projects to support — all sharing one
            dataset, no integrations required.
          </p>
          <div className="mt-10">
            <ModuleTabs />
          </div>
        </section>
      </ScrollReveal>

      <div className="marketing-divider-accent" />

      {/* ── Problem band ─────────────────────────────────── */}
      <ScrollReveal>
        <section>
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            The problem
          </p>
          <h2
            className="mt-4 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl"
            style={{ color: "var(--text)" }}
          >
            The future of business software is open.
          </h2>
          <div className="mt-12 grid gap-10 md:grid-cols-3 marketing-stagger">
            {problems.map((item) => (
              <div key={item.title} className="flex items-start gap-4">
                <span
                  className="mt-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--text)]"
                  style={{ background: "var(--surface)" }}
                >
                  <MarketingIcon icon={item.icon} className="h-5 w-5" />
                </span>
                <div>
                  <h3 className="font-semibold" style={{ color: "var(--text)" }}>
                    {item.title}
                  </h3>
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
        </section>
      </ScrollReveal>

      <div className="marketing-divider-accent" />

      {/* ── How it works — timeline ───────────────────────── */}
      <ScrollReveal>
        <section className="grid gap-12 lg:grid-cols-2 lg:items-start">
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              How it works
            </p>
            <h2
              className="mt-4 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl"
              style={{ color: "var(--text)" }}
            >
              One platform for every part of the business.
            </h2>
            <p
              className="mt-4 max-w-md text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              From first sales call to final invoice — every workflow runs
              inside a single connected system with no double-entry, no
              spreadsheets, and no broken handoffs.
            </p>
            <div className="mt-8">
              <MarketingButtonLink href="/modules">
                See all features
              </MarketingButtonLink>
            </div>
          </div>

          <div className="marketing-timeline space-y-8">
            {steps.map((item, i) => (
              <ScrollReveal key={item.num} delay={i * 0.08}>
                <div className="marketing-timeline-item">
                  <span className="marketing-step-num shrink-0">{item.num}</span>
                  <div className="pt-1.5">
                    <h3 className="font-semibold" style={{ color: "var(--text)" }}>
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

      <div className="marketing-divider" />

      {/* ── Capabilities — module grid ────────────────────── */}
      <ScrollReveal>
        <section>
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            Capabilities
          </p>
          <h2
            className="mt-4 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl"
            style={{ color: "var(--text)" }}
          >
            Everything your business runs on.
          </h2>
          <p
            className="mt-4 max-w-2xl text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            Accounts, invoicing, sales, procurement, stock, manufacturing,
            projects, HR, and more — out of the box for almost any industry,
            customisable to fit your unique needs.
          </p>

          <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {capabilities.map((item, i) => (
              <ScrollReveal key={item.title} delay={i * 0.05}>
                <div className="marketing-panel rounded-[1.5rem] p-6 h-full">
                  <span
                    className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--text)]"
                    style={{ background: "var(--surface-strong)" }}
                  >
                    <MarketingIcon icon={item.icon} className="h-5 w-5" />
                  </span>
                  <h3
                    className="mt-4 font-semibold"
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

          <div className="mt-8">
            <MarketingButtonLink href="/modules" variant="secondary">
              View all features
            </MarketingButtonLink>
          </div>
        </section>
      </ScrollReveal>

      <div className="marketing-divider" />

      {/* ── Why choose LenERP ───────────────────────────── */}
      <ScrollReveal>
        <section>
          <div className="grid gap-10 lg:grid-cols-2 lg:items-center">
            <div>
              <p
                className="text-xs font-semibold uppercase tracking-[0.28em]"
                style={{ color: "var(--accent)" }}
              >
                Why LenERP
              </p>
              <h2
                className="mt-4 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl"
                style={{ color: "var(--text)" }}
              >
                Built for any industry. Works out of the box.
              </h2>
              <p
                className="mt-4 max-w-md text-base leading-7"
                style={{ color: "var(--muted)" }}
              >
                LenERP works for manufacturing, distribution, services, retail,
                construction, and field operations — including specialist use cases
                like drilling. Every engagement includes implementation,
                onboarding, and ongoing support.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <MarketingButtonLink href="/industries">
                  See industries
                </MarketingButtonLink>
                <MarketingButtonLink href="/demo" variant="secondary">
                  Book a demo
                </MarketingButtonLink>
              </div>
            </div>

            <div className="space-y-4">
              {[
                {
                  icon: "spark" as MarketingIconName,
                  title: "No-code / low-code customisation",
                  description:
                    "Automate tasks with drag-and-drop simplicity. Customise forms, reports, print formats, and dashboards without writing code.",
                },
                {
                  icon: "shield" as MarketingIconName,
                  title: "Built for global businesses",
                  description:
                    "Multi-subsidiary, multi-currency, multi-language. Tax compliance out of the box for 150+ countries.",
                },
                {
                  icon: "chart" as MarketingIconName,
                  title: "No per-user pricing",
                  description:
                    "Pay only for hosting — not for every seat. Costs don't compound as your team grows.",
                },
                {
                  icon: "link" as MarketingIconName,
                  title: "API-first integrations",
                  description:
                    "Connect to payment gateways, e-commerce platforms, cloud storage, and third-party tools with ease.",
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
          </div>

          {/* Platform feature images */}
          <div className="mt-14 grid gap-5 sm:grid-cols-3 marketing-stagger">
            <ScrollReveal delay={0}>
              <div className="overflow-hidden rounded-2xl border" style={{ borderColor: "var(--border)" }}>
                <Image src="/platform-nocode.webp" alt="No-code workflow automation" width={600} height={380} className="w-full object-cover" />
                <div className="px-4 py-3" style={{ background: "var(--surface)" }}>
                  <p className="text-xs font-semibold" style={{ color: "var(--text)" }}>No-code workflows</p>
                  <p className="mt-0.5 text-xs" style={{ color: "var(--muted)" }}>Automate without code</p>
                </div>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={0.08}>
              <div className="overflow-hidden rounded-2xl border" style={{ borderColor: "var(--border)" }}>
                <Image src="/accounting-multicurrency.webp" alt="Multi-currency accounting" width={600} height={380} className="w-full object-cover" />
                <div className="px-4 py-3" style={{ background: "var(--surface)" }}>
                  <p className="text-xs font-semibold" style={{ color: "var(--text)" }}>Global compliance</p>
                  <p className="mt-0.5 text-xs" style={{ color: "var(--muted)" }}>Multi-currency, multi-entity</p>
                </div>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={0.16}>
              <div className="overflow-hidden rounded-2xl border" style={{ borderColor: "var(--border)" }}>
                <Image src="/platform-api.webp" alt="API integrations" width={600} height={380} className="w-full object-cover" />
                <div className="px-4 py-3" style={{ background: "var(--surface)" }}>
                  <p className="text-xs font-semibold" style={{ color: "var(--text)" }}>API-first integrations</p>
                  <p className="mt-0.5 text-xs" style={{ color: "var(--muted)" }}>Connect any third-party tool</p>
                </div>
              </div>
            </ScrollReveal>
          </div>
        </section>
      </ScrollReveal>

      <MarketingPageCta />
    </div>
  );
}
