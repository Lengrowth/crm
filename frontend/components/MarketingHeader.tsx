"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { marketingNav } from "@/lib/navigation";
import { ThemeToggle } from "@/components/ThemeToggle";
import { MarketingButtonLink } from "@/components/MarketingPrimitives";
import { useScrolled } from "@/hooks/useScrolled";

export function MarketingHeader() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const scrolled = useScrolled(40);

  function isActive(href: string) {
    return href === "/" ? pathname === "/" : pathname.startsWith(href);
  }

  return (
    <header
      className="sticky top-0 z-50 border-b backdrop-blur-xl transition-all duration-300"
      style={{
        borderColor: scrolled
          ? "var(--border-strong)"
          : "var(--border)",
        background: scrolled
          ? "var(--surface-strong)"
          : "var(--surface-overlay)",
        boxShadow: scrolled ? "0 4px 24px var(--shadow)" : "none",
      }}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4 md:px-8">
        <Link
          href="/"
          className="marketing-brand text-base font-bold uppercase tracking-[0.22em] transition hover:opacity-70"
          style={{ color: "var(--text)" }}
          onClick={() => setMobileOpen(false)}
        >
          LenERP
        </Link>

        <nav className="hidden items-center gap-1 lg:flex">
          {marketingNav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`marketing-nav-link rounded-full px-3 py-2 text-sm ${isActive(item.href) ? "active" : ""}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="hidden items-center gap-3 lg:flex">
          <ThemeToggle />
          <Link href="/login" className="marketing-nav-link px-3 py-2 text-sm">
            Sign in
          </Link>
          <MarketingButtonLink href="/demo">Book a demo</MarketingButtonLink>
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
            onClick={() => setMobileOpen((c) => !c)}
            aria-expanded={mobileOpen}
            aria-label="Toggle navigation menu"
          >
            {mobileOpen ? "Close" : "Menu"}
          </button>
        </div>
      </div>

      {mobileOpen ? (
        <div className="border-t border-[color:var(--border)] px-6 py-4 md:px-8 lg:hidden">
          <div className="flex flex-col gap-1">
            {marketingNav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`marketing-nav-link rounded-2xl px-4 py-3 text-sm font-medium ${isActive(item.href) ? "active" : ""}`}
                onClick={() => setMobileOpen(false)}
              >
                {item.label}
              </Link>
            ))}
            <div className="mt-3 grid grid-cols-2 gap-3 border-t border-[color:var(--border)] pt-3">
              <MarketingButtonLink href="/demo">
                Book a demo
              </MarketingButtonLink>
              <MarketingButtonLink href="/login" variant="secondary">
                Sign in
              </MarketingButtonLink>
            </div>
          </div>
        </div>
      ) : null}
    </header>
  );
}
