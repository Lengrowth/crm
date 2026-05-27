"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import Link from "next/link";

export default function NewTenantPage() {
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitted(true);
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

          <button
            type="submit"
            className="rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              backgroundColor: "var(--accent)",
              color: "var(--accent-foreground)",
              boxShadow: "0 16px 32px var(--shadow)",
            }}
          >
            Save tenant draft
          </button>
          {submitted ? (
            <p className="text-sm" style={{ color: "var(--muted)" }}>
              Draft captured for demo and planning use. Persist this screen when
              you connect it to the protected tenant create route.
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
