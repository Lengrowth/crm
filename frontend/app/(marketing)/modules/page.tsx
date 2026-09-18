import type { Metadata } from "next";
import Image from "next/image";
import {
  MarketingButtonLink,
  MarketingIcon,
  MarketingPageCta,
  ScrollReveal,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Features — LenERP",
  description:
    "LenERP covers accounting, CRM, sales, procurement, inventory, manufacturing, projects, HR, quality, and support — one connected platform for any business.",
};

type PublicModule = { code: string; name: string; category: string | null; description: string; display_order: number };

async function loadPublicModules(): Promise<PublicModule[]> {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000"}/public/modules`, { next: { revalidate: 60 } });
    if (!response.ok) return [];
    return await response.json() as PublicModule[];
  } catch {
    return [];
  }
}

export default async function ModulesPage() {
  const modules = await loadPublicModules();
  return (
    <div className="space-y-16 lg:space-y-24">
      {/* Hero */}
      <div className="max-w-2xl">
        <p
          className="marketing-reveal text-xs font-semibold uppercase tracking-[0.28em]"
          style={{ color: "var(--accent)" }}
        >
          Features
        </p>
        <h1
          className="marketing-reveal mt-4 text-5xl font-semibold tracking-[-0.05em] sm:text-6xl"
          style={{ color: "var(--text)", animationDelay: "60ms" }}
        >
          Every feature your business needs, connected.
        </h1>
        <p
          className="marketing-reveal mt-5 max-w-lg text-lg leading-8"
          style={{ color: "var(--muted)", animationDelay: "120ms" }}
        >
          Accounting, CRM, sales, procurement, inventory, manufacturing, projects,
          and more — one platform that works out of the box for any business,
          customisable to fit your unique needs.
        </p>
      </div>

      {/* Module grid — with hover microinteractions */}
      <ScrollReveal>
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3 marketing-stagger">
          {modules.map((mod) => (
            <div
              key={mod.code}
              className="marketing-module-card marketing-panel rounded-[1.75rem] p-6 flex flex-col"
            >
              <span
                className="marketing-module-icon flex h-10 w-10 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--text)]"
                style={{ background: "var(--surface-strong)" }}
              >
                <MarketingIcon icon="grid" className="h-5 w-5" />
              </span>
              <h2
                className="mt-4 text-xl font-semibold tracking-[-0.02em]"
                style={{ color: "var(--text)" }}
              >
                {mod.name}
              </h2>
              <p
                className="mt-2 text-sm leading-6"
                style={{ color: "var(--muted)" }}
              >
                {mod.description}
              </p>
              <p className="mt-4 font-mono text-[0.65rem] uppercase tracking-[0.16em]" style={{ color: "var(--accent)" }}>{mod.code}</p>
            </div>
          ))}
        </div>
      </ScrollReveal>

      <div className="marketing-divider" />

      {/* ── CRM deep-dive ─────────────────────────────────── */}
      <ScrollReveal>
        <section className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              CRM
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              Win more deals with a pipeline built for every team.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              Track leads from first contact to closed contract. Manage
              opportunities across territories, set follow-up reminders, assign
              tasks, and get a real-time view of your pipeline — without
              switching tools.
            </p>
            <ul className="mt-6 space-y-2.5">
              {["Leads & opportunities", "Quotations & proposals", "Multi-territory sales", "SLA management", "Email & call logging"].map((f) => (
                <li key={f} className="flex items-center gap-2.5">
                  <span className="h-1.5 w-1.5 rounded-full shrink-0" style={{ background: "var(--accent)" }} />
                  <span className="text-sm" style={{ color: "var(--muted)" }}>{f}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="overflow-hidden rounded-2xl border" style={{ borderColor: "var(--border)" }}>
            <Image
              src="/crm-contacts.webp"
              alt="CRM — contacts and customer management"
              width={760}
              height={500}
              className="w-full object-cover"
            />
          </div>
        </section>
      </ScrollReveal>

      <div className="marketing-divider" />

      {/* ── Accounting deep-dive ──────────────────────────── */}
      <ScrollReveal>
        <section className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <div className="order-last lg:order-first overflow-hidden rounded-2xl border" style={{ borderColor: "var(--border)" }}>
            <Image
              src="/accounting-balance-sheet.png"
              alt="Accounting — balance sheet and financial statements"
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
              Accounting
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              Real-time financials with nothing left to reconcile.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              Every invoice, payment, stock movement, and payroll entry flows
              directly into the general ledger. Get your balance sheet, P&amp;L,
              and cash flow statement at any time — with multi-currency and
              multi-subsidiary support built in.
            </p>
            <ul className="mt-6 space-y-2.5">
              {["General ledger & chart of accounts", "Accounts payable & receivable", "Balance sheet & P&L", "Multi-currency & multi-subsidiary", "Global tax compliance"].map((f) => (
                <li key={f} className="flex items-center gap-2.5">
                  <span className="h-1.5 w-1.5 rounded-full shrink-0" style={{ background: "var(--accent)" }} />
                  <span className="text-sm" style={{ color: "var(--muted)" }}>{f}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>
      </ScrollReveal>

      <div className="marketing-divider" />

      {/* ── Manufacturing deep-dive ───────────────────────── */}
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
              Plan, produce, and track every work order in one place.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              Multi-level BOMs, production scheduling, work orders, job cards,
              and subcontracting — all connected to your inventory, procurement,
              and accounting so nothing falls through the cracks on the
              production floor.
            </p>
            <ul className="mt-6 space-y-2.5">
              {["Multi-level BOM", "Production planning & scheduling", "Work orders & job cards", "Subcontracting", "Quality checks in-line"].map((f) => (
                <li key={f} className="flex items-center gap-2.5">
                  <span className="h-1.5 w-1.5 rounded-full shrink-0" style={{ background: "var(--accent)" }} />
                  <span className="text-sm" style={{ color: "var(--muted)" }}>{f}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="overflow-hidden rounded-2xl border" style={{ borderColor: "var(--border)" }}>
            <Image
              src="/manufacturing-dashboard.webp"
              alt="Manufacturing dashboard — work orders and production"
              width={760}
              height={500}
              className="w-full object-cover"
            />
          </div>
        </section>
      </ScrollReveal>

      <div className="marketing-divider-accent" />

      {/* Why modules matter */}
      <ScrollReveal>
        <section className="grid gap-10 lg:grid-cols-2 lg:items-start">
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              Why it matters
            </p>
            <h2
              className="mt-4 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              Connected by design.
            </h2>
            <p
              className="mt-4 text-base leading-7"
              style={{ color: "var(--muted)" }}
            >
              Every module shares the same customer records, financial data, and
              operational history. When a sales order closes, inventory moves.
              When a job finishes, the invoice is ready. No spreadsheets, no
              double-entry, no broken handoffs between teams.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <MarketingButtonLink href="/onboarding">
                Request onboarding
              </MarketingButtonLink>
              <MarketingButtonLink href="/demo">
                Book a demo
              </MarketingButtonLink>
              <MarketingButtonLink href="/industries" variant="secondary">
                See industries
              </MarketingButtonLink>
            </div>
          </div>

          <div className="space-y-6">
            {[
              {
                icon: "eye" as const,
                title: "One source of truth",
                description:
                  "Customer records, job data, and financials live in one place — visible to everyone who needs them.",
              },
              {
                icon: "clock" as const,
                title: "Real-time across the business",
                description:
                  "Field updates reflect instantly in the office. Invoices generate when jobs close. Nothing waits.",
              },
              {
                icon: "link" as const,
                title: "Built for how you grow",
                description:
                  "Start with CRM and accounting. Add manufacturing, projects, POS, HR, and quality as the business expands.",
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
                    <h3
                      className="text-sm font-semibold"
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
