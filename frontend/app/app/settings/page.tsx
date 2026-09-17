"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ErrorState, Skeleton } from "@/components/ui/feedback";
import { PageHeader } from "@/components/ui/page-header";
import { env } from "@/lib/env";
import { fetchRuntimeRelease, isPhaseOneShellEnabled, type RuntimeRelease } from "@/lib/runtime-config";

export default function SettingsPage() {
  const [runtime, setRuntime] = useState<RuntimeRelease | null>(null); const [loading, setLoading] = useState(true); const [error, setError] = useState<string | null>(null);
  useEffect(() => { fetchRuntimeRelease().then(setRuntime).catch((cause) => setError(cause instanceof Error ? "Runtime configuration is unavailable." : "Runtime configuration is unavailable.")).finally(() => setLoading(false)); }, []);
  if (loading) return <div className="space-y-6"><PageHeader eyebrow="System" title="Settings" description="Loading supported runtime configuration." /><Skeleton className="h-80" /></div>;
  if (error || !runtime) return <ErrorState title="Settings unavailable" description={error ?? "No runtime configuration was returned."} />;
  return <div className="space-y-6"><PageHeader eyebrow="System" title="Settings" description="Review supported product, environment, security, and support configuration." /><div className="grid gap-6 lg:grid-cols-2"><ReadOnlySection title="Product"><ReadOnlyRow label="Application" value={env.appName} /><ReadOnlyRow label="Environment" value={env.environmentLabel} /><ReadOnlyRow label="Status" value={env.statusLabel} /></ReadOnlySection><ReadOnlySection title="Runtime"><ReadOnlyRow label="Release" value={runtime.release_id} mono /><ReadOnlyRow label="Commit" value={runtime.commit} mono /><ReadOnlyRow label="Build environment" value={runtime.environment} /><ReadOnlyRow label="Phase 1 shell" value={<Badge tone={isPhaseOneShellEnabled(runtime) ? "success" : "warning"}>{isPhaseOneShellEnabled(runtime) ? "Enabled" : "Legacy fallback"}</Badge>} /></ReadOnlySection><ReadOnlySection title="Security"><ReadOnlyRow label="Authentication" value="Protected session required" /><ReadOnlyRow label="Secrets" value="Not displayed in the operator workspace" /><ReadOnlyRow label="Tenant boundary" value="Enforced by the protected API" /></ReadOnlySection><ReadOnlySection title="Support and operations"><ReadOnlyRow label="Support" value={<a className="underline underline-offset-4" href={env.supportUrl}>Open support</a>} /><ReadOnlyRow label="Status page" value={env.statusUrl ? <a className="underline underline-offset-4" href={env.statusUrl}>Open status</a> : "Not configured"} /><ReadOnlyRow label="Runtime refresh" value="Reload the page to read the server configuration" /></ReadOnlySection></div></div>;
}

function ReadOnlySection({ title, children }: { title: string; children: React.ReactNode }) { return <Card><CardHeader><CardTitle>{title}</CardTitle></CardHeader><CardContent className="divide-y" style={{ borderColor: "var(--color-border)" }}>{children}</CardContent></Card>; }
function ReadOnlyRow({ label, value, mono }: { label: string; value: React.ReactNode; mono?: boolean }) { return <div className="flex flex-col gap-1 py-3 first:pt-0 last:pb-0 sm:flex-row sm:items-center sm:justify-between"><span className="text-sm" style={{ color: "var(--color-muted)" }}>{label}</span><span className={mono ? "font-mono text-xs" : "text-sm"}>{value}</span></div>; }
