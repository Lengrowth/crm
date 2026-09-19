"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { Alert, EmptyState, ErrorState, Skeleton } from "@/components/ui/feedback";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { fetchModuleBundles, fetchModuleCatalog, fetchOrganizations, fetchOrganizationModules, previewOrganizationModules, applyOrganizationModules } from "@/lib/api";
import type { ModuleBundle, ModulePreview, ModuleSummary, ModuleEffective } from "@/features/modules/types";
import type { OrganizationRecord } from "@/features/organizations/types";

export default function AppModulesPage() {
  const [catalog, setCatalog] = useState<ModuleSummary[]>([]);
  const [organizations, setOrganizations] = useState<OrganizationRecord[]>([]);
  const [bundles, setBundles] = useState<ModuleBundle[]>([]);
  const [effective, setEffective] = useState<ModuleEffective | null>(null);
  const [preview, setPreview] = useState<ModulePreview | null>(null);
  const [organizationId, setOrganizationId] = useState("");
  const [selectedCodes, setSelectedCodes] = useState<string[]>([]);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [bundleKey, setBundleKey] = useState("none");
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const viewVersion = useRef(0);

  useEffect(() => {
    void Promise.all([fetchModuleCatalog(), fetchOrganizations(), fetchModuleBundles()])
      .then(([modules, companies, availableBundles]) => {
        setCatalog(modules); setOrganizations(companies); setBundles(availableBundles);
        if (companies[0]) setOrganizationId(companies[0].id);
      })
      .catch((cause) => setError(cause instanceof Error ? cause.message : "The module catalog could not be loaded."))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!organizationId) return;
    const version = ++viewVersion.current;
    setPreview(null); setMessage(null);
    void fetchOrganizationModules(organizationId)
      .then((result) => { if (version !== viewVersion.current) return; setEffective(result); setSelectedCodes(result.requested_codes); })
      .catch((cause) => setError(cause instanceof Error ? cause.message : "The company modules could not be loaded."));
  }, [organizationId]);

  const categories = useMemo(() => Array.from(new Set(catalog.map((item) => item.category).filter(Boolean))).sort() as string[], [catalog]);
  const visible = useMemo(() => catalog.filter((item) => item.name.toLowerCase().includes(query.toLowerCase()) && (category === "all" || item.category === category)), [catalog, category, query]);

  function toggle(code: string) { viewVersion.current += 1; setSelectedCodes((current) => current.includes(code) ? current.filter((item) => item !== code) : [...current, code]); setPreview(null); }
  async function previewSelection() {
    if (!organizationId) return;
    const version = viewVersion.current;
    const requestedOrganization = organizationId;
    const requestedCodes = [...selectedCodes];
    const requestedBundle = bundleKey;
    setWorking(true); setError(null); setMessage(null);
    try { const result = await previewOrganizationModules(requestedOrganization, { enable_codes: requestedCodes, disable_codes: (effective?.requested_codes ?? []).filter((code) => !requestedCodes.includes(code)), bundle_key: requestedBundle === "none" ? undefined : requestedBundle }); if (version === viewVersion.current && requestedOrganization === organizationId && requestedBundle === bundleKey && requestedCodes.join("\u0000") === selectedCodes.join("\u0000")) setPreview(result); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "The module preview could not be created."); }
    finally { setWorking(false); }
  }
  async function applyPreview() {
    if (!preview || !organizationId || !window.confirm("Save these module changes?")) return;
    const version = viewVersion.current;
    const applyingOrganization = organizationId;
    const applyingPreviewHash = preview.preview_hash;
    setWorking(true); setError(null);
    try { const result = await applyOrganizationModules(applyingOrganization, { enable_codes: preview.requested_enable_codes, disable_codes: preview.requested_disable_codes, clear_codes: preview.requested_clear_codes, bundle_key: bundleKey === "none" ? undefined : bundleKey, preview_hash: applyingPreviewHash, idempotency_key: `modules-${applyingPreviewHash}` }); if (version === viewVersion.current && applyingOrganization === organizationId && preview?.preview_hash === applyingPreviewHash) { setEffective(result.effective); setPreview(null); setSelectedCodes(result.effective.requested_codes); setMessage(result.replayed ? "The same request was safely saved again." : "Module choices saved."); } }
    catch (cause) { setError(cause instanceof Error ? cause.message : "The module change could not be applied."); }
    finally { setWorking(false); }
  }

  if (loading) return <div className="space-y-6"><Skeleton className="h-28" /><Skeleton className="h-96" /></div>;
  if (error && !catalog.length) return <ErrorState title="Modules unavailable" description={error} />;
  return <div className="space-y-6">
    <section className="rounded-[2rem] border p-8 lg:p-10" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface)", boxShadow: "0 24px 60px var(--shadow)" }}>
      <p className="text-xs font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>Available modules</p>
      <h1 className="mt-4 text-4xl font-semibold tracking-tight" style={{ color: "var(--text)" }}>Choose the tools your company needs.</h1>
      <p className="mt-4 max-w-3xl text-sm leading-7" style={{ color: "var(--muted)" }}>Review the capabilities available to each company, preview the setup, and save clear module choices.</p>
    </section>
    {error ? <Alert tone="danger">{error}</Alert> : null}{message ? <Alert tone="success">{message}</Alert> : null}
    <Card><CardHeader><CardTitle>Company setup</CardTitle></CardHeader><CardContent className="grid gap-4 md:grid-cols-3">
      <Field label="Company"><Select value={organizationId} onValueChange={setOrganizationId}><SelectTrigger><SelectValue placeholder="Choose a company" /></SelectTrigger><SelectContent>{organizations.map((organization) => <SelectItem key={organization.id} value={organization.id}>{organization.name}</SelectItem>)}</SelectContent></Select></Field>
      <Field label="Recommended setup"><Select value={bundleKey} onValueChange={(value) => { viewVersion.current += 1; setBundleKey(value); setPreview(null); }}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="none">Choose modules individually</SelectItem>{bundles.map((bundle) => <SelectItem key={`${bundle.bundle_key}-${bundle.version}`} value={bundle.bundle_key}>{bundle.name}</SelectItem>)}</SelectContent></Select></Field>
      <div className="flex items-end gap-3"><Button onClick={() => void previewSelection()} loading={working} disabled={!organizationId}>Preview</Button><Button variant="secondary" onClick={() => void applyPreview()} disabled={!preview || working}>Apply preview</Button></div>
    </CardContent></Card>
    {preview ? <Card><CardHeader><CardTitle>Review your changes</CardTitle></CardHeader><CardContent className="space-y-3 text-sm"><p>Add: {preview.requested_enable_codes.map((code) => catalog.find((item) => item.code === code)?.name).filter(Boolean).join(", ") || "none"}</p><p>Remove: {preview.requested_disable_codes.map((code) => catalog.find((item) => item.code === code)?.name).filter(Boolean).join(", ") || "none"}</p><p>Additional modules included: {preview.dependency_additions.map((code) => catalog.find((item) => item.code === code)?.name).filter(Boolean).join(", ") || "none"}</p><p style={{ color: "var(--muted)" }}>Your selections are saved for this company and reviewed as part of setup.</p></CardContent></Card> : null}
    <Card><CardHeader><CardTitle>Available modules</CardTitle><div className="flex flex-wrap gap-3"><Input aria-label="Search modules" placeholder="Search modules" value={query} onChange={(event) => setQuery(event.target.value)} /><Select value={category} onValueChange={setCategory}><SelectTrigger className="w-48"><SelectValue /></SelectTrigger><SelectContent><SelectItem value="all">All categories</SelectItem>{categories.map((item) => <SelectItem key={item} value={item}>{item}</SelectItem>)}</SelectContent></Select></div></CardHeader><CardContent>{visible.length === 0 ? <EmptyState title="No modules match" description="Try a different search or category." /> : <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{visible.map((module) => { const item = effective?.items.find((candidate) => candidate.code === module.code); const dependencies = module.dependency_codes.map((code) => catalog.find((candidate) => candidate.code === code)?.name).filter(Boolean); const status = item?.entitled ? (item.verification_state === "verified" ? "Ready" : "Setup in progress") : "Available"; return <article key={module.code} className="rounded-2xl border p-5" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface-strong)" }}><div className="flex items-start justify-between gap-3"><div><p className="text-sm font-semibold" style={{ color: "var(--text)" }}>{module.name}</p></div><Badge>{module.category ?? "General"}</Badge></div><p className="mt-3 text-sm leading-6" style={{ color: "var(--muted)" }}>{module.public_description ?? module.description ?? "No description provided."}</p><div className="mt-4 flex flex-wrap gap-2"><Badge>{status}</Badge></div>{dependencies.length ? <p className="mt-3 text-xs" style={{ color: "var(--muted)" }}>Also includes: {dependencies.join(", ")}</p> : null}<label className="mt-4 flex items-center gap-2 text-sm"><input type="checkbox" checked={selectedCodes.includes(module.code)} onChange={() => toggle(module.code)} aria-label={`Select ${module.name}`} />Select</label></article>; })}</div>}</CardContent></Card>
  </div>;
}
