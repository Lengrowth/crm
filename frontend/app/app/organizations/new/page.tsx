"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createOrganization } from "@/lib/api";

export default function NewOrganizationPage() {
  const router = useRouter();
  const [submitted, setSubmitted] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError(null);

    const form = event.currentTarget;
    const fd = new FormData(form);
    const read = (name: string) => String(fd.get(name) ?? "").trim();

    try {
      const created = await createOrganization({
        name: read("name"),
        legal_name: read("legal_name") || undefined,
        industry: read("industry") || undefined,
        country: read("country") || undefined,
        timezone: read("timezone") || undefined,
        billing_email: read("billing_email") || undefined,
        status: read("status") || "lead",
      });

      setSubmitted(true);
      router.push(`/app/organizations/${created.id}`);
      router.refresh();
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Unable to create the organization.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[1fr_0.85fr]">
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
          Create organization
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Capture a customer account brief for pilot planning and onboarding.
        </h1>
        <p className="mt-4 text-sm leading-7" style={{ color: "var(--muted)" }}>
          Use this screen to create the organization record that anchors tenant
          rollout, implementation planning, and billing ownership in the SaaS
          layer.
        </p>

        <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
          {[
            ["Organization name", "North Ridge Operations"],
            ["Legal name", "North Ridge Operations LLC"],
            ["Industry", "drilling"],
            ["Country", "United States"],
            ["Billing email", "finance@northridge.example"],
          ].map(([label, placeholder]) => (
            <label key={label} className="block space-y-2">
              <span
                className="text-xs font-semibold uppercase tracking-[0.18em]"
                style={{ color: "var(--muted)" }}
              >
                {label}
              </span>
              <input
                name={
                  label === "Organization name"
                    ? "name"
                    : label === "Legal name"
                      ? "legal_name"
                      : label === "Industry"
                        ? "industry"
                        : label === "Country"
                          ? "country"
                          : "billing_email"
                }
                required={label === "Organization name"}
                className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                style={{
                  borderColor: "var(--border)",
                  backgroundColor: "var(--surface-strong)",
                  color: "var(--text)",
                }}
                placeholder={placeholder}
              />
            </label>
          ))}

          <label className="block space-y-2">
            <span
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              Timezone
            </span>
            <input
              name="timezone"
              className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
              placeholder="UTC"
            />
          </label>

          <label className="block space-y-2">
            <span
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              Status
            </span>
            <select
              name="status"
              className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
              defaultValue="lead"
            >
              <option value="lead">lead</option>
              <option value="trial">trial</option>
              <option value="active">active</option>
            </select>
          </label>

          <button
            type="submit"
            disabled={busy}
            className="rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              backgroundColor: "var(--accent)",
              color: "var(--accent-foreground)",
              boxShadow: "0 16px 32px var(--shadow)",
            }}
          >
            {busy ? "Creating..." : "Create organization"}
          </button>
          {error ? (
            <p className="text-sm text-red-500">{error}</p>
          ) : submitted ? (
            <p className="text-sm" style={{ color: "var(--muted)" }}>
              Organization created successfully. Redirecting to the detail
              screen.
            </p>
          ) : null}
        </form>
      </section>

      <aside className="space-y-6">
        <div
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
            Why this screen matters
          </h2>
          <p
            className="mt-3 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            A strong organization record anchors billing contacts, tenant
            ownership, implementation planning, and module packaging decisions.
          </p>
        </div>
        <div
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
            Need to go back?
          </h2>
          <Link
            href="/app/organizations"
            className="mt-4 inline-flex rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface)",
              color: "var(--text)",
            }}
          >
            Return to organizations
          </Link>
        </div>
      </aside>
    </div>
  );
}
