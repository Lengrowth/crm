"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { Alert, EmptyState, ErrorState, Skeleton } from "@/components/ui/feedback";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader } from "@/components/ui/page-header";
import { fetchOrganization, fetchOrganizationModuleAudit, fetchOrganizationModules } from "@/lib/api";
import type { ModuleAudit, ModuleEffective } from "@/features/modules/types";
import type { OrganizationRecord } from "@/features/organizations/types";

export default function OrganizationModulesPage() {
  const { organizationId } = useParams<{ organizationId: string }>();
  const [organization, setOrganization] = useState<OrganizationRecord | null>(null);
  const [effective, setEffective] = useState<ModuleEffective | null>(null);
  const [audit, setAudit] = useState<ModuleAudit[]>([]);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { void Promise.all([fetchOrganization(organizationId), fetchOrganizationModules(organizationId), fetchOrganizationModuleAudit(organizationId)]).then(([company, modules, events]) => { setOrganization(company); setEffective(modules); setAudit(events); }).catch((cause) => setError(cause instanceof Error ? cause.message : "Company modules could not be loaded.")); }, [organizationId]);
  if (error) return <ErrorState title="Modules unavailable" description={error} />;
  if (!organization || !effective) return <div className="space-y-6"><Skeleton className="h-24" /><Skeleton className="h-80" /></div>;
  const entitled = effective.items.filter((item) => item.entitled);
  return <div className="space-y-6"><PageHeader eyebrow="Company / Modules" title={organization.name} description="Review requested, entitled, applied, verified, hidden, and needs-attention states for this company." actions={<Link className="ui-button ui-button-secondary" href={`/app/organizations/${organization.id}`}>Back to company</Link>} />
    <Alert tone="info">Module choices are shown here with their current setup status.</Alert>
    <Card><CardHeader><CardTitle>Selected modules</CardTitle></CardHeader><CardContent>{entitled.length === 0 ? <EmptyState title="No modules selected" description="Choose modules for this company to see them here." /> : <div className="grid gap-4 md:grid-cols-2">{entitled.map((item) => <article key={item.code} className="rounded-2xl border p-5" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface-strong)" }}><div className="flex items-start justify-between gap-3"><h2 className="font-semibold" style={{ color: "var(--text)" }}>{item.name}</h2><Badge tone={item.needs_attention ? "warning" : "success"}>{item.states.join(" · ")}</Badge></div><p className="mt-3 text-sm" style={{ color: "var(--muted)" }}>{item.explanation.join("; ")}</p>{item.required_app ? <p className="mt-3 text-xs" style={{ color: "var(--muted)" }}>Backing application: {item.required_app}</p> : null}{item.state_reasons.length ? <p className="mt-2 text-xs" style={{ color: "var(--muted)" }}>{item.state_reasons.join(" ")}</p> : null}</article>)}</div>}</CardContent></Card>
    <Card><CardHeader><CardTitle>Recent changes</CardTitle></CardHeader><CardContent>{audit.length === 0 ? <EmptyState title="No module changes" description="Changes to this company’s modules will appear here." /> : <div className="space-y-3">{audit.map((event) => { const previousBundle = event.previous_bundle_key ? `${event.previous_bundle_key}@${event.previous_bundle_version ?? "?"}` : "none"; const newBundle = event.new_bundle_key ? `${event.new_bundle_key}@${event.new_bundle_version ?? "?"}` : "individual changes"; const tenantIds = event.tenant_ids.length ? event.tenant_ids.join(", ") : event.tenant_id ?? "none attached"; return <article key={event.id} className="rounded-xl border p-4 text-sm" style={{ borderColor: "var(--border)" }}><div className="flex flex-wrap justify-between gap-2"><span className="font-semibold">Module choices updated</span><time style={{ color: "var(--muted)" }}>{new Date(event.created_at).toLocaleString()}</time></div><p className="mt-2" style={{ color: "var(--muted)" }}>{event.reason ?? "No additional details."}</p><p className="mt-2 text-xs" style={{ color: "var(--muted)" }}>Tenant(s): {tenantIds} · Bundle: {previousBundle} → {newBundle}</p></article>; })}</div>}</CardContent></Card>
  </div>;
}
