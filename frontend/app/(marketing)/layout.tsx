import type { ReactNode } from "react";
import Link from "next/link";
import { MarketingHeader } from "@/components/MarketingHeader";
import { AnalyticsTracker } from "@/components/AnalyticsTracker";

export default function MarketingLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen text-[color:var(--text)]">
      <MarketingHeader />
      <AnalyticsTracker />
      <main className="mx-auto max-w-6xl px-6 py-12">{children}</main>
      <footer
        className="border-t"
        style={{
          borderColor: "var(--border)",
          backgroundColor: "var(--surface)",
        }}
      >
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-6 py-8 text-sm md:flex-row md:items-center md:justify-between">
          <p style={{ color: "var(--muted)" }}>
            SaaS control plane for organizations, tenants, implementation
            readiness, and ERPNext rollout coordination.
          </p>
          <div
            className="flex flex-wrap gap-4"
            style={{ color: "var(--muted)" }}
          >
            <Link href="/privacy" className="transition hover:opacity-80">
              Privacy
            </Link>
            <Link href="/terms" className="transition hover:opacity-80">
              Terms
            </Link>
            <Link href="/demo" className="transition hover:opacity-80">
              Request demo
            </Link>
            <Link href="/contact" className="transition hover:opacity-80">
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
