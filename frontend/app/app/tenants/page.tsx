"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { fetchTenants } from "@/lib/api";

export default function AppTenantsPage() {
  const [tenants, setTenants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    fetchTenants()
      .then((data) => {
        if (!mounted) return;
        setTenants(data || []);
      })
      .catch((err: any) => setError(err?.message ?? "Failed to load tenants"))
      .finally(() => mounted && setLoading(false));

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div className="space-y-6">
      <section
        className="rounded-[2rem] border p-8 lg:p-10"
        style={{
          borderColor: "var(--border)",
          backgroundColor: "var(--surface)",
          boxShadow: "0 24px 60px var(--shadow)",
        }}
      >
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl">
            <p
              className="text-xs font-semibold uppercase tracking-[0.24em]"
              style={{ color: "var(--muted)" }}
            >
              Tenants
            </p>
            <h1
              className="mt-4 text-4xl font-semibold tracking-tight"
              style={{ color: "var(--text)" }}
            >
              Tenant records stay in the SaaS layer, even before live ERPNext
              cutover begins.
            </h1>
            <p
              className="mt-4 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              Review environments, provisioning posture, and domain planning
              from a protected control-plane view.
            </p>
          </div>
          <Link
            href="/app/tenants/new"
            className="inline-flex rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              backgroundColor: "var(--accent)",
              color: "var(--accent-foreground)",
              boxShadow: "0 16px 32px var(--shadow)",
            }}
          >
            Create tenant
          </Link>
        </div>
      </section>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-4">
          {loading ? (
            <p style={{ color: "var(--muted)" }}>Loading tenants...</p>
          ) : error ? (
            <p className="text-sm text-red-500">{error}</p>
          ) : tenants.length === 0 ? (
            <p style={{ color: "var(--muted)" }}>No tenants found.</p>
          ) : (
            tenants.map((tenant) => (
              <article
                key={tenant.id}
                className="rounded-2xl border p-6"
                style={{
                  borderColor: "var(--border)",
                  backgroundColor: "var(--surface-strong)",
                  boxShadow: "0 18px 40px var(--shadow)",
                }}
              >
                <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                  <div>
                    <p
                      className="text-xs font-semibold uppercase tracking-[0.18em]"
                      style={{ color: "var(--muted)" }}
                    >
                      {tenant.environment} • org {tenant.organization_id}
                    </p>
                    <h2
                      className="mt-2 text-2xl font-semibold"
                      style={{ color: "var(--text)" }}
                    >
                      {tenant.tenant_slug}
                    </h2>
                    <p
                      className="mt-2 text-sm leading-6"
                      style={{ color: "var(--muted)" }}
                    >
                      Status: {tenant.status} • Provisioning:{" "}
                      {tenant.provisioning_status}
                    </p>
                    {tenant.primary_domain ? (
                      <p
                        className="mt-1 text-sm leading-6"
                        style={{ color: "var(--muted)" }}
                      >
                        Primary domain: {tenant.primary_domain}
                      </p>
                    ) : null}
                  </div>
                  <Link
                    href={`/app/tenants/${tenant.id}`}
                    className="rounded-full border px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] transition hover:translate-y-[-1px]"
                    style={{
                      borderColor: "var(--border)",
                      backgroundColor: "var(--surface)",
                      color: "var(--text)",
                    }}
                  >
                    Open detail
                  </Link>
                </div>
              </article>
            ))
          )}
        </div>

        <div className="space-y-6">
          {[
            [
              "Environment mapping",
              "Each tenant should map cleanly to one target environment and, later, one explicit ERPNext site reference.",
            ],
            [
              "Provisioning visibility",
              "Provisioning status belongs in the SaaS layer so operators can see readiness before and after cutover.",
            ],
            [
              "Boundary safety",
              "The production path should never rely on hidden mock defaults; the product boundary stays explicit.",
            ],
          ].map(([title, description]) => (
            <div
              key={title}
              className="rounded-2xl border p-6"
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
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
