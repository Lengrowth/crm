"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { fetchOrganizations } from "@/lib/api";

export default function AppOrganizationsPage() {
  const [orgs, setOrgs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    fetchOrganizations()
      .then((data) => {
        if (!mounted) return;
        setOrgs(data || []);
      })
      .catch((err: any) =>
        setError(err?.message ?? "Failed to load organizations"),
      )
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
              Organizations
            </p>
            <h1
              className="mt-4 text-4xl font-semibold tracking-tight"
              style={{ color: "var(--text)" }}
            >
              Customer accounts live here, with tenant work hanging off each
              organization.
            </h1>
            <p
              className="mt-4 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              This view is wired to the protected organization APIs so operators
              can review account status, open details, and move directly into
              tenant-level work.
            </p>
          </div>
          <Link
            href="/app/organizations/new"
            className="inline-flex rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              backgroundColor: "var(--accent)",
              color: "var(--accent-foreground)",
              boxShadow: "0 16px 32px var(--shadow)",
            }}
          >
            Create organization
          </Link>
        </div>
      </section>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-4">
          {loading ? (
            <p style={{ color: "var(--muted)" }}>Loading organizations...</p>
          ) : error ? (
            <p className="text-sm text-red-500">{error}</p>
          ) : orgs.length === 0 ? (
            <p style={{ color: "var(--muted)" }}>No organizations found.</p>
          ) : (
            orgs.map((organization) => (
              <article
                key={organization.id}
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
                      {organization.industry ?? "-"}
                    </p>
                    <h2
                      className="mt-2 text-2xl font-semibold"
                      style={{ color: "var(--text)" }}
                    >
                      {organization.name}
                    </h2>
                    <p
                      className="mt-2 text-sm leading-6"
                      style={{ color: "var(--muted)" }}
                    >
                      Status: {organization.status}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-3">
                    <Link
                      href={`/app/organizations/${organization.id}`}
                      className="rounded-full border px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] transition hover:translate-y-[-1px]"
                      style={{
                        borderColor: "var(--border)",
                        backgroundColor: "var(--surface)",
                        color: "var(--text)",
                      }}
                    >
                      Open detail
                    </Link>
                    <Link
                      href={`/app/organizations/${organization.id}/tenants`}
                      className="rounded-full border px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] transition hover:translate-y-[-1px]"
                      style={{
                        borderColor: "var(--border)",
                        backgroundColor: "var(--surface)",
                        color: "var(--text)",
                      }}
                    >
                      View tenants
                    </Link>
                  </div>
                </div>
              </article>
            ))
          )}
        </div>

        <div className="space-y-6">
          <div
            className="rounded-2xl border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
          >
            <p className="text-sm leading-7" style={{ color: "var(--muted)" }}>
              Authenticated access is required for this view. Use a valid SaaS
              control-plane session to review customer accounts and their linked
              tenant work.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
