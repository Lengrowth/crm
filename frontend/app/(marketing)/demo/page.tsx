"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import Link from "next/link";

import { sendDemoRequest, trackMarketingEvent } from "@/lib/api";

export default function DemoPage() {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setLoading(true);

    const form = event.currentTarget;
    const formData = new FormData(form);
    const payload = {
      name: String(formData.get("name") ?? ""),
      email: String(formData.get("email") ?? ""),
      message: String(formData.get("message") ?? ""),
    };

    try {
      await sendDemoRequest(payload);
      setSubmitted(true);
      trackMarketingEvent({
        type: "demo_request",
        path: window.location.pathname,
      });
    } catch (err: any) {
      setError(err?.message ?? "Failed to send demo request");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[1fr_0.9fr]">
      <section
        className="rounded-[2rem] border p-8 lg:p-10"
        style={{
          borderColor: "var(--border)",
          backgroundColor: "var(--surface)",
          boxShadow: "0 24px 60px var(--shadow)",
        }}
      >
        <p
          className="text-xs font-semibold uppercase tracking-[0.24em]"
          style={{ color: "var(--muted)" }}
        >
          Demo request
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          See how the control plane handles onboarding, tenant readiness, and
          rollout visibility.
        </h1>
        <p className="mt-4 text-sm leading-7" style={{ color: "var(--muted)" }}>
          Request a walkthrough of the SaaS control layer, including
          organizations, tenants, implementation views, and the mock-safe
          ERPNext boundary used for local demos.
        </p>

        <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
          <label className="block space-y-2">
            <span
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              Name
            </span>
            <input
              name="name"
              required
              className="w-full rounded-xl border px-4 py-3 text-sm outline-none"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
            />
          </label>
          <label className="block space-y-2">
            <span
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              Work email
            </span>
            <input
              name="email"
              required
              type="email"
              className="w-full rounded-xl border px-4 py-3 text-sm outline-none"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
            />
          </label>
          <label className="block space-y-2">
            <span
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              What should the demo focus on?
            </span>
            <textarea
              name="message"
              rows={4}
              className="w-full rounded-xl border px-4 py-3 text-sm outline-none"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
              placeholder="Examples: pilot onboarding, tenant mapping, implementation tracking, or launch operations."
            />
          </label>
          <button
            type="submit"
            disabled={loading}
            className="rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px] disabled:opacity-60"
            style={{
              backgroundColor: "var(--accent)",
              color: "var(--accent-foreground)",
              boxShadow: "0 16px 32px var(--shadow)",
            }}
          >
            {loading ? "Sending..." : "Request demo"}
          </button>

          {error ? <p className="text-sm text-red-500">{error}</p> : null}

          {submitted ? (
            <p className="text-sm" style={{ color: "var(--muted)" }}>
              Demo request captured. We&apos;ll follow up with next steps.
            </p>
          ) : null}
        </form>
      </section>

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
            What the demo covers
          </h2>
          <p
            className="mt-3 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            The demo shows the product boundary clearly: the SaaS layer owns
            access, tenants, implementation, and rollout coordination, while
            ERPNext remains an external runtime that has not been cut over yet.
          </p>
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
            Need direct access?
          </h2>
          <Link
            href="/login"
            className="mt-4 inline-flex rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface)",
              color: "var(--text)",
            }}
          >
            Sign in
          </Link>
        </div>
      </aside>
    </div>
  );
}
