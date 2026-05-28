"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createTenant } from "@/lib/api";

export default function NewTenantPage() {
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
      const created = await createTenant({
        organization_id: read("organization_id") || undefined,
        tenant_slug: read("tenant_slug"),
        environment: read("environment") || "demo",
        status: read("status") || "planned",
        primary_domain: read("primary_domain") || undefined,
        custom_domain: read("custom_domain") || undefined,
        erpnext_site_name: read("erpnext_site_name") || undefined,
        erpnext_base_url: read("erpnext_base_url") || undefined,
        provisioning_status: read("provisioning_status") || "pending",
      });

      setSubmitted(true);
      router.push(`/app/tenants/${created.id}`);
      router.refresh();
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Unable to create the tenant.",
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
          Create tenant
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Prepare a tenant record before live environment cutover.
        </h1>
        <p className="mt-4 text-sm leading-7" style={{ color: "var(--muted)" }}>
          Use this flow to capture the tenant identity, domain plan, and target
          environment that the SaaS layer will own before ERPNext runtime
          activation.
        </p>

        <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
          <label className="block space-y-2">
            <span
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              Organization ID
            </span>
            <input
              name="organization_id"
              required
              className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
              placeholder="org-north-ridge-operations"
            />
          </label>

          {[
            ["Tenant slug", "north-ridge-demo"],
            ["ERPNext site name", "north-ridge-demo.example.com"],
            ["Primary domain", "north-ridge-demo.example.com"],
            ["Custom domain", "ops.northridge.example.com"],
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
                  label === "Tenant slug"
                    ? "tenant_slug"
                    : label === "ERPNext site name"
                      ? "erpnext_site_name"
                      : label === "Primary domain"
                        ? "primary_domain"
                        : "custom_domain"
                }
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

          <div className="grid gap-4 md:grid-cols-2">
            <label className="block space-y-2">
              <span
                className="text-xs font-semibold uppercase tracking-[0.18em]"
                style={{ color: "var(--muted)" }}
              >
                Environment
              </span>
              <select
                name="environment"
                className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                style={{
                  borderColor: "var(--border)",
                  backgroundColor: "var(--surface-strong)",
                  color: "var(--text)",
                }}
                defaultValue="demo"
              >
                <option value="demo">demo</option>
                <option value="staging">staging</option>
                <option value="production">production</option>
              </select>
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
                defaultValue="planned"
              >
                <option value="planned">planned</option>
                <option value="provisioning">provisioning</option>
                <option value="ready">ready</option>
                <option value="suspended">suspended</option>
              </select>
            </label>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <label className="block space-y-2">
              <span
                className="text-xs font-semibold uppercase tracking-[0.18em]"
                style={{ color: "var(--muted)" }}
              >
                Provisioning status
              </span>
              <select
                name="provisioning_status"
                className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                style={{
                  borderColor: "var(--border)",
                  backgroundColor: "var(--surface-strong)",
                  color: "var(--text)",
                }}
                defaultValue="pending"
              >
                <option value="pending">pending</option>
                <option value="queued">queued</option>
                <option value="running">running</option>
                <option value="ready">ready</option>
                <option value="failed">failed</option>
              </select>
            </label>
            <label className="block space-y-2">
              <span
                className="text-xs font-semibold uppercase tracking-[0.18em]"
                style={{ color: "var(--muted)" }}
              >
                ERPNext base URL
              </span>
              <input
                name="erpnext_base_url"
                className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                style={{
                  borderColor: "var(--border)",
                  backgroundColor: "var(--surface-strong)",
                  color: "var(--text)",
                }}
                placeholder="https://north-ridge-demo.example.com"
              />
            </label>
          </div>

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
            {busy ? "Creating..." : "Create tenant"}
          </button>
          {error ? (
            <p className="text-sm text-red-500">{error}</p>
          ) : submitted ? (
            <p className="text-sm" style={{ color: "var(--muted)" }}>
              Tenant created successfully. Redirecting to the detail screen.
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
            Tenant boundaries
          </h2>
          <p
            className="mt-3 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            Tenants belong to organizations, carry rollout metadata, and provide
            the mapping surface for a later live ERPNext site connection.
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
            Back to tenants
          </h2>
          <Link
            href="/app/tenants"
            className="mt-4 inline-flex rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface)",
              color: "var(--text)",
            }}
          >
            Return to tenant list
          </Link>
        </div>
      </aside>
    </div>
  );
}
