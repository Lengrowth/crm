"use client";

import { useEffect, useState } from "react";
import { Alert, EmptyState, ErrorState, Skeleton } from "@/components/ui/feedback";
import { Badge, StatusBadge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader } from "@/components/ui/page-header";
import { approveOperatorOnboarding, authorizeOperatorOnboarding, beginOperatorOnboardingReview, convertOperatorOnboarding, fetchOperatorOnboarding, fetchOperatorProvisioningEvents, fetchOperatorProvisioningJob, retryOperatorProvisioningStep } from "@/lib/api";
import type { OperatorOnboardingRead, ProvisioningEventRead, ProvisioningJobDetailRead } from "@/features/onboarding/types";

type JobView = { detail: ProvisioningJobDetailRead; events: ProvisioningEventRead[] };

function progressLabel(stepKey: string) {
  if (stepKey === "install_pinned_hrms") return "Installing People & Payroll capability";
  if (stepKey === "install_pinned_erpnext") return "Installing ERP platform capability";
  if (stepKey === "install_lenerp_custom_app") return "Installing LenERP operational capability";
  if (stepKey === "verify_apps_modules") return "Verifying installed applications and module access";
  return stepKey.replaceAll("_", " ");
}

export default function OnboardingQueuePage() {
  const [items, setItems] = useState<OperatorOnboardingRead[]>([]);
  const [jobs, setJobs] = useState<Record<string, JobView>>({});
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  async function load() {
    setLoading(true); setError(null);
    try { setItems(await fetchOperatorOnboarding()); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "The onboarding queue could not be loaded."); }
    finally { setLoading(false); }
  }

  useEffect(() => { void load(); }, []);

  async function act(id: string, operation: (item: OperatorOnboardingRead) => Promise<OperatorOnboardingRead>, success: string) {
    const item = items.find((entry) => entry.request_id === id); if (!item) return;
    setWorking(id); setError(null); setMessage(null);
    try { const next = await operation(item); setItems((current) => current.map((entry) => entry.request_id === id ? next : entry)); setMessage(success); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "The operator action could not be completed."); }
    finally { setWorking(null); }
  }

  async function loadJob(jobId: string) {
    setWorking(jobId); setError(null);
    try {
      const [detail, events] = await Promise.all([fetchOperatorProvisioningJob(jobId), fetchOperatorProvisioningEvents(jobId)]);
      setJobs((current) => ({ ...current, [jobId]: { detail, events } }));
    } catch (cause) { setError(cause instanceof Error ? cause.message : "The provisioning workflow could not be loaded."); }
    finally { setWorking(null); }
  }

  async function retryStep(jobId: string, stepKey: string) {
    const irreversible = stepKey === "create_isolated_site" || stepKey === "bind_domain_ssl";
    if (irreversible && !window.confirm(`Retry ${stepKey}? This step requires explicit operator confirmation.`)) return;
    setWorking(`${jobId}:${stepKey}`); setError(null); setMessage(null);
    try {
      const detail = await retryOperatorProvisioningStep(jobId, stepKey, irreversible ? "confirm_irreversible_step" : "retry_safe_step", `Operator recovery retry for ${stepKey}.`);
      const events = await fetchOperatorProvisioningEvents(jobId);
      setJobs((current) => ({ ...current, [jobId]: { detail, events } })); setMessage(`${stepKey} queued for recovery.`);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "The provisioning step could not be retried."); }
    finally { setWorking(null); }
  }

  if (loading) return <div className="space-y-6"><PageHeader eyebrow="Delivery / onboarding" title="Onboarding queue" description="Review versioned public requests before any control-plane conversion or isolated execution." /><Skeleton className="h-72" /></div>;
  if (error && !items.length) return <ErrorState title="Onboarding queue unavailable" description={error} onRetry={() => void load()} />;

  return <div className="space-y-6">
    <PageHeader eyebrow="Delivery / onboarding" title="Onboarding queue" description="Every execution action is server-authorized, version-bound, and separate from public module selection." actions={<Button variant="secondary" onClick={() => void load()}>Refresh</Button>} />
    {error ? <Alert tone="danger">{error}</Alert> : null}{message ? <Alert tone="success">{message}</Alert> : null}
    {!items.length ? <EmptyState title="No onboarding requests" description="Public requests will appear here only after the intake flag is enabled." /> : <div className="space-y-4">{items.map((item) => {
      const job = item.provisioning_job_id ? jobs[item.provisioning_job_id] : undefined;
      return <Card key={item.request_id}><CardHeader><div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between"><div><CardTitle>{String(item.snapshot.company_name ?? "Unnamed company")}</CardTitle><p className="mt-1 font-mono text-xs" style={{ color: "var(--muted)" }}>{item.request_id} · v{item.current_version}</p></div><StatusBadge status={item.state} /></div></CardHeader><CardContent className="space-y-4">
        <div className="grid gap-3 text-sm sm:grid-cols-3"><div><span style={{ color: "var(--muted)" }}>Administrator</span><p>{String(item.snapshot.administrator_email ?? "Not provided")}</p></div><div><span style={{ color: "var(--muted)" }}>Requested modules</span><p>{item.requested_modules.join(", ") || "None selected"}</p></div><div><span style={{ color: "var(--muted)" }}>Target</span><p>Isolated synthetic lane</p></div></div>
        <div className="flex flex-wrap items-center gap-2">{item.state === "submitted" ? <Button loading={working === item.request_id} onClick={() => void act(item.request_id, (entry) => beginOperatorOnboardingReview(entry.request_id, entry.current_version, "Operator review started."), "Request moved to review.")}>Begin review</Button> : null}{item.state === "under_review" ? <Button loading={working === item.request_id} onClick={() => void act(item.request_id, (entry) => approveOperatorOnboarding(entry.request_id, entry.current_version, "Approved exact submitted version after preflight."), "Exact request version approved.")}>Approve exact version</Button> : null}{item.state === "approved" && !item.organization_id ? <Button variant="secondary" loading={working === item.request_id} onClick={() => void act(item.request_id, (entry) => convertOperatorOnboarding(entry.request_id), "Request converted transactionally; execution is still disabled until separately authorized.")}>Convert control-plane records</Button> : null}{item.state === "approved" && item.provisioning_job_id ? <Button loading={working === item.request_id} onClick={() => void act(item.request_id, (entry) => authorizeOperatorOnboarding(entry.request_id, entry.current_version, "Authorized isolated synthetic execution after target-bound confirmation."), "Isolated execution authorized.")}>Authorize synthetic execution</Button> : null}{item.state === "provisioning" ? <Badge tone="info">Worker execution enabled for this approved request</Badge> : null}{item.state === "ready" ? <Badge tone="success">Verified isolated tenant ready</Badge> : null}{item.provisioning_job_id ? <Button variant="ghost" loading={working === item.provisioning_job_id} onClick={() => void loadJob(item.provisioning_job_id!)}>Show durable job</Button> : null}</div>
        {item.rejection_reason ? <Alert tone="warning">{item.rejection_reason}</Alert> : null}
        {job ? <div className="space-y-3 rounded-xl border p-4" style={{ borderColor: "var(--border)" }}><div className="flex flex-wrap items-center justify-between gap-2"><p className="font-semibold">{job.detail.workflow_version} · {job.detail.status} · {job.detail.attempt_count} job attempt{job.detail.attempt_count === 1 ? "" : "s"}</p><Button variant="ghost" onClick={() => void loadJob(job.detail.job_id)}>Refresh job</Button></div><ol className="grid gap-2 md:grid-cols-2">{job.detail.steps.map((step) => <li key={step.id} className="rounded-lg border p-3 text-sm" style={{ borderColor: "var(--border)" }}><div className="flex items-center justify-between gap-2"><span>{step.ordinal}. {progressLabel(step.step_key)}</span><StatusBadge status={step.status} /></div><details className="mt-2 text-xs"><summary className="cursor-pointer underline underline-offset-2" style={{ color: "var(--muted)" }}>Technical detail</summary><p className="mt-1 font-mono">{step.step_key}</p></details>{step.sanitized_error ? <p className="mt-2 text-xs" style={{ color: "var(--danger)" }}>{step.sanitized_error}</p> : null}{["failed", "queued"].includes(step.status) && !["success", "cancelled"].includes(job.detail.status) ? <Button className="mt-2" variant="secondary" loading={working === `${job.detail.job_id}:${step.step_key}`} onClick={() => void retryStep(job.detail.job_id, step.step_key)}>Retry step</Button> : null}</li>)}</ol><div><p className="text-xs font-semibold uppercase tracking-[0.16em]" style={{ color: "var(--muted)" }}>Safe event log</p><ul className="mt-2 space-y-1 text-xs" role="log">{job.events.slice(0, 12).map((event) => <li key={event.id}>{event.event_code} · {event.public_message}</li>)}</ul></div></div> : null}
      </CardContent></Card>;
    })}</div>}
  </div>;
}
