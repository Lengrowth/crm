"use client";

import { useEffect, useMemo, useState } from "react";
import { Alert } from "@/components/ui/feedback";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/input";
import { createPublicOnboarding, fetchPublicModuleCatalog, submitPublicOnboarding } from "@/lib/api";

type PublicModule = { code: string; name: string; category: string | null; description: string; display_order: number };

export default function OnboardingPage() {
  const [catalog, setCatalog] = useState<PublicModule[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [token, setToken] = useState<string | null>(null);
  const [requestId, setRequestId] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [form, setForm] = useState({ company_name: "", legal_name: "", industry: "", country: "", administrator_name: "", administrator_email: "", desired_domain: "", implementation_notes: "" });

  useEffect(() => { void fetchPublicModuleCatalog().then(setCatalog).catch(() => setError("The public module catalog is temporarily unavailable.")); }, []);
  const grouped = useMemo(() => catalog.reduce<Record<string, PublicModule[]>>((groups, item) => { const key = item.category ?? "platform"; groups[key] = [...(groups[key] ?? []), item]; return groups; }, {}), [catalog]);
  function set(key: keyof typeof form, value: string) { setForm((current) => ({ ...current, [key]: value })); }
  function toggle(code: string) { setSelected((current) => current.includes(code) ? current.filter((item) => item !== code) : [...current, code]); }
  async function submit(event: React.FormEvent) {
    event.preventDefault(); setBusy(true); setError(null); setStatus(null);
    try {
      const result = await createPublicOnboarding(`public-${crypto.randomUUID()}`, { ...form, requested_modules: selected, desired_infrastructure: "isolated_synthetic", branding: {}, expected_users: [], applicant_revision: 1 });
      setRequestId(result.request_id); setToken(result.management_token ?? null); setStatus(result.applicant_visible_status);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "The request could not be saved."); }
    finally { setBusy(false); }
  }
  async function submitForReview() {
    if (!requestId || !token) return;
    setBusy(true); setError(null);
    try { const result = await submitPublicOnboarding(requestId, token); setStatus(result.applicant_visible_status); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "The request could not be submitted."); }
    finally { setBusy(false); }
  }
  if (status) return <div className="mx-auto max-w-3xl space-y-6 py-12"><Card><CardHeader><CardTitle>Request received for review</CardTitle></CardHeader><CardContent className="space-y-5"><Alert tone="success">Your request has been saved for review. No company, billing record, domain, or ERP workspace has been created.</Alert><dl className="grid gap-4 sm:grid-cols-2 text-sm"><div><dt style={{ color: "var(--muted)" }}>Request status</dt><dd className="mt-1 font-semibold capitalize">{status}</dd></div><div><dt style={{ color: "var(--muted)" }}>Request reference</dt><dd className="mt-1 font-mono text-xs break-all">{requestId}</dd></div></dl>{token ? <div className="rounded-xl border p-4" style={{ borderColor: "var(--border)" }}><p className="text-sm font-semibold">Save your private request access code</p><p className="mt-1 text-xs leading-5" style={{ color: "var(--muted)" }}>It is shown once, scoped to this request, and is not included in the request URL.</p><code className="mt-3 block break-all rounded-lg p-3 text-xs" style={{ background: "var(--surface-strong)" }}>{token}</code></div> : null}<Button loading={busy} onClick={() => void submitForReview()} disabled={!token}>Send for review</Button></CardContent></Card></div>;
  return <div className="mx-auto max-w-5xl space-y-10 py-12"><div className="max-w-2xl"><p className="text-xs font-semibold uppercase tracking-[0.28em]" style={{ color: "var(--accent)" }}>Workspace setup</p><h1 className="mt-4 text-5xl font-semibold tracking-[-0.05em]" style={{ color: "var(--text)" }}>Tell us what your team needs.</h1><p className="mt-5 text-lg leading-8" style={{ color: "var(--muted)" }}>Share a few details and choose the capabilities you want to review. We will follow up before anything is created or activated.</p></div>{error ? <Alert tone="danger">{error}</Alert> : null}<form onSubmit={submit} className="grid gap-6 lg:grid-cols-[1fr_.9fr]"><Card><CardHeader><CardTitle>Company and administrator</CardTitle></CardHeader><CardContent className="grid gap-4 sm:grid-cols-2"><Field label="Company name"><Input required value={form.company_name} onChange={(event) => set("company_name", event.target.value)} /></Field><Field label="Legal name"><Input value={form.legal_name} onChange={(event) => set("legal_name", event.target.value)} /></Field><Field label="Industry"><Input value={form.industry} onChange={(event) => set("industry", event.target.value)} placeholder="Field service" /></Field><Field label="Country"><Input value={form.country} onChange={(event) => set("country", event.target.value)} /></Field><Field label="Administrator name"><Input required value={form.administrator_name} onChange={(event) => set("administrator_name", event.target.value)} /></Field><Field label="Administrator email"><Input required type="email" value={form.administrator_email} onChange={(event) => set("administrator_email", event.target.value)} /></Field><Field label="Desired domain" hint="A domain reservation is reviewed separately; no DNS is changed by this form."><Input value={form.desired_domain} onChange={(event) => set("desired_domain", event.target.value)} placeholder="portal.example.com" /></Field><Field label="Implementation notes"><Input value={form.implementation_notes} onChange={(event) => set("implementation_notes", event.target.value)} /></Field></CardContent></Card><Card><CardHeader><CardTitle>Requested capabilities</CardTitle></CardHeader><CardContent className="space-y-5">{Object.entries(grouped).map(([category, items]) => <fieldset key={category}><legend className="mb-2 text-xs font-semibold uppercase tracking-[0.18em]" style={{ color: "var(--muted)" }}>{category}</legend><div className="space-y-2">{items.map((item) => <label key={item.code} className="flex cursor-pointer gap-3 rounded-xl border p-3" style={{ borderColor: "var(--border)" }}><input type="checkbox" checked={selected.includes(item.code)} onChange={() => toggle(item.code)} /><span><span className="block text-sm font-semibold">{item.name}</span><span className="block text-xs leading-5" style={{ color: "var(--muted)" }}>{item.description}</span></span></label>)}</div></fieldset>)}<p className="text-xs leading-5" style={{ color: "var(--muted)" }}>We will review compatibility and dependencies with you. This request does not grant access or start setup.</p><Button type="submit" loading={busy} disabled={!catalog.length}>Save request</Button></CardContent></Card></form></div>;
}
