import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Industries",
  description:
    "Start with drilling and extend the SaaS control plane across other operations-heavy teams without losing the platform boundary.",
};

export default function IndustriesPage() {
  return (
    <div className="space-y-8">
      <section className="max-w-3xl">
        <p
          className="text-xs font-semibold uppercase tracking-[0.24em]"
          style={{ color: "var(--muted)" }}
        >
          Industries
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Start with drilling, then reuse the control model across other
          operations-heavy teams.
        </h1>
        <p className="mt-4 text-sm leading-7" style={{ color: "var(--muted)" }}>
          The product boundary stays stable even as the vertical changes. The
          SaaS layer owns the account, tenant, and rollout model; ERPNext
          remains the external runtime target.
        </p>
      </section>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        {[
          [
            "Drilling",
            "The first vertical for implementation templates, field workflows, and operator-ready defaults.",
          ],
          [
            "Field service",
            "Dispatch, work orders, and mobile-first coordination patterns.",
          ],
          [
            "Fleet",
            "Vehicles, maintenance, and asset-aware operational management.",
          ],
          [
            "Back office",
            "Finance, support, and admin teams that need a clean SaaS control room.",
          ],
        ].map(([title, description]) => (
          <article
            key={title}
            className="rounded-[2rem] border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
          >
            <h2
              className="text-xl font-semibold"
              style={{ color: "var(--text)" }}
            >
              {title}
            </h2>
            <p
              className="mt-3 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {description}
            </p>
          </article>
        ))}
      </div>

      <div className="flex flex-wrap gap-3">
        <Link
          href="/drilling"
          className="rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
          style={{
            backgroundColor: "var(--accent)",
            color: "var(--accent-foreground)",
            boxShadow: "0 16px 32px var(--shadow)",
          }}
        >
          Explore drilling
        </Link>
        <Link
          href="/modules"
          className="rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
          style={{
            borderColor: "var(--border)",
            backgroundColor: "var(--surface-strong)",
            color: "var(--text)",
          }}
        >
          View modules
        </Link>
      </div>
    </div>
  );
}
