import type { Metadata } from "next";
import Link from "next/link";
import { PlaceholderCard } from "@/components/PlaceholderCard";

export const metadata: Metadata = {
  title: "Drilling",
  description:
    "Explore the first rollout-ready industry story for the SaaS control plane: drilling operations, onboarding, and field execution visibility.",
};

export default function DrillingPage() {
  return (
    <div className="space-y-8">
      <section
        className="rounded-[2rem] border p-8 lg:p-10"
        style={{
          borderColor: "var(--border)",
          backgroundColor: "var(--surface)",
          boxShadow: "0 24px 60px var(--shadow)",
        }}
      >
        <p
          className="text-xs font-semibold uppercase tracking-[0.24em]"
          style={{ color: "var(--muted)" }}
        >
          First vertical
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          A drilling-focused rollout story with field-ready structure and a
          clear ERPNext boundary.
        </h1>
        <p
          className="mt-4 max-w-2xl text-sm leading-7"
          style={{ color: "var(--muted)" }}
        >
          The first implementation template prioritizes the operational rhythms
          of a drilling company: daily field work, safety, equipment readiness,
          dispatch coordination, and controlled go-live planning.
        </p>
      </section>

      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <PlaceholderCard
          eyebrow="Why drilling"
          title="A focused launch vertical"
          description="Starting with one operations-heavy industry gives the control plane a concrete customer profile, implementation pattern, and module mix."
        />
        <div className="grid gap-4 md:grid-cols-2">
          {[
            "Daily field reporting",
            "Safety checklists",
            "Equipment inspections",
            "Crew and dispatcher workflows",
          ].map((item) => (
            <div
              key={item}
              className="rounded-2xl border p-4"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
              }}
            >
              <p
                className="text-sm font-semibold"
                style={{ color: "var(--text)" }}
              >
                {item}
              </p>
            </div>
          ))}
        </div>
      </div>

      <Link
        href="/demo"
        className="inline-flex rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
        style={{
          backgroundColor: "var(--accent)",
          color: "var(--accent-foreground)",
          boxShadow: "0 16px 32px var(--shadow)",
        }}
      >
        Request a drilling demo
      </Link>
    </div>
  );
}
