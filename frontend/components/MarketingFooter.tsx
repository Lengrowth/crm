import Link from "next/link";
import {
  marketingFooterSections,
  marketingUtilityNav,
} from "@/lib/navigation";
import { MarketingButtonLink } from "@/components/MarketingPrimitives";

export function MarketingFooter() {
  return (
    <footer className="relative border-t border-[color:var(--border)] bg-[color:var(--surface-overlay)] backdrop-blur-xl">
      <div className="mx-auto grid max-w-7xl gap-12 px-6 py-14 md:px-8 lg:grid-cols-[1.2fr_1.8fr]">
        <div className="max-w-md">
          <Link
            href="/"
            className="text-sm font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--text)" }}
          >
            LenQuant
          </Link>
          <p className="mt-4 text-sm leading-7" style={{ color: "var(--muted)" }}>
            Premium SaaS control for onboarding, tenant readiness, rollout
            coordination, and implementation visibility around ERPNext-backed
            operations.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <MarketingButtonLink href={marketingUtilityNav[0].href}>
              {marketingUtilityNav[0].label}
            </MarketingButtonLink>
            <MarketingButtonLink
              href={marketingUtilityNav[1].href}
              variant="secondary"
            >
              {marketingUtilityNav[1].label}
            </MarketingButtonLink>
          </div>
        </div>

        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {marketingFooterSections.map((section) => (
            <div key={section.title}>
              <p
                className="text-xs font-semibold uppercase tracking-[0.24em]"
                style={{ color: "var(--muted)" }}
              >
                {section.title}
              </p>
              <ul className="mt-4 space-y-3 text-sm" style={{ color: "var(--muted)" }}>
                {section.links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="transition hover:opacity-100"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="marketing-divider" />

      <div className="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-6 text-sm md:flex-row md:items-center md:justify-between md:px-8">
        <p style={{ color: "var(--muted)" }}>
          Designed for pilot conversations, implementation-led sales, and safer
          ERP runtime cutovers.
        </p>
        <p style={{ color: "var(--muted)" }}>
          Public website, SaaS control plane, and ERP runtime kept intentionally
          distinct.
        </p>
      </div>
    </footer>
  );
}
