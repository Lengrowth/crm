import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Modules",
  description:
    "Review the product modules that the SaaS control plane can position, track, and eventually entitle per organization.",
};

const moduleList = [
  [
    "CRM",
    "Customer, pipeline, and commercial visibility that belongs to the SaaS control layer.",
  ],
  [
    "Field Ops",
    "Operational workflows for teams coordinating jobs, crews, and site execution.",
  ],
  [
    "Drilling",
    "Industry-specific defaults for the first rollout-ready vertical.",
  ],
  ["Fleet", "Vehicle, equipment, and maintenance-aware operations support."],
  [
    "Inventory",
    "Materials and stock visibility for deployment-critical operations.",
  ],
  [
    "Reporting",
    "Operational and administrative reporting for support, leadership, and launch visibility.",
  ],
];

export default function ModulesPage() {
  return (
    <div className="space-y-8">
      <section className="max-w-3xl">
        <p
          className="text-xs font-semibold uppercase tracking-[0.24em]"
          style={{ color: "var(--muted)" }}
        >
          Modules
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Modules define what each organization can activate, package, and
          prepare for rollout.
        </h1>
        <p className="mt-4 text-sm leading-7" style={{ color: "var(--muted)" }}>
          The public site now presents a real product story: modules are part of
          the SaaS commercial and operational model first, then they map into
          ERPNext configuration later.
        </p>
      </section>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {moduleList.map(([title, description]) => (
          <article
            key={title}
            className="rounded-[1.75rem] border p-6"
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
          href="/demo"
          className="inline-flex rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
          style={{
            backgroundColor: "var(--accent)",
            color: "var(--accent-foreground)",
            boxShadow: "0 16px 32px var(--shadow)",
          }}
        >
          See the demo
        </Link>
        <Link
          href="/login"
          className="inline-flex rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
          style={{
            borderColor: "var(--border)",
            backgroundColor: "var(--surface-strong)",
            color: "var(--text)",
          }}
        >
          Sign in
        </Link>
      </div>
    </div>
  );
}
