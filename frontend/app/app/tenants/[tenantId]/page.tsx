"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { Alert, EmptyState, ErrorState, Skeleton } from "@/components/ui/feedback";
import { StatusBadge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ConfirmAction } from "@/components/ui/confirm-action";
import { Field, Input } from "@/components/ui/input";
import { PageHeader } from "@/components/ui/page-header";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { fetchSsoReadiness, fetchTenant, listProvisioningJobs, listTenantDomains, manualActivateDomain, reactivateTenant, suspendTenant, updateTenant } from "@/lib/api";
import type { DomainRecord, ProvisioningJobRecord, TenantRecord } from "@/features/tenants/types";

export default function TenantDetailPage() {
  const { tenantId } = useParams<{ tenantId: string }>();
  const [tenant, setTenant] = useState<TenantRecord | null>(null);
  const [domains, setDomains] = useState<DomainRecord[]>([]);
  const [jobs, setJobs] = useState<ProvisioningJobRecord[]>([]);
  const [ssoReadiness, setSsoReadiness] = useState<Awaited<ReturnType<typeof fetchSsoReadiness>> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [partial, setPartial] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [form, setForm] = useState({ tenant_slug: "", environment: "demo", status: "planned", primary_domain: "", custom_domain: "", erpnext_site_name: "", erpnext_base_url: "", provisioning_status: "pending" });

  const load = useCallback(async () => {
    setLoading(true); setError(null); setPartial([]);
    try {
      const record = await fetchTenant(tenantId);
      setTenant(record);
      setForm({ tenant_slug: record.tenant_slug, environment: record.environment, status: record.status, primary_domain: record.primary_domain ?? "", custom_domain: record.custom_domain ?? "", erpnext_site_name: record.erpnext_site_name ?? "", erpnext_base_url: record.erpnext_base_url ?? "", provisioning_status: record.provisioning_status });
      const [domainResult, jobsResult, ssoResult] = await Promise.allSettled([listTenantDomains(tenantId), listProvisioningJobs(tenantId), fetchSsoReadiness(tenantId)]);
      const failures: string[] = [];
      if (domainResult.status === "fulfilled") setDomains(domainResult.value); else failures.push("domain status");
      if (jobsResult.status === "fulfilled") setJobs(jobsResult.value); else failures.push("job history");
      if (ssoResult.status === "fulfilled") setSsoReadiness(ssoResult.value); else failures.push("central sign-in readiness");
      setPartial(failures);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "The ERP site could not be loaded."); }
    finally { setLoading(false); }
  }, [tenantId]);

  useEffect(() => { void load(); }, [load]);

  async function save(event: React.FormEvent) {
    event.preventDefault();
    if (!tenant || !form.tenant_slug.trim()) { setError("Site slug is required."); return; }
    setSaving(true); setError(null); setMessage(null);
    try {
      const updated = await updateTenant(tenant.id, { ...form, tenant_slug: form.tenant_slug.trim(), primary_domain: form.primary_domain.trim() || undefined, custom_domain: form.custom_domain.trim() || undefined, erpnext_site_name: form.erpnext_site_name.trim() || undefined, erpnext_base_url: form.erpnext_base_url.trim() || undefined });
      setTenant(updated); setMessage("ERP site details saved.");
    } catch (cause) { setError(cause instanceof Error ? cause.message : "The ERP site could not be updated."); }
    finally { setSaving(false); }
  }

  async function lifecycle(action: "suspend" | "reactivate") {
    if (!tenant) return;
    setError(null);
    try {
      const updated = action === "suspend" ? await suspendTenant(tenant.id, "Operator action from site detail") : await reactivateTenant(tenant.id, "Operator action from site detail");
      setTenant(updated); setForm((current) => ({ ...current, status: updated.status }));
    } catch (cause) { setError(cause instanceof Error ? cause.message : "The site status could not be changed."); }
  }

  async function activateDomain(domain: DomainRecord) {
    try {
      const updated = await manualActivateDomain(tenantId, domain.id, { activate: true, notes: "Confirmed by operator" });
      setDomains((items) => items.map((item) => item.id === updated.id ? updated : item));
    } catch (cause) { setError(cause instanceof Error ? cause.message : "The domain could not be activated."); }
  }

  if (loading) return <div className="space-y-6"><Skeleton className="h-28" /><Skeleton className="h-96" /></div>;
  if (!tenant) return <ErrorState title="ERP site unavailable" description={error ?? "The site record is unavailable."} onRetry={() => void load()} />;
  const attentionDomains = domains.filter((domain) => domain.manual_activation_required || !domain.is_active || domain.ssl_status === "unknown" || !["active", "verified", "ready"].includes(domain.status));
  const identityStartUrl = tenant.erpnext_base_url ? `${tenant.erpnext_base_url.replace(/\/$/, "")}/app` : null;

  return <div className="space-y-6">
    <PageHeader eyebrow="Customers / ERP site" title={tenant.tenant_slug} description={`${tenant.environment} · ${tenant.primary_domain ?? "Domain not configured"}`} actions={<><Link className="ui-button ui-button-secondary" href={`/app/organizations/${tenant.organization_id}/tenants`}>Company sites</Link><Link className="ui-button ui-button-ghost" href="/app/tenants">All ERP sites</Link></>} />
    {partial.length ? <Alert tone="warning" title="Some site data is unavailable">The record is current, but {partial.join(" and ")} could not be loaded.</Alert> : null}
    {error ? <Alert tone="danger">{error}</Alert> : null}
    <div className="flex flex-wrap items-center gap-2"><StatusBadge status={tenant.status} /><StatusBadge status={tenant.provisioning_status} />{tenant.status === "suspended" ? <ConfirmAction label="Reactivate site" variant="secondary" title="Reactivate this ERP site?" description="The site will return to ready status for operators." confirmLabel="Reactivate" onConfirm={() => lifecycle("reactivate")} /> : <ConfirmAction label="Suspend site" title="Suspend this ERP site?" description="This changes the site lifecycle status." onConfirm={() => lifecycle("suspend")} />}</div>
    <Tabs defaultValue="overview"><TabsList><TabsTrigger value="overview">Overview</TabsTrigger><TabsTrigger value="domains">Domains {attentionDomains.length ? `(${attentionDomains.length})` : ""}</TabsTrigger><TabsTrigger value="jobs">Job history</TabsTrigger></TabsList>
      <TabsContent value="overview" className="pt-5"><div className="grid gap-6 lg:grid-cols-[1fr_.42fr]">
        <Card><CardHeader><CardTitle>Edit site details</CardTitle></CardHeader><CardContent><form className="grid gap-4 md:grid-cols-2" onSubmit={save}><Field label="Site slug"><Input value={form.tenant_slug} onChange={(event) => setForm({ ...form, tenant_slug: event.target.value })} /></Field><Field label="Environment"><Select value={form.environment} onValueChange={(value) => setForm({ ...form, environment: value })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="demo">Demo</SelectItem><SelectItem value="staging">Staging</SelectItem><SelectItem value="production">Production</SelectItem></SelectContent></Select></Field><Field label="Primary domain"><Input value={form.primary_domain} onChange={(event) => setForm({ ...form, primary_domain: event.target.value })} /></Field><Field label="Custom domain"><Input value={form.custom_domain} onChange={(event) => setForm({ ...form, custom_domain: event.target.value })} /></Field><Field label="ERP site name"><Input value={form.erpnext_site_name} onChange={(event) => setForm({ ...form, erpnext_site_name: event.target.value })} /></Field><Field label="ERP base URL"><Input value={form.erpnext_base_url} onChange={(event) => setForm({ ...form, erpnext_base_url: event.target.value })} /></Field><Field label="Lifecycle status"><Select value={form.status} onValueChange={(value) => setForm({ ...form, status: value })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent>{["planned", "provisioning", "ready", "suspended", "failed", "archived"].map((item) => <SelectItem key={item} value={item}>{item}</SelectItem>)}</SelectContent></Select></Field><Field label="Provisioning status"><Select value={form.provisioning_status} onValueChange={(value) => setForm({ ...form, provisioning_status: value })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent>{["pending", "queued", "running", "ready", "failed"].map((item) => <SelectItem key={item} value={item}>{item}</SelectItem>)}</SelectContent></Select></Field><div className="flex items-center gap-3 md:col-span-2"><Button type="submit" loading={saving}>Save changes</Button>{message ? <span className="text-sm" style={{ color: "var(--color-success)" }} role="status">{message}</span> : null}</div></form></CardContent></Card>
        <div className="space-y-6"><Card><CardHeader><CardTitle>Open ERP</CardTitle></CardHeader><CardContent className="space-y-4"><p className="text-sm leading-6" style={{ color: "var(--color-muted)" }}>Destination: {tenant.erpnext_base_url ?? "Not configured"}<br />Organization: {ssoReadiness?.organization_name ?? tenant.organization_id}<br />Environment: {tenant.environment}</p>{ssoReadiness?.ready && identityStartUrl ? <Link className="ui-button ui-button-primary" href={identityStartUrl} aria-label={`Open ERP for ${ssoReadiness.organization_name}`}>Open ERP in this tab</Link> : <div className="rounded-xl border px-4 py-3 text-sm" style={{ borderColor: "var(--color-border)", color: "var(--color-muted)" }} role="status">{ssoReadiness?.explanation ?? "Central sign-in readiness is being checked."}</div>}</CardContent></Card><Card><CardHeader><CardTitle>Provisioning</CardTitle></CardHeader><CardContent className="space-y-4"><p className="text-sm leading-6" style={{ color: "var(--color-muted)" }}>Direct provisioning is retired. Use the reviewed onboarding queue so the approved request, bundle, synthetic target, and execution authorization remain linked.</p><Link className="ui-button ui-button-primary" href="/app/onboarding">Open onboarding queue</Link></CardContent></Card></div>
      </div></TabsContent>
      <TabsContent value="domains" className="pt-5"><Card><CardHeader><CardTitle>Domains and SSL</CardTitle></CardHeader><CardContent>{!domains.length ? <EmptyState title="No domains registered" description="Domain records will appear here when the control plane has them." /> : <div className="space-y-3">{domains.map((domain) => <div key={domain.id} className="flex flex-col gap-3 rounded-xl border p-4 sm:flex-row sm:items-center sm:justify-between" style={{ borderColor: "var(--color-border)" }}><div><p className="font-bold">{domain.domain}</p><div className="mt-1 flex flex-wrap gap-2"><StatusBadge status={domain.status} /><StatusBadge status={domain.ssl_status} />{domain.manual_activation_required ? <span className="text-xs" style={{ color: "var(--color-warning)" }}>Manual activation required</span> : null}</div></div>{domain.manual_activation_required ? <ConfirmAction label="Activate domain" variant="secondary" title="Activate this domain?" description="Confirm DNS and SSL readiness before marking this domain active." confirmLabel="Activate" onConfirm={() => activateDomain(domain)} /> : null}</div>)}</div>}</CardContent></Card></TabsContent>
      <TabsContent value="jobs" className="pt-5"><Card><CardHeader><CardTitle>Provisioning job history</CardTitle></CardHeader><CardContent>{!jobs.length ? <EmptyState title="No provisioning jobs" description="Jobs will appear after a controlled provisioning action." /> : <div className="space-y-3">{jobs.map((job) => <div key={job.id} className="flex items-center justify-between gap-3 rounded-xl border p-4" style={{ borderColor: "var(--color-border)" }}><div><p className="font-bold">{job.job_type}</p><p className="mt-1 text-xs" style={{ color: "var(--color-muted)" }}>{job.attempt_count} attempt{job.attempt_count === 1 ? "" : "s"}</p></div><StatusBadge status={job.status} /></div>)}</div>}</CardContent></Card></TabsContent>
    </Tabs>
  </div>;
}
