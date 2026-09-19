"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader } from "@/components/ui/page-header";
import { env } from "@/lib/env";

export default function SettingsPage() {
  const workspaceLabel = env.environmentLabel.toLowerCase() === "production"
    ? "Live workspace"
    : "Demo workspace";

  return <div className="space-y-6">
    <PageHeader eyebrow="Account" title="Settings" description="Review your workspace, security, and support options." />
    <div className="grid gap-6 lg:grid-cols-2">
      <ReadOnlySection title="Workspace">
        <ReadOnlyRow label="Application" value={env.appName} />
        <ReadOnlyRow label="Workspace type" value={workspaceLabel} />
        <ReadOnlyRow label="Service status" value={env.statusLabel} />
      </ReadOnlySection>
      <ReadOnlySection title="Security">
        <ReadOnlyRow label="Authentication" value="Protected sign-in required" />
        <ReadOnlyRow label="Data access" value="Limited to your authorized companies and sites" />
        <ReadOnlyRow label="Secrets" value="Never displayed in the workspace" />
      </ReadOnlySection>
      <ReadOnlySection title="Support">
        <ReadOnlyRow label="Help" value={<a className="underline underline-offset-4" href={env.supportUrl}>Contact support</a>} />
        <ReadOnlyRow label="Service updates" value={env.statusUrl ? <a className="underline underline-offset-4" href={env.statusUrl}>View service status</a> : "Contact support for help"} />
      </ReadOnlySection>
    </div>
  </div>;
}

function ReadOnlySection({ title, children }: { title: string; children: React.ReactNode }) {
  return <Card><CardHeader><CardTitle>{title}</CardTitle></CardHeader><CardContent className="divide-y" style={{ borderColor: "var(--color-border)" }}>{children}</CardContent></Card>;
}

function ReadOnlyRow({ label, value }: { label: string; value: React.ReactNode }) {
  return <div className="flex flex-col gap-1 py-3 first:pt-0 last:pb-0 sm:flex-row sm:items-center sm:justify-between"><span className="text-sm" style={{ color: "var(--color-muted)" }}>{label}</span><span className="text-sm">{value}</span></div>;
}
