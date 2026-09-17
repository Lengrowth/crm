"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Alert } from "@/components/ui/feedback";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Field } from "@/components/ui/input";
import { Input } from "@/components/ui/input";
import { PageHeader } from "@/components/ui/page-header";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { createOrganization } from "@/lib/api";

export default function NewOrganizationPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", legal_name: "", industry: "", country: "", timezone: "UTC", billing_email: "", status: "lead" });
  const [error, setError] = useState<string | null>(null);
  const [fieldError, setFieldError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  function set(key: keyof typeof form, value: string) { setForm((current) => ({ ...current, [key]: value })); setFieldError(null); }
  async function submit(event: React.FormEvent) { event.preventDefault(); setError(null); if (!form.name.trim()) { setFieldError("Company name is required."); return; } if (form.billing_email && !/^\S+@\S+\.\S+$/.test(form.billing_email)) { setFieldError("Enter a valid billing email or leave it blank."); return; } setBusy(true); try { const created = await createOrganization({ ...form, name: form.name.trim(), legal_name: form.legal_name.trim() || undefined, industry: form.industry.trim() || undefined, country: form.country.trim() || undefined, timezone: form.timezone.trim() || undefined, billing_email: form.billing_email.trim() || undefined }); router.push(`/app/organizations/${created.id}`); } catch (cause) { setError(cause instanceof Error ? cause.message : "The company could not be created."); } finally { setBusy(false); } }
  return <div className="space-y-6"><PageHeader eyebrow="Customers" title="Create company" description="Create the customer record that owns ERP sites and delivery work." /><Card className="max-w-3xl"><CardHeader><CardTitle>Company details</CardTitle></CardHeader><CardContent><form className="grid gap-4 md:grid-cols-2" onSubmit={submit} noValidate><Field label="Company name" error={fieldError ?? undefined}><Input autoFocus value={form.name} onChange={(event) => set("name", event.target.value)} placeholder="North Ridge Operations" /></Field><Field label="Legal name"><Input value={form.legal_name} onChange={(event) => set("legal_name", event.target.value)} placeholder="Optional legal entity name" /></Field><Field label="Industry"><Input value={form.industry} onChange={(event) => set("industry", event.target.value)} placeholder="Drilling" /></Field><Field label="Country"><Input value={form.country} onChange={(event) => set("country", event.target.value)} placeholder="United States" /></Field><Field label="Timezone"><Input value={form.timezone} onChange={(event) => set("timezone", event.target.value)} placeholder="UTC" /></Field><Field label="Billing email"><Input type="email" value={form.billing_email} onChange={(event) => set("billing_email", event.target.value)} placeholder="finance@example.test" /></Field><Field label="Initial status"><Select value={form.status} onValueChange={(value) => set("status", value)}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="lead">Lead</SelectItem><SelectItem value="trial">Trial</SelectItem><SelectItem value="active">Active</SelectItem></SelectContent></Select></Field><div className="flex items-end gap-3 md:col-span-2"><Button type="submit" loading={busy}>Create company</Button><Button type="button" variant="ghost" onClick={() => router.back()}>Cancel</Button></div>{error ? <div className="md:col-span-2"><Alert tone="danger">{error}</Alert></div> : null}</form></CardContent></Card></div>;
}
