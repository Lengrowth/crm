"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { fetchOrganization } from "@/lib/api";

export default function OrganizationDetailPage() {
  const params = useParams<{ organizationId: string }>();
  const organizationId = params.organizationId;
  const [org, setOrg] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    fetchOrganization(organizationId)
      .then((data) => mounted && setOrg(data))
      .catch((err: any) =>
        setError(err?.message ?? "Failed to load organization"),
      )
      .finally(() => mounted && setLoading(false));
    return () => {
      mounted = false;
    };
  }, [organizationId]);

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
              Organization detail
            </p>
            <h1
              className="mt-4 text-4xl font-semibold tracking-tight"
              style={{ color: "var(--text)" }}
            >
              {loading ? "Loading..." : org ? org.name : organizationId}
            </h1>
            <p
              className="mt-4 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {error
                ? error
                : org
                  ? `Industry: ${org.industry ?? "-"} • Status: ${org.status}`
                  : "This organization could not be loaded."}
            </p>
          </div>
          <Link
            href={`/app/organizations/${organizationId}/tenants`}
            className="inline-flex rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              backgroundColor: "var(--accent)",
              color: "var(--accent-foreground)",
              boxShadow: "0 16px 32px var(--shadow)",
            }}
          >
            View tenants
          </Link>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6">
          <div
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
              Profile
            </h2>
            <p className="mt-2 text-sm" style={{ color: "var(--muted)" }}>
              {org ? (
                <>
                  <strong>Name:</strong> {org.name}
                  <br />
                  <strong>Industry:</strong> {org.industry ?? "-"}
                  <br />
                  <strong>Billing:</strong> {org.billing_email ?? "-"}
                </>
              ) : (
                <span style={{ color: "var(--muted)" }}>
                  No organization data
                </span>
              )}
            </p>
          </div>

          <div
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
              Tenants
            </h2>
            <p className="mt-2 text-sm" style={{ color: "var(--muted)" }}>
              Tenants are managed under the organization. View the tenants list
              to create or open tenant records.
            </p>
            <div className="mt-4">
              <Link
                href={`/app/organizations/${organizationId}/tenants`}
                className="inline-flex rounded-full border px-4 py-2 text-sm font-semibold transition hover:translate-y-[-1px]"
                style={{
                  borderColor: "var(--border)",
                  backgroundColor: "var(--surface)",
                  color: "var(--text)",
                }}
              >
                Open tenants
              </Link>
            </div>
          </div>
        </div>

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
              Edit
            </h2>
            <p
              className="mt-3 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              The live edit form is available via the PATCH endpoint; implement
              in a follow-up if you'd like inline editing.
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
              Back to list
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
              Open organization list
            </Link>
          </div>
        </aside>
      </div>
    </div>
  );
}
