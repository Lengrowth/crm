"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  fetchTenant,
  listTenantDomains,
  manualActivateDomain,
  provisionTenant,
  getProvisioningStatus,
} from "@/lib/api";

export default function TenantDetailPage() {
  const params = useParams<{ tenantId: string }>();
  const tenantId = params.tenantId;
  const [tenant, setTenant] = useState<any | null>(null);
  const [domains, setDomains] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [provLoading, setProvLoading] = useState(false);
  const [provStatus, setProvStatus] = useState<string | null>(null);
  const [provId, setProvId] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    Promise.all([fetchTenant(tenantId), listTenantDomains(tenantId)])
      .then(([t, d]) => {
        if (!mounted) return;
        setTenant(t);
        setDomains(d || []);
      })
      .catch((err: any) => setError(err?.message ?? "Failed to load tenant"))
      .finally(() => mounted && setLoading(false));

    return () => {
      mounted = false;
    };
  }, [tenantId]);

  useEffect(() => {
    let interval: number | undefined;
    if (provId) {
      setProvLoading(true);
      interval = window.setInterval(async () => {
        try {
          const st = await getProvisioningStatus(provId);
          setProvStatus(st.status ?? String(st));
          if (st.status === "ready" || st.status === "failed") {
            // refresh tenant/domains
            const refreshed = await fetchTenant(tenantId);
            const refreshedDomains = await listTenantDomains(tenantId);
            setTenant(refreshed);
            setDomains(refreshedDomains || []);
            setProvLoading(false);
            if (interval) window.clearInterval(interval);
            setProvId(null);
          }
        } catch (err) {
          // swallow polling errors but stop after a while
          setProvLoading(false);
          if (interval) window.clearInterval(interval);
        }
      }, 2000);
    }
    return () => {
      if (interval) window.clearInterval(interval);
    };
  }, [provId, tenantId]);

  async function handleProvision(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!tenant) return;
    setProvLoading(true);
    const fd = new FormData(event.currentTarget as HTMLFormElement);
    const payload = {
      custom_app: String(fd.get("custom_app") ?? "") || undefined,
      domain: String(fd.get("domain") ?? "") || undefined,
      options: {},
    };

    try {
      const resp = await provisionTenant(
        tenant.organization_id,
        tenant.id,
        payload,
      );
      setProvId(resp.id);
      setProvStatus("queued");
    } catch (err: any) {
      setError(err?.message ?? "Provisioning failed");
      setProvLoading(false);
    }
  }

  async function handleManualActivate(domainId: string, activate: boolean) {
    try {
      const notes = activate
        ? prompt("Optional notes for activation:")
        : undefined;
      const resp = await manualActivateDomain(tenantId, domainId, {
        activate,
        notes,
      });
      setDomains((prev) => prev.map((d) => (d.id === resp.id ? resp : d)));
    } catch (err: any) {
      setError(err?.message ?? "Failed to update domain activation");
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
              Tenant detail
            </p>
            <h1
              className="mt-4 text-4xl font-semibold tracking-tight"
              style={{ color: "var(--text)" }}
            >
              {loading ? "Loading..." : tenant ? tenant.tenant_slug : tenantId}
            </h1>
            <p
              className="mt-4 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {error
                ? error
                : tenant
                  ? `Environment: ${tenant.environment} • Status: ${tenant.status}`
                  : ""}
            </p>
          </div>
          <Link
            href="/app/tenants"
            className="inline-flex rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              backgroundColor: "var(--accent)",
              color: "var(--accent-foreground)",
              boxShadow: "0 16px 32px var(--shadow)",
            }}
          >
            Back to tenants
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
            {tenant ? (
              <div className="mt-3 text-sm" style={{ color: "var(--muted)" }}>
                <div>
                  <strong>Slug:</strong> {tenant.tenant_slug}
                </div>
                <div>
                  <strong>ERPNext site:</strong>{" "}
                  {tenant.erpnext_site_name ?? "-"}
                </div>
                <div>
                  <strong>Provisioning:</strong>{" "}
                  {provStatus ?? tenant.provisioning_status}
                </div>
              </div>
            ) : (
              <p className="mt-3 text-sm" style={{ color: "var(--muted)" }}>
                No tenant data
              </p>
            )}
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
              Domains
            </h2>
            <div className="mt-3 space-y-3">
              {domains.length === 0 ? (
                <p className="text-sm" style={{ color: "var(--muted)" }}>
                  No domains registered for this tenant.
                </p>
              ) : (
                domains.map((d) => (
                  <div
                    key={d.id}
                    className="rounded-lg border p-3"
                    style={{
                      borderColor: "var(--border)",
                      backgroundColor: "var(--surface)",
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div
                          className="text-sm font-semibold"
                          style={{ color: "var(--text)" }}
                        >
                          {d.domain}
                        </div>
                        <div
                          className="text-xs"
                          style={{ color: "var(--muted)" }}
                        >
                          {d.status} • {d.ssl_status}
                        </div>
                      </div>
                      <div>
                        {d.manual_activation_required ? (
                          <button
                            onClick={() => handleManualActivate(d.id, true)}
                            className="rounded-full border px-3 py-1 text-xs font-semibold"
                            style={{
                              borderColor: "var(--border)",
                              backgroundColor: "var(--accent)",
                              color: "var(--accent-foreground)",
                            }}
                          >
                            Manual activate
                          </button>
                        ) : (
                          <span
                            className="text-xs"
                            style={{ color: "var(--muted)" }}
                          >
                            {d.is_active ? "Active" : "Inactive"}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
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
              Provision ERPNext site
            </h2>
            <form className="mt-3 space-y-3" onSubmit={handleProvision}>
              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  ERPNext custom app
                </span>
                <input
                  name="custom_app"
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
                  Domain
                </span>
                <input
                  name="domain"
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface-strong)",
                    color: "var(--text)",
                  }}
                />
              </label>
              <div>
                <button
                  type="submit"
                  disabled={provLoading}
                  className="rounded-full px-4 py-2 text-sm font-semibold transition hover:translate-y-[-1px] disabled:opacity-60"
                  style={{
                    backgroundColor: "var(--accent)",
                    color: "var(--accent-foreground)",
                  }}
                >
                  {provLoading ? "Provisioning..." : "Start provisioning"}
                </button>
                {provStatus ? (
                  <span
                    className="ml-3 text-sm"
                    style={{ color: "var(--muted)" }}
                  >
                    {provStatus}
                  </span>
                ) : null}
              </div>
            </form>
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
              The live tenant edit flow will eventually connect to the protected
              {"PATCH /tenants/{tenantId}"} route.
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
              Related route
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
              Open organizations
            </Link>
          </div>
        </aside>
      </div>
    </div>
  );
}
