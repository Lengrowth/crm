"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { fetchOrganization, updateOrganization } from "@/lib/api";

type OrganizationFormState = {
  name: string;
  legal_name: string;
  industry: string;
  country: string;
  timezone: string;
  billing_email: string;
  status: string;
};

export default function OrganizationDetailPage() {
  const params = useParams<{ organizationId: string }>();
  const organizationId = params.organizationId;
  const [org, setOrg] = useState<any | null>(null);
  const [form, setForm] = useState<OrganizationFormState>({
    name: "",
    legal_name: "",
    industry: "",
    country: "",
    timezone: "",
    billing_email: "",
    status: "lead",
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    fetchOrganization(organizationId)
      .then((data) => mounted && setOrg(data))
      .catch((err: any) =>
        setError(err?.message ?? "Failed to load organization"),
      )
      .finally(() => mounted && setLoading(false));
    return () => {
      mounted = false;
    };
  }, [organizationId]);

  useEffect(() => {
    if (!org) return;

    setForm({
      name: org.name ?? "",
      legal_name: org.legal_name ?? "",
      industry: org.industry ?? "",
      country: org.country ?? "",
      timezone: org.timezone ?? "",
      billing_email: org.billing_email ?? "",
      status: org.status ?? "lead",
    });
  }, [org]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!org) return;

    setSaving(true);
    setSaveError(null);
    setSaveMessage(null);

    try {
      const updated = await updateOrganization(org.id, {
        name: form.name.trim(),
        legal_name: form.legal_name.trim() || undefined,
        industry: form.industry.trim() || undefined,
        country: form.country.trim() || undefined,
        timezone: form.timezone.trim() || undefined,
        billing_email: form.billing_email.trim() || undefined,
        status: form.status,
      });

      setOrg(updated);
      setSaveMessage("Organization updated successfully.");
    } catch (submitError) {
      setSaveError(
        submitError instanceof Error
          ? submitError.message
          : "Unable to update the organization.",
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6">
      <section
        className="rounded-[2rem] border p-8 lg:p-10"
        style={{
          borderColor: "var(--border)",
          backgroundColor: "var(--surface)",
          boxShadow: "0 24px 60px var(--shadow)",
        }}
      >
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl">
            <p
              className="text-xs font-semibold uppercase tracking-[0.24em]"
              style={{ color: "var(--muted)" }}
            >
              Organization detail
            </p>
            <h1
              className="mt-4 text-4xl font-semibold tracking-tight"
              style={{ color: "var(--text)" }}
            >
              {loading ? "Loading..." : org ? org.name : organizationId}
            </h1>
            <p
              className="mt-4 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {error
                ? error
                : org
                  ? `Industry: ${org.industry ?? "-"} • Status: ${org.status}`
                  : "This organization could not be loaded."}
            </p>
          </div>
          <Link
            href={`/app/organizations/${organizationId}/tenants`}
            className="inline-flex rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              backgroundColor: "var(--accent)",
              color: "var(--accent-foreground)",
              boxShadow: "0 16px 32px var(--shadow)",
            }}
          >
            View tenants
          </Link>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6">
          <div
            className="rounded-2xl border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
          >
            <h2
              className="text-xl font-semibold"
              style={{ color: "var(--text)" }}
            >
              Profile
            </h2>
            <p className="mt-2 text-sm" style={{ color: "var(--muted)" }}>
              {org ? (
                <>
                  <strong>Name:</strong> {org.name}
                  <br />
                  <strong>Industry:</strong> {org.industry ?? "-"}
                  <br />
                  <strong>Billing:</strong> {org.billing_email ?? "-"}
                </>
              ) : (
                <span style={{ color: "var(--muted)" }}>
                  No organization data
                </span>
              )}
            </p>
          </div>

          <div
            className="rounded-2xl border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
          >
            <h2
              className="text-xl font-semibold"
              style={{ color: "var(--text)" }}
            >
              Tenants
            </h2>
            <p className="mt-2 text-sm" style={{ color: "var(--muted)" }}>
              Tenants are managed under the organization. View the tenants list
              to create or open tenant records.
            </p>
            <div className="mt-4">
              <Link
                href={`/app/organizations/${organizationId}/tenants`}
                className="inline-flex rounded-full border px-4 py-2 text-sm font-semibold transition hover:translate-y-[-1px]"
                style={{
                  borderColor: "var(--border)",
                  backgroundColor: "var(--surface)",
                  color: "var(--text)",
                }}
              >
                Open tenants
              </Link>
            </div>
          </div>
        </div>

        <aside className="space-y-6">
          <div
            className="rounded-[2rem] border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
          >
            <h2
              className="text-xl font-semibold"
              style={{ color: "var(--text)" }}
            >
              Edit
            </h2>
            <form className="mt-4 space-y-3" onSubmit={handleSubmit}>
              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Organization name
                </span>
                <input
                  value={form.name}
                  onChange={(event) =>
                    setForm((prev) => ({ ...prev, name: event.target.value }))
                  }
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface)",
                    color: "var(--text)",
                  }}
                />
              </label>

              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Legal name
                </span>
                <input
                  value={form.legal_name}
                  onChange={(event) =>
                    setForm((prev) => ({ ...prev, legal_name: event.target.value }))
                  }
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface)",
                    color: "var(--text)",
                  }}
                />
              </label>

              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Industry
                </span>
                <input
                  value={form.industry}
                  onChange={(event) =>
                    setForm((prev) => ({ ...prev, industry: event.target.value }))
                  }
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface)",
                    color: "var(--text)",
                  }}
                />
              </label>

              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Country
                </span>
                <input
                  value={form.country}
                  onChange={(event) =>
                    setForm((prev) => ({ ...prev, country: event.target.value }))
                  }
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface)",
                    color: "var(--text)",
                  }}
                />
              </label>

              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Timezone
                </span>
                <input
                  value={form.timezone}
                  onChange={(event) =>
                    setForm((prev) => ({ ...prev, timezone: event.target.value }))
                  }
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface)",
                    color: "var(--text)",
                  }}
                />
              </label>

              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Billing email
                </span>
                <input
                  value={form.billing_email}
                  onChange={(event) =>
                    setForm((prev) => ({
                      ...prev,
                      billing_email: event.target.value,
                    }))
                  }
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface)",
                    color: "var(--text)",
                  }}
                />
              </label>

              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Status
                </span>
                <select
                  value={form.status}
                  onChange={(event) =>
                    setForm((prev) => ({ ...prev, status: event.target.value }))
                  }
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface)",
                    color: "var(--text)",
                  }}
                >
                  <option value="lead">lead</option>
                  <option value="trial">trial</option>
                  <option value="active">active</option>
                  <option value="suspended">suspended</option>
                  <option value="cancelled">cancelled</option>
                  <option value="archived">archived</option>
                </select>
              </label>

              {saveError ? (
                <p className="text-sm text-red-500">{saveError}</p>
              ) : saveMessage ? (
                <p className="text-sm" style={{ color: "var(--muted)" }}>
                  {saveMessage}
                </p>
              ) : null}

              <button
                type="submit"
                disabled={saving}
                className="inline-flex rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px] disabled:cursor-not-allowed disabled:opacity-60"
                style={{
                  backgroundColor: "var(--accent)",
                  color: "var(--accent-foreground)",
                  boxShadow: "0 16px 32px var(--shadow)",
                }}
              >
                {saving ? "Saving..." : "Save organization"}
              </button>
            </form>
          </div>

          <div
            className="rounded-[2rem] border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
          >
            <h2
              className="text-xl font-semibold"
              style={{ color: "var(--text)" }}
            >
              Back to list
            </h2>
            <Link
              href="/app/organizations"
              className="mt-4 inline-flex rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface)",
                color: "var(--text)",
              }}
            >
              Open organization list
            </Link>
          </div>
        </aside>
      </div>
    </div>
  );
}
