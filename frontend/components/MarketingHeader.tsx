"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { marketingNav, marketingUtilityNav } from "@/lib/navigation";
import { ThemeToggle } from "@/components/ThemeToggle";
import { MarketingButtonLink } from "@/components/MarketingPrimitives";

export function MarketingHeader() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  function isActive(href: string) {
    return href === "/" ? pathname === "/" : pathname.startsWith(href);
  }

  return (
    <header className="sticky top-0 z-50 border-b border-[color:var(--border)] bg-[color:var(--surface-overlay)] backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4 md:px-8">
        <div className="flex items-center gap-4">
          <Link
            href="/"
            className="text-sm font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--text)" }}
            onClick={() => setMobileOpen(false)}
          >
            LenQuant
          </Link>
          <div
            className="hidden rounded-full border px-3 py-1 text-xs font-medium lg:inline-flex"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface)",
              color: "var(--muted)",
            }}
          >
            ERP rollout control plane
          </div>
        </div>

        <nav className="hidden items-center gap-6 lg:flex">
          {marketingNav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`marketing-nav-link text-sm ${isActive(item.href) ? "active" : ""}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="hidden items-center gap-3 lg:flex">
          <ThemeToggle />
          <MarketingButtonLink href={marketingUtilityNav[0].href}>
            {marketingUtilityNav[0].label}
          </MarketingButtonLink>
          <MarketingButtonLink
            href={marketingUtilityNav[2].href}
            variant="secondary"
          >
            {marketingUtilityNav[2].label}
          </MarketingButtonLink>
        </div>

        <div className="flex items-center gap-2 lg:hidden">
          <ThemeToggle />
          <button
            type="button"
            className="marketing-menu-button rounded-full border px-4 py-2 text-sm font-semibold"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface)",
              color: "var(--text)",
            }}
            onClick={() => setMobileOpen((current) => !current)}
            aria-expanded={mobileOpen}
            aria-label="Toggle navigation menu"
          >
            {mobileOpen ? "Close" : "Menu"}
          </button>
        </div>
      </div>

      {mobileOpen ? (
        <div className="border-t border-[color:var(--border)] px-6 py-4 md:px-8 lg:hidden">
          <div className="flex flex-col gap-3">
            {marketingNav.concat(marketingUtilityNav).map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`marketing-nav-link rounded-2xl border px-4 py-3 text-sm ${isActive(item.href) ? "active" : ""}`}
                style={{
                  borderColor: isActive(item.href)
                    ? "var(--border-strong)"
                    : "var(--border)",
                  backgroundColor: isActive(item.href)
                    ? "var(--surface-strong)"
                    : "var(--surface)",
                }}
                onClick={() => setMobileOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      ) : null}
    </header>
  );
}
