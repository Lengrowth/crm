"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Search } from "lucide-react";
import { StatusBadge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { EmptyState, ErrorState, Skeleton } from "@/components/ui/feedback";
import { Input } from "@/components/ui/input";
import { PageHeader } from "@/components/ui/page-header";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { fetchImplementationPortfolio } from "@/lib/api";
import type { ImplementationPortfolio } from "@/features/implementation/types";

export default function PortfolioClient() {
  const [portfolio, setPortfolio] = useState<ImplementationPortfolio | null>(null);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setPortfolio(await fetchImplementationPortfolio());
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Implementation work is unavailable.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void load(); }, [load]);

  const projects = useMemo(
    () => portfolio?.projects.filter((project) =>
      (!query || `${project.organization_name} ${project.tenant_slug} ${project.status}`.toLowerCase().includes(query.toLowerCase()))
      && (status === "all" || project.status === status)
    ) ?? [],
    [portfolio, query, status],
  );

  if (loading) return <div className="space-y-6"><PageHeader eyebrow="Delivery" title="Implementation portfolio" description="Loading implementation projects and task progress." /><div className="grid gap-4 sm:grid-cols-3"><Skeleton className="h-24" /><Skeleton className="h-24" /><Skeleton className="h-24" /></div><Skeleton className="h-72" /></div>;
  if (error || !portfolio) return <ErrorState title="Implementation portfolio unavailable" description={error ?? "No portfolio read model was returned."} onRetry={() => void load()} />;

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Delivery" title="Implementation portfolio" description="Track real project progress, blockers, and overdue tasks across accessible companies." actions={<Button variant="ghost" onClick={() => void load()}>Refresh</Button>} />
      <div className="grid gap-4 sm:grid-cols-3"><SummaryCard label="Projects" value={portfolio.project_count} /><SummaryCard label="Blockers" value={portfolio.blocker_count} tone={portfolio.blocker_count ? "danger" : "success"} /><SummaryCard label="Overdue tasks" value={portfolio.overdue_task_count} tone={portfolio.overdue_task_count ? "warning" : "success"} /></div>
      <Card><CardContent><div className="flex flex-col gap-3 md:flex-row"><div className="relative flex-1"><Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2" style={{ color: "var(--color-muted)" }} aria-hidden="true" /><Input className="pl-9" aria-label="Search implementation projects" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search company, site, or project status" /></div><Select value={status} onValueChange={setStatus}><SelectTrigger aria-label="Filter projects by status" className="w-48"><SelectValue /></SelectTrigger><SelectContent>{["all", "discovery", "planning", "setup", "configuration", "training", "go_live", "closed", "archived"].map((item) => <SelectItem key={item} value={item}>{item === "all" ? "All statuses" : item}</SelectItem>)}</SelectContent></Select></div></CardContent></Card>
      {!projects.length ? <EmptyState title={portfolio.project_count ? "No projects match" : "No implementation projects"} description={portfolio.project_count ? "Try another search or status filter." : "Projects will appear when the protected implementation API has records."} /> : <Table><TableHeader><TableRow><TableHead>Company / site</TableHead><TableHead>Phase</TableHead><TableHead>Progress</TableHead><TableHead>Attention</TableHead><TableHead>Tasks</TableHead></TableRow></TableHeader><TableBody>{projects.map((project) => <TableRow key={project.id}><TableCell><div className="font-bold">{project.organization_name}</div><div className="mt-1 text-xs" style={{ color: "var(--color-muted)" }}>{project.tenant_slug}</div></TableCell><TableCell><StatusBadge status={project.status} /></TableCell><TableCell><div className="min-w-32"><div className="flex justify-between text-xs"><span>{project.progress_percent}%</span><span style={{ color: "var(--color-muted)" }}>{project.completed_task_count}/{project.task_count}</span></div><div className="mt-2 h-1.5 overflow-hidden rounded-full" style={{ background: "var(--color-surface-muted)" }}><div className="h-full rounded-full" style={{ width: `${project.progress_percent}%`, background: "var(--accent)" }} /></div></div></TableCell><TableCell>{project.blocker_count || project.overdue_task_count ? <div className="flex flex-wrap gap-2">{project.blocker_count ? <StatusBadge status="blocked" /> : null}{project.overdue_task_count ? <StatusBadge status="warning" /> : null}</div> : <span className="text-xs" style={{ color: "var(--color-muted)" }}>No attention flags</span>}</TableCell><TableCell>{project.tasks.length ? <><ul className="space-y-1 text-xs">{project.tasks.slice(0, 3).map((task) => <li key={task.id} className="flex items-center gap-2"><StatusBadge status={task.status} /><span>{task.title}</span></li>)}</ul>{project.tasks_truncated ? <p className="mt-1 text-[11px]" style={{ color: "var(--color-warning)" }}>Showing the first 100 tasks.</p> : null}</> : <span style={{ color: "var(--color-muted)" }}>No tasks</span>}</TableCell></TableRow>)}</TableBody></Table>}
      {portfolio.truncated ? <p className="text-xs" style={{ color: "var(--color-warning)" }}>This portfolio is bounded to the first 250 projects. Narrow the backend scope before reviewing older records.</p> : null}
    </div>
  );
}

function SummaryCard({ label, value, tone = "info" }: { label: string; value: number; tone?: "info" | "warning" | "danger" | "success" }) { return <Card><CardHeader><CardTitle className="flex items-center justify-between"><span>{label}</span><StatusBadge status={tone === "info" ? "planned" : tone} /></CardTitle></CardHeader><CardContent><p className="text-3xl font-black">{value}</p></CardContent></Card>; }
