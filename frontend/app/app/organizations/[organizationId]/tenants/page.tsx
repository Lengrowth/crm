"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { createOrganizationTenant, fetchOrganization, fetchOrganizationTenants } from "@/lib/api";
import { Alert, EmptyState, ErrorState, Skeleton } from "@/components/ui/feedback";
import { StatusBadge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/input";
import { PageHeader } from "@/components/ui/page-header";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { OrganizationRecord } from "@/features/organizations/types";
import type { TenantRecord } from "@/features/tenants/types";

export default function OrganizationTenantsPage() {
  const { organizationId } = useParams<{ organizationId: string }>(); const router = useRouter();
  const [organization, setOrganization] = useState<OrganizationRecord | null>(null); const [tenants, setTenants] = useState<TenantRecord[]>([]); const [loading, setLoading] = useState(true); const [error, setError] = useState<string | null>(null); const [creating, setCreating] = useState(false); const [form, setForm] = useState({ tenant_slug: "", environment: "demo", primary_domain: "" });
  const load = useCallback(async () => { setLoading(true); setError(null); try { const [org, sites] = await Promise.all([fetchOrganization(organizationId), fetchOrganizationTenants(organizationId)]); setOrganization(org); setTenants(sites); } catch (cause) { setError(cause instanceof Error ? cause.message : "The company sites could not be loaded."); } finally { setLoading(false); } }, [organizationId]);
  useEffect(() => { void load(); }, [load]);
  async function create(event: React.FormEvent) { event.preventDefault(); if (!form.tenant_slug.trim()) { setError("Site slug is required."); return; } setCreating(true); setError(null); try { const created = await createOrganizationTenant(organizationId, { tenant_slug: form.tenant_slug.trim(), environment: form.environment, primary_domain: form.primary_domain.trim() || undefined }); router.push(`/app/tenants/${created.id}`); } catch (cause) { setError(cause instanceof Error ? cause.message : "The ERP site could not be created."); } finally { setCreating(false); } }
  if (loading) return <div className="space-y-6"><Skeleton className="h-28" /><Skeleton className="h-64" /></div>;
  if (!organization) return <ErrorState title="Company unavailable" description={error ?? "The company record is unavailable."} onRetry={() => void load()} />;
  return <div className="space-y-6"><PageHeader eyebrow="Customers / ERP sites" title={organization.name} description="Manage ERP sites that belong to this company." actions={<Link className="ui-button ui-button-secondary" href={`/app/organizations/${organization.id}`}>Company details</Link>} /><div className="grid gap-6 xl:grid-cols-[1fr_.42fr]"><Card><CardHeader><CardTitle>ERP sites</CardTitle></CardHeader><CardContent>{error ? <Alert tone="danger">{error}</Alert> : tenants.length ? <div className="space-y-3">{tenants.map((tenant) => <div key={tenant.id} className="flex flex-col gap-3 rounded-xl border p-4 sm:flex-row sm:items-center sm:justify-between" style={{ borderColor: "var(--color-border)" }}><div><Link className="font-bold hover:underline" href={`/app/tenants/${tenant.id}`}>{tenant.tenant_slug}</Link><p className="mt-1 text-xs" style={{ color: "var(--color-muted)" }}>{tenant.environment} · {tenant.primary_domain ?? "Domain not set"}</p></div><div className="flex items-center gap-2"><StatusBadge status={tenant.status} /><Link className="ui-button ui-button-secondary" href={`/app/tenants/${tenant.id}`}>Open</Link></div></div>)}</div> : <EmptyState title="No ERP sites yet" description="Add the first site for this company." />}</CardContent></Card><Card><CardHeader><CardTitle>Add ERP site</CardTitle></CardHeader><CardContent><form className="space-y-4" onSubmit={create}><Field label="Site slug"><Input autoFocus value={form.tenant_slug} onChange={(event) => setForm({ ...form, tenant_slug: event.target.value })} placeholder="north-ridge-demo" /></Field><Field label="Primary domain"><Input value={form.primary_domain} onChange={(event) => setForm({ ...form, primary_domain: event.target.value })} placeholder="north-ridge.example.test" /></Field><Field label="Environment"><Select value={form.environment} onValueChange={(value) => setForm({ ...form, environment: value })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="demo">Demo</SelectItem><SelectItem value="staging">Staging</SelectItem><SelectItem value="production">Production</SelectItem></SelectContent></Select></Field><Button type="submit" loading={creating}>Create ERP site</Button></form></CardContent></Card></div></div>;
}
