"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { fetchOrganizationTenants, createOrganizationTenant } from "@/lib/api";

export default function OrganizationTenantsPage() {
  const router = useRouter();
  const params = useParams<{ organizationId: string }>();
  const organizationId = params.organizationId;
  const [tenants, setTenants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    fetchOrganizationTenants(organizationId)
      .then((data) => mounted && setTenants(data || []))
      .catch((err: any) => setError(err?.message ?? "Failed to load tenants"))
      .finally(() => mounted && setLoading(false));
    return () => {
      mounted = false;
    };
  }, [organizationId]);

  async function handleCreate(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setCreating(true);
    const form = event.currentTarget as HTMLFormElement;
    const fd = new FormData(form);
    const payload = {
      tenant_slug: String(fd.get("tenant_slug") ?? "").trim(),
      environment: String(fd.get("environment") ?? "demo"),
      primary_domain: String(fd.get("primary_domain") ?? "") || undefined,
    };

    try {
      const created = await createOrganizationTenant(organizationId, payload);
      // navigate to tenant detail
      router.push(`/app/tenants/${created.id}`);
    } catch (err: any) {
      setError(err?.message ?? "Failed to create tenant");
    } finally {
      setCreating(false);
    }
  }

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
              Organization tenants
            </p>
            <h1
              className="mt-4 text-4xl font-semibold tracking-tight"
              style={{ color: "var(--text)" }}
            >
              {organizationId}
            </h1>
            <p
              className="mt-4 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              Tenants are scoped to an organization. Create a tenant here and
              open detail to manage provisioning and domains.
            </p>
          </div>
          <form onSubmit={() => {}}>
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
          </form>
        </div>
      </section>

      <div className="grid gap-6 xl:grid-cols-[1fr_0.8fr]">
        <div className="space-y-4">
          {loading ? (
            <p style={{ color: "var(--muted)" }}>Loading tenants...</p>
          ) : error ? (
            <p className="text-sm text-red-500">{error}</p>
          ) : tenants.length === 0 ? (
            <p style={{ color: "var(--muted)" }}>
              No tenants for this organization.
            </p>
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
                      {tenant.environment}
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
          <div
            className="rounded-2xl border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
          >
            <h3
              className="text-sm font-semibold"
              style={{ color: "var(--muted)" }}
            >
              Create tenant
            </h3>
            <form className="mt-4 space-y-3" onSubmit={handleCreate}>
              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Tenant slug
                </span>
                <input
                  name="tenant_slug"
                  required
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface-strong)",
                    color: "var(--text)",
                  }}
                />
              </label>
              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Primary domain
                </span>
                <input
                  name="primary_domain"
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface-strong)",
                    color: "var(--text)",
                  }}
                />
              </label>
              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Environment
                </span>
                <select
                  name="environment"
                  defaultValue="demo"
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface-strong)",
                    color: "var(--text)",
                  }}
                >
                  <option value="demo">demo</option>
                  <option value="staging">staging</option>
                  <option value="production">production</option>
                </select>
              </label>
              <div>
                <button
                  type="submit"
                  disabled={creating}
                  className="rounded-full px-4 py-2 text-sm font-semibold transition hover:translate-y-[-1px] disabled:opacity-60"
                  style={{
                    backgroundColor: "var(--accent)",
                    color: "var(--accent-foreground)",
                  }}
                >
                  {creating ? "Creating..." : "Create tenant"}
                </button>
              </div>
            </form>
          </div>

          <div
            className="rounded-2xl border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
          >
            <h3
              className="text-sm font-semibold"
              style={{ color: "var(--muted)" }}
            >
              Notes
            </h3>
            <p className="mt-2 text-sm" style={{ color: "var(--muted)" }}>
              New tenants are created as SaaS metadata records. Provisioning,
              domains and ERPNext integration are managed separately.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
