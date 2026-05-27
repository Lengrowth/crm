import Link from "next/link";
import type { ReactNode } from "react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { SessionBadge } from "@/components/SessionBadge";
import { dashboardNav } from "@/lib/navigation";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="theme-shell min-h-screen">
      <div className="grid min-h-screen lg:grid-cols-[260px_1fr]">
        <aside
          className="border-r p-6"
          style={{
            borderColor: "var(--border)",
            backgroundColor: "var(--surface)",
          }}
        >
          <div className="mb-8">
            <p className="text-xs font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>
              Control Layer
            </p>
            <h1 className="mt-2 text-xl font-semibold" style={{ color: "var(--text)" }}>
              SaaS App Shell
            </h1>
            <p className="mt-2 text-sm leading-6" style={{ color: "var(--muted)" }}>
              Local-only dashboard routes for organizations, tenants, modules, and implementation work.
            </p>
          </div>
          <SessionBadge />
          <nav className="space-y-2 text-sm">
            {dashboardNav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="block rounded-xl border px-4 py-3 transition hover:translate-x-0.5"
                style={{
                  borderColor: "var(--border)",
                  backgroundColor: "var(--surface-strong)",
                  color: "var(--text)",
                  boxShadow: "0 10px 30px var(--shadow)",
                }}
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <div className="mt-8">
            <ThemeToggle />
          </div>
        </aside>
        <main className="p-6 lg:p-10">{children}</main>
      </div>
    </div>
  );
}
