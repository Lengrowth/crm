"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Search, SlidersHorizontal } from "lucide-react";
import { Badge, StatusBadge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { EmptyState, ErrorState, Skeleton } from "@/components/ui/feedback";
import { Input } from "@/components/ui/input";
import { PageHeader } from "@/components/ui/page-header";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { fetchOrganizations } from "@/lib/api";
import type { OrganizationRecord, OrganizationStatus } from "@/features/organizations/types";

const statuses: Array<OrganizationStatus | "all"> = ["all", "lead", "trial", "active", "suspended", "cancelled", "archived"];

export default function OrganizationsPage() {
  const [organizations, setOrganizations] = useState<OrganizationRecord[]>([]);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<OrganizationStatus | "all">("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const load = useCallback(async () => { setLoading(true); setError(null); try { setOrganizations(await fetchOrganizations()); } catch (cause) { setError(cause instanceof Error ? cause.message : "Companies are unavailable."); } finally { setLoading(false); } }, []);
  useEffect(() => { void load(); }, [load]);
  const filtered = useMemo(() => organizations.filter((organization) => { const haystack = [organization.name, organization.legal_name, organization.industry, organization.country].filter(Boolean).join(" ").toLowerCase(); return (!query || haystack.includes(query.toLowerCase())) && (status === "all" || organization.status === status); }), [organizations, query, status]);

  return <div className="space-y-6"><PageHeader eyebrow="Customers" title="Companies" description="Review customer accounts and move into site and delivery work." actions={<Link className="ui-button ui-button-primary" href="/app/organizations/new">Create company</Link>} /><Card><CardContent><div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between"><div className="relative flex-1"><Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2" style={{ color: "var(--color-muted)" }} aria-hidden="true" /><Input aria-label="Search companies" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search by name, industry, or country" className="pl-9" /></div><div className="flex items-center gap-2"><SlidersHorizontal className="h-4 w-4" style={{ color: "var(--color-muted)" }} aria-hidden="true" /><Select value={status} onValueChange={(value) => setStatus(value as OrganizationStatus | "all")}><SelectTrigger aria-label="Filter by company status" className="w-44"><SelectValue /></SelectTrigger><SelectContent>{statuses.map((item) => <SelectItem key={item} value={item}>{item === "all" ? "All statuses" : item}</SelectItem>)}</SelectContent></Select></div></div></CardContent></Card>{loading ? <Skeleton className="h-72" /> : error ? <ErrorState description={error} onRetry={() => void load()} /> : !filtered.length ? <EmptyState title={organizations.length ? "No companies match" : "No companies yet"} description={organizations.length ? "Try a different search or status filter." : "Create a company record to begin a customer rollout."} action={!organizations.length ? { label: "Create company", href: "/app/organizations/new" } : undefined} /> : <Table><TableHeader><TableRow><TableHead>Company</TableHead><TableHead>Industry</TableHead><TableHead>Location</TableHead><TableHead>Status</TableHead><TableHead><span className="sr-only">Actions</span></TableHead></TableRow></TableHeader><TableBody>{filtered.map((organization) => <TableRow key={organization.id}><TableCell><Link className="font-bold hover:underline" href={`/app/organizations/${organization.id}`}>{organization.name}</Link><p className="mt-1 text-xs" style={{ color: "var(--color-muted)" }}>{organization.legal_name ?? "Legal name not set"}</p></TableCell><TableCell className="capitalize">{organization.industry ?? "—"}</TableCell><TableCell>{[organization.country, organization.timezone].filter(Boolean).join(" · ") || "—"}</TableCell><TableCell><StatusBadge status={organization.status} /></TableCell><TableCell><div className="flex flex-wrap justify-end gap-2"><Link className="ui-button ui-button-secondary" href={`/app/organizations/${organization.id}`}>Open</Link><Link className="ui-button ui-button-ghost" href={`/app/organizations/${organization.id}/tenants`}>Sites</Link></div></TableCell></TableRow>)}</TableBody></Table>}<div className="flex items-center justify-between text-xs" style={{ color: "var(--color-muted)" }}><span>{filtered.length} of {organizations.length} companies</span><Button variant="ghost" onClick={() => void load()}>Refresh</Button></div></div>;
}
