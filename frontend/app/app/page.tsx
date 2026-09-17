"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { Alert, EmptyState, ErrorState, Skeleton } from "@/components/ui/feedback";
import { Badge, StatusBadge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader } from "@/components/ui/page-header";
import { fetchDashboardSummary, fetchOrganizations, fetchTenants } from "@/lib/api";
import type { DashboardSummary } from "@/features/dashboard/types";
import type { OrganizationRecord } from "@/features/organizations/types";
import type { TenantRecord } from "@/features/tenants/types";

function label(value: string) { return value.replaceAll("_", " "); }

export default function AppHomePage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [organizations, setOrganizations] = useState<OrganizationRecord[]>([]);
  const [tenants, setTenants] = useState<TenantRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [partial, setPartial] = useState<string[]>([]);

  const load = useCallback(async () => {
    setLoading(true); setError(null); setPartial([]);
    const [summaryResult, organizationsResult, tenantsResult] = await Promise.allSettled([fetchDashboardSummary(), fetchOrganizations(), fetchTenants()]);
    if (summaryResult.status === "fulfilled") setSummary(summaryResult.value);
    else { setSummary(null); setError(summaryResult.reason instanceof Error ? summaryResult.reason.message : "The operational summary is unavailable."); }
    const optionalFailures: string[] = [];
    if (organizationsResult.status === "fulfilled") setOrganizations(organizationsResult.value);
    else optionalFailures.push("company list");
    if (tenantsResult.status === "fulfilled") setTenants(tenantsResult.value);
    else optionalFailures.push("site list");
    setPartial(optionalFailures);
    setLoading(false);
  }, []);

  useEffect(() => { void load(); }, [load]);

  if (loading) return <div className="space-y-6"><PageHeader eyebrow="Overview" title="Operational overview" description="Loading the current control-plane state." /><div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{Array.from({ length: 4 }, (_, index) => <Skeleton key={index} className="h-28" />)}</div><Skeleton className="h-56" /></div>;
  if (error || !summary) return <ErrorState title="Operational overview unavailable" description={error ?? "The dashboard did not return a usable summary."} onRetry={() => void load()} />;

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Overview" title="Operational overview" description="See customer, ERP site, delivery, and runtime work that needs attention." actions={<><Link className="ui-button ui-button-primary" href="/app/organizations/new">New company</Link><Link className="ui-button ui-button-secondary" href="/app/tenants/new">New ERP site</Link></>} />
      {partial.length ? <Alert tone="warning" title="Some supporting data is unavailable">The summary is current, but the {partial.join(" and ")} could not be loaded. Retry when the API is available.</Alert> : null}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Companies" value={summary.organization_count} href="/app/organizations" detail={summary.organization_status_counts.active ? `${summary.organization_status_counts.active} active` : "Review company status"} />
        <MetricCard label="ERP sites" value={summary.tenant_count} href="/app/tenants" detail={summary.provisioning_status_counts.ready ? `${summary.provisioning_status_counts.ready} ready` : "Review site readiness"} />
        <MetricCard label="Failed jobs" value={summary.failed_job_count} href="/app/tenants" tone={summary.failed_job_count ? "danger" : "success"} detail={summary.failed_job_count ? "Needs operator review" : "No failed jobs reported"} />
        <MetricCard label="Delivery attention" value={summary.implementation_blocker_count + summary.overdue_task_count} href="/app/implementation" tone={summary.implementation_blocker_count + summary.overdue_task_count ? "warning" : "success"} detail={`${summary.implementation_blocker_count} blockers · ${summary.overdue_task_count} overdue`} />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.15fr_.85fr]">
        <Card><CardHeader><CardTitle>Next actions</CardTitle></CardHeader><CardContent className="space-y-3">{summary.next_actions.length ? summary.next_actions.map((action) => <Link key={`${action.href}-${action.label}`} href={action.href} className="flex items-center justify-between rounded-xl border p-3 transition hover:bg-[var(--color-surface-muted)]" style={{ borderColor: "var(--color-border)" }}><span className="text-sm font-semibold">{action.label}</span><Badge tone={action.tone}>{label(action.tone)}</Badge></Link>) : <EmptyState title="No prioritized actions" description="The API did not report a current blocker, warning, failed job, or overdue task." />}</CardContent></Card>
        <Card><CardHeader><CardTitle>Site readiness</CardTitle></CardHeader><CardContent><div className="space-y-3">{Object.entries(summary.provisioning_status_counts).length ? Object.entries(summary.provisioning_status_counts).map(([status, count]) => <div key={status} className="flex items-center justify-between border-b pb-3 last:border-0 last:pb-0" style={{ borderColor: "var(--color-border)" }}><span className="text-sm capitalize" style={{ color: "var(--color-muted)" }}>{label(status)}</span><StatusBadge status={status} /><span className="text-sm font-bold">{count}</span></div>) : <p className="text-sm" style={{ color: "var(--color-muted)" }}>No site status records are available.</p>}</div></CardContent></Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card><CardHeader><div className="flex items-center justify-between gap-3"><CardTitle>Companies</CardTitle><Link className="text-xs font-bold underline underline-offset-4" href="/app/organizations">View all</Link></div></CardHeader><CardContent>{organizations.length ? <div className="space-y-3">{organizations.slice(0, 5).map((organization) => <div key={organization.id} className="flex items-center justify-between gap-4 border-b pb-3 last:border-0 last:pb-0" style={{ borderColor: "var(--color-border)" }}><div className="min-w-0"><Link className="truncate text-sm font-bold hover:underline" href={`/app/organizations/${organization.id}`}>{organization.name}</Link><p className="text-xs capitalize" style={{ color: "var(--color-muted)" }}>{organization.industry ?? "Industry not set"}</p></div><StatusBadge status={organization.status} /></div>)}</div> : <EmptyState title="No companies yet" description="Create a company to begin a customer rollout." action={{ label: "Create company", href: "/app/organizations/new" }} />}</CardContent></Card>
        <Card><CardHeader><div className="flex items-center justify-between gap-3"><CardTitle>ERP sites</CardTitle><Link className="text-xs font-bold underline underline-offset-4" href="/app/tenants">View all</Link></div></CardHeader><CardContent>{tenants.length ? <div className="space-y-3">{tenants.slice(0, 5).map((tenant) => <div key={tenant.id} className="flex items-center justify-between gap-4 border-b pb-3 last:border-0 last:pb-0" style={{ borderColor: "var(--color-border)" }}><div className="min-w-0"><Link className="truncate text-sm font-bold hover:underline" href={`/app/tenants/${tenant.id}`}>{tenant.tenant_slug}</Link><p className="text-xs" style={{ color: "var(--color-muted)" }}>{tenant.primary_domain ?? "Domain not configured"}</p></div><StatusBadge status={tenant.provisioning_status} /></div>)}</div> : <EmptyState title="No ERP sites yet" description="Create a site record to track its environment and readiness." action={{ label: "Create ERP site", href: "/app/tenants/new" }} />}</CardContent></Card>
      </div>

      {summary.failed_job_count || summary.domain_warning_count ? <Card><CardHeader><CardTitle>Warnings</CardTitle></CardHeader><CardContent className="grid gap-3 md:grid-cols-2">{summary.provisioning_failures.map((failure) => <Alert key={failure.id} tone="danger" title={`Provisioning failed for ${failure.tenant_slug ?? "an ERP site"}`}>Review the site record and retry only after confirming the cause.</Alert>)}{summary.domain_warnings.map((warning) => <Alert key={warning.id} tone="warning" title={warning.domain ?? "Domain warning"}>{warning.tenant_slug ?? "ERP site"} · {label(warning.status ?? "unknown")} · SSL {label(warning.ssl_status ?? "unknown")}</Alert>)}</CardContent></Card> : null}
      <div className="flex justify-end"><Button variant="ghost" onClick={() => void load()}>Refresh data</Button></div>
    </div>
  );
}

function MetricCard({ label: metricLabel, value, detail, href, tone = "info" }: { label: string; value: number; detail: string; href: string; tone?: "info" | "warning" | "danger" | "success" }) {
  return <Link href={href} className="ui-card block p-5 transition hover:-translate-y-0.5 hover:shadow-[var(--shadow-md)]"><div className="flex items-center justify-between gap-3"><span className="text-xs font-bold uppercase tracking-[.14em]" style={{ color: "var(--color-muted)" }}>{metricLabel}</span><Badge tone={tone}>{tone === "info" ? "View" : tone}</Badge></div><p className="mt-4 text-3xl font-black tracking-tight">{value}</p><p className="mt-1 text-xs" style={{ color: "var(--color-muted)" }}>{detail}</p></Link>;
}
