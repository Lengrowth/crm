"use client";

import { useState } from "react";
import Image from "next/image";
import { MarketingIcon, type MarketingIconName } from "@/components/MarketingPrimitives";

type ModuleTab = {
  id: string;
  label: string;
  icon: MarketingIconName;
  image: string;
  imageAlt: string;
  features: string[];
};

const tabs: ModuleTab[] = [
  {
    id: "crm",
    label: "CRM",
    icon: "building",
    image: "/crm-deals.webp",
    imageAlt: "CRM — deals pipeline and opportunity management",
    features: [
      "Leads & opportunity pipeline",
      "Quotations & proposals",
      "Multi-territory sales",
      "SLA management",
      "Email & call logging",
      "Customer newsletters",
    ],
  },
  {
    id: "accounting",
    label: "Accounting",
    icon: "chart",
    image: "/accounting-insights.png",
    imageAlt: "Accounting — real-time financial insights",
    features: [
      "General ledger & chart of accounts",
      "Accounts payable & receivable",
      "Financial statements (P&L, balance sheet)",
      "Fixed assets & depreciation",
      "Multi-currency & multi-subsidiary",
      "Global tax compliance",
    ],
  },
  {
    id: "sales",
    label: "Sales",
    icon: "spark",
    image: "/sales-quotation.png",
    imageAlt: "Sales — quotations and order-to-cash",
    features: [
      "Order-to-cash workflow",
      "Sales orders & invoicing",
      "Pricing rules & discounts",
      "Print formats",
      "Payment integration",
      "Sales analytics",
    ],
  },
  {
    id: "procurement",
    label: "Procurement",
    icon: "shield",
    image: "/procurement.png",
    imageAlt: "Procurement — purchase orders and supplier management",
    features: [
      "Procure-to-pay cycle",
      "Material requests",
      "Purchase orders",
      "Multi-level approvals",
      "Supplier scorecards",
      "Supplier payments",
    ],
  },
  {
    id: "inventory",
    label: "Inventory",
    icon: "layers",
    image: "/inventory-ledger.png",
    imageAlt: "Inventory — stock ledger and warehouse management",
    features: [
      "Item master & variants",
      "Multi-warehouse management",
      "Serial & batch tracking",
      "Stock ledger",
      "Inventory reports",
      "Stock replenishment",
    ],
  },
  {
    id: "manufacturing",
    label: "Manufacturing",
    icon: "bolt",
    image: "/manufacturing-bom.webp",
    imageAlt: "Manufacturing — BOM browser and production planning",
    features: [
      "Multi-level BOM",
      "Production planning & scheduling",
      "Work orders & job cards",
      "Subcontracting",
      "Capacity planning",
      "Quality checks in-line",
    ],
  },
  {
    id: "projects",
    label: "Projects",
    icon: "clock",
    image: "/projects-gantt-chart.webp",
    imageAlt: "Projects — Gantt chart and task tracking",
    features: [
      "Project & task tracking",
      "Gantt & Kanban views",
      "Timesheets & expenses",
      "Revenue recognition",
      "Project budgets",
      "Cashflow management",
    ],
  },
  {
    id: "support",
    label: "Support",
    icon: "link",
    image: "/support-dashboard.webp",
    imageAlt: "Support & Helpdesk — ticket management and SLAs",
    features: [
      "Auto-assign ticket rules",
      "SLA definitions & tracking",
      "Customer portal",
      "Knowledge base",
      "Maintenance visits",
      "Integrated invoicing",
    ],
  },
];

export default function ModuleTabs() {
  const [active, setActive] = useState("crm");
  const tab = tabs.find((t) => t.id === active) ?? tabs[0];

  return (
    <div>
      {/* Tab bar */}
      <div
        className="flex flex-wrap gap-1 rounded-2xl p-1.5"
        style={{ background: "var(--surface-strong)", border: "1px solid var(--border)" }}
        role="tablist"
      >
        {tabs.map((t) => (
          <button
            key={t.id}
            role="tab"
            aria-selected={t.id === active}
            onClick={() => setActive(t.id)}
            className="flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-semibold transition-all duration-200"
            style={
              t.id === active
                ? {
                    background: "var(--accent)",
                    color: "#fff",
                    boxShadow: "0 2px 8px color-mix(in srgb, var(--accent) 35%, transparent)",
                  }
                : { color: "var(--muted)" }
            }
          >
            <MarketingIcon icon={t.icon} className="h-3.5 w-3.5 shrink-0" />
            {t.label}
          </button>
        ))}
      </div>

      {/* Panel */}
      <div
        className="mt-4 grid gap-0 overflow-hidden rounded-2xl border lg:grid-cols-[1fr_1.5fr]"
        style={{ borderColor: "var(--border)", background: "var(--surface)" }}
        key={active}
      >
        {/* Feature list */}
        <div className="flex flex-col justify-center p-7 lg:p-8">
          <div className="flex items-center gap-2.5">
            <span
              className="flex h-9 w-9 items-center justify-center rounded-xl border"
              style={{
                background: "color-mix(in srgb, var(--accent) 10%, var(--surface))",
                borderColor: "color-mix(in srgb, var(--accent) 25%, var(--border))",
                color: "var(--accent)",
              }}
            >
              <MarketingIcon icon={tab.icon} className="h-4 w-4" />
            </span>
            <h3
              className="text-lg font-semibold tracking-[-0.02em]"
              style={{ color: "var(--text)" }}
            >
              {tab.label}
            </h3>
          </div>

          <ul className="mt-6 space-y-3">
            {tab.features.map((f) => (
              <li key={f} className="flex items-start gap-2.5">
                <span
                  className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full"
                  style={{ background: "var(--accent)" }}
                />
                <span className="text-sm leading-6" style={{ color: "var(--muted)" }}>
                  {f}
                </span>
              </li>
            ))}
          </ul>
        </div>

        {/* Screenshot */}
        <div
          className="relative hidden overflow-hidden lg:block"
          style={{ borderLeft: "1px solid var(--border)" }}
        >
          <Image
            src={tab.image}
            alt={tab.imageAlt}
            fill
            sizes="(max-width: 1024px) 0px, 55vw"
            className="object-cover object-left-top"
            priority={active === "crm"}
          />
        </div>

        {/* Mobile screenshot (below features) */}
        <div className="overflow-hidden border-t lg:hidden" style={{ borderColor: "var(--border)" }}>
          <Image
            src={tab.image}
            alt={tab.imageAlt}
            width={760}
            height={380}
            className="w-full object-cover object-left-top"
          />
        </div>
      </div>
    </div>
  );
}
