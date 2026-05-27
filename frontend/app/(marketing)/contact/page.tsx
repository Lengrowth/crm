"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import Link from "next/link";
import { sendContact, trackMarketingEvent } from "@/lib/api";

export default function ContactPage() {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setSuccess(null);
    setLoading(true);
    const form = event.currentTarget;
    const formData = new FormData(form);
    const payload = {
      name: String(formData.get("name") ?? ""),
      email: String(formData.get("email") ?? ""),
      message: String(formData.get("message") ?? ""),
    };

    try {
      const resp = await sendContact(payload);
      setSuccess(resp.detail ?? "Message captured");
      trackMarketingEvent({ type: "contact", path: window.location.pathname });
      form.reset();
    } catch (err: any) {
      setError(err?.message ?? "Failed to send contact message");
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
          Contact
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Talk to us about your rollout, pilot, or control-plane requirements.
        </h1>
        <p className="mt-4 text-sm leading-7" style={{ color: "var(--muted)" }}>
          Share your team size, operating model, deployment timeline, or ERP
          migration concerns and we will respond with the right next step.
        </p>

        <form
          className="mt-8 grid gap-4 md:grid-cols-2"
          onSubmit={handleSubmit}
        >
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

          <label className="block space-y-2 md:col-span-2">
            <span
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              What do you need help with?
            </span>
            <textarea
              name="message"
              rows={5}
              className="w-full rounded-xl border px-4 py-3 text-sm outline-none"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
                color: "var(--text)",
              }}
              placeholder="Tell us about your operating model, pilot scope, or rollout blockers."
            />
          </label>

          <div className="md:col-span-2">
            <button
              type="submit"
              className="rounded-full px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px] disabled:opacity-60"
              style={{
                backgroundColor: "var(--accent)",
                color: "var(--accent-foreground)",
                boxShadow: "0 16px 32px var(--shadow)",
              }}
              disabled={loading}
            >
              {loading ? "Sending..." : "Send message"}
            </button>

            {error ? (
              <p className="mt-3 text-sm text-red-500">{error}</p>
            ) : null}
            {success ? (
              <p className="mt-3 text-sm" style={{ color: "var(--muted)" }}>
                {success}
              </p>
            ) : null}
          </div>
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
            Best fit for this conversation
          </h2>
          <ol
            className="mt-4 space-y-3 text-sm leading-6"
            style={{ color: "var(--muted)" }}
          >
            <li>Teams planning a pilot launch or controlled rollout.</li>
            <li>Operators who need visibility before ERPNext goes live.</li>
            <li>
              Implementation-led deployments that need a clean SaaS boundary.
            </li>
          </ol>
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
            Prefer a walkthrough?
          </h2>
          <Link
            href="/demo"
            className="mt-4 inline-flex rounded-full border px-5 py-3 text-sm font-semibold transition hover:translate-y-[-1px]"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface)",
              color: "var(--text)",
            }}
          >
            Request demo
          </Link>
        </div>
      </aside>
    </div>
  );
}
