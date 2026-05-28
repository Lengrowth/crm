"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingIcon,
  MarketingPageCta,
  ScrollReveal,
} from "@/components/MarketingPrimitives";
import { sendDemoRequest, trackMarketingEvent } from "@/lib/api";

const expectations = [
  {
    icon: "grid" as const,
    title: "The full platform",
    description:
      "A live walkthrough of CRM, field operations, drilling workflows, inventory, and finance — all connected.",
  },
  {
    icon: "chart" as const,
    title: "Your industry, your workflows",
    description:
      "We focus the demo on the modules and workflows most relevant to your business and team.",
  },
  {
    icon: "spark" as const,
    title: "Next steps",
    description:
      "A clear conversation about what getting started looks like: scope, timeline, and implementation.",
  },
];

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
      form.reset();
    } catch (err: any) {
      setError(err?.message ?? "Failed to send demo request");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-16 lg:space-y-24">
      {/* Hero */}
      <div className="max-w-2xl">
        <p
          className="marketing-reveal text-xs font-semibold uppercase tracking-[0.28em]"
          style={{ color: "var(--accent)" }}
        >
          Book a demo
        </p>
        <h1
          className="marketing-reveal mt-4 text-5xl font-semibold tracking-[-0.05em] sm:text-6xl"
          style={{ color: "var(--text)", animationDelay: "60ms" }}
        >
          See the platform built for your business.
        </h1>
        <p
          className="marketing-reveal mt-5 max-w-lg text-lg leading-8"
          style={{ color: "var(--muted)", animationDelay: "120ms" }}
        >
          A live product walkthrough tailored to your industry. We show
          you the real platform — CRM, field ops, drilling, inventory, and
          finance — and talk through what implementation looks like.
        </p>
      </div>

      {/* Main content: expectations + form */}
      <ScrollReveal>
      <section className="grid gap-12 lg:grid-cols-2 lg:items-start">
        {/* What to expect */}
        <div className="space-y-8">
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            What to expect
          </p>
          {expectations.map((item) => (
            <div key={item.title} className="flex items-start gap-4">
              <span
                className="mt-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[color:var(--border)] text-[color:var(--text)]"
                style={{ background: "var(--surface)" }}
              >
                <MarketingIcon icon={item.icon} className="h-5 w-5" />
              </span>
              <div>
                <h3 className="font-semibold" style={{ color: "var(--text)" }}>
                  {item.title}
                </h3>
                <p
                  className="mt-1 text-sm leading-6"
                  style={{ color: "var(--muted)" }}
                >
                  {item.description}
                </p>
              </div>
            </div>
          ))}

          <div className="pt-4">
            <p
              className="text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--accent)" }}
            >
              Already have access?
            </p>
            <p
              className="mt-2 text-sm leading-6"
              style={{ color: "var(--muted)" }}
            >
              Sign in to return to the dashboard or review an active workspace.
            </p>
            <div className="mt-4">
              <MarketingButtonLink href="/login" variant="secondary">
                Sign in
              </MarketingButtonLink>
            </div>
          </div>
        </div>

        {/* Form */}
        <MarketingCard
          className="rounded-[2rem] px-7 py-8 sm:px-8 sm:py-9"
          tone="default"
        >
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            Request a demo
          </p>
          <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
            <label className="block space-y-2">
              <span
                className="text-xs font-semibold uppercase tracking-[0.18em]"
                style={{ color: "var(--muted)" }}
              >
                Name
              </span>
              <input name="name" required className="marketing-input" />
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
                className="marketing-input"
              />
            </label>
            <label className="block space-y-2">
              <span
                className="text-xs font-semibold uppercase tracking-[0.18em]"
                style={{ color: "var(--muted)" }}
              >
                What should we focus on?
              </span>
              <textarea
                name="message"
                rows={4}
                className="marketing-textarea"
                placeholder="Drilling workflows, field operations, what you want to replace, or anything else you want us to focus on…"
              />
            </label>
            <button
              type="submit"
              disabled={loading}
              className="marketing-button marketing-button-primary disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Sending…" : "Request demo"}
            </button>

            {error ? <p className="text-sm text-red-500">{error}</p> : null}
            {submitted ? (
              <p className="text-sm" style={{ color: "var(--muted)" }}>
                Request received — we&apos;ll follow up with next steps.
              </p>
            ) : null}
          </form>
        </MarketingCard>
      </section>
      </ScrollReveal>

      <MarketingPageCta />
    </div>
  );
}
