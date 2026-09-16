import Link from "next/link";
import { marketingFooterSections } from "@/lib/navigation";
import { MarketingButtonLink } from "@/components/MarketingPrimitives";

export function MarketingFooter() {
  return (
    <footer className="relative overflow-hidden border-t border-[color:var(--border)] bg-[color:var(--surface-overlay)] backdrop-blur-xl">
      {/* Decorative background wordmark */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 bottom-0 select-none overflow-hidden"
      >
        <p
          className="whitespace-nowrap text-center font-semibold uppercase leading-none tracking-[-0.04em]"
          style={{
            fontSize: "clamp(5rem, 20vw, 18rem)",
            color: "var(--text)",
            opacity: 0.025,
            transform: "translateY(18%)",
          }}
        >
          LenERP
        </p>
      </div>

      <div className="relative mx-auto grid max-w-7xl gap-12 px-6 py-14 md:px-8 lg:grid-cols-[1.2fr_1.8fr]">
        <div className="max-w-md">
          <Link
            href="/"
            className="text-sm font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--text)" }}
          >
            LenERP
          </Link>
          <p
            className="mt-4 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            A modern CRM & ERP platform for any business. Accounting, sales,
            procurement, inventory, manufacturing, projects, and more — in one
            connected system.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <MarketingButtonLink href="/demo">Book a demo</MarketingButtonLink>
            <MarketingButtonLink href="/contact" variant="secondary">
              Talk to us
            </MarketingButtonLink>
          </div>
        </div>

        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {marketingFooterSections.map((section) => (
            <div key={section.title}>
              <p
                className="text-xs font-semibold uppercase tracking-[0.24em]"
                style={{ color: "var(--accent)" }}
              >
                {section.title}
              </p>
              <ul
                className="mt-4 space-y-3 text-sm"
                style={{ color: "var(--muted)" }}
              >
                {section.links.map((link) => (
                  <li key={`${link.href}-${link.label}`}>
                    <Link
                      href={link.href}
                      className="transition-opacity hover:opacity-100"
                      style={{ opacity: 0.8 }}
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

      <div className="marketing-divider-accent" />

      <div className="relative mx-auto flex max-w-7xl flex-col gap-2 px-6 py-6 text-sm md:flex-row md:items-center md:justify-between md:px-8">
        <p style={{ color: "var(--muted)" }}>
          © {new Date().getFullYear()} LenERP. All rights reserved.
        </p>
        <p style={{ color: "var(--muted)" }}>
          The only ERP you'll ever need.
        </p>
      </div>
    </footer>
  );
}
