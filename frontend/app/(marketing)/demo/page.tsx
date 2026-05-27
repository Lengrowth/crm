"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingPageCta,
} from "@/components/MarketingPrimitives";
import { sendDemoRequest, trackMarketingEvent } from "@/lib/api";

const demoExpectations = [
  "A walkthrough of the public product story and the SaaS control surface.",
  "A clear explanation of what lives in the control plane versus the ERP runtime.",
  "A conversation about pilot fit, rollout sequencing, and what the next step should be.",
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
    <div className="space-y-8 sm:space-y-10 lg:space-y-12">
      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <MarketingCard
          className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10"
          tone="accent"
        >
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--muted)" }}
          >
            Book a demo
          </p>
          <h1
            className="mt-4 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl"
            style={{ color: "var(--text)" }}
          >
            See how the control plane makes onboarding, tenants, and rollout
            readiness visible.
          </h1>
          <p
            className="mt-5 text-base leading-8"
            style={{ color: "var(--muted)" }}
          >
            This is a product-led walkthrough for teams evaluating pilots,
            implementation flow, or launch readiness. We will show the SaaS
            control surface clearly and explain the ERPNext runtime boundary
            without hand-waving.
          </p>

          <div className="mt-8 space-y-3">
            {demoExpectations.map((item) => (
              <div
                key={item}
                className="rounded-[1.25rem] border border-[color:var(--border)] bg-[color:var(--surface)] px-4 py-4 text-sm leading-7"
                style={{ color: "var(--text)" }}
              >
                {item}
              </div>
            ))}
          </div>
        </MarketingCard>

        <MarketingCard
          className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10"
          tone="default"
        >
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--muted)" }}
          >
            Demo request form
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
                rows={5}
                className="marketing-textarea"
                placeholder="Examples: drilling workflows, tenant readiness, implementation visibility, launch planning, or product packaging."
              />
            </label>
            <button
              type="submit"
              disabled={loading}
              className="marketing-button marketing-button-primary disabled:cursor-not-allowed disabled:opacity-60"
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
        </MarketingCard>
      </section>

      <section className="grid gap-5 md:grid-cols-3">
        {[
          [
            "Best fit",
            "Teams planning a pilot, guided rollout, or implementation-led evaluation.",
          ],
          [
            "What you will not get",
            "A vague sales pitch. The demo is designed to clarify product boundaries and real rollout posture.",
          ],
          [
            "Already have access?",
            "Sign in if you are returning to the dashboard or reviewing an active workspace.",
          ],
        ].map(([title, description], index) => (
          <MarketingCard
            key={title}
            className="rounded-[1.75rem] p-6"
            tone={index === 1 ? "muted" : "default"}
          >
            <h2
              className="text-xl font-semibold"
              style={{ color: "var(--text)" }}
            >
              {title}
            </h2>
            <p
              className="mt-3 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {description}
            </p>
            {title === "Already have access?" ? (
              <div className="mt-5">
                <MarketingButtonLink href="/login" variant="secondary">
                  Sign in
                </MarketingButtonLink>
              </div>
            ) : null}
          </MarketingCard>
        ))}
      </section>

      <MarketingPageCta />
    </div>
  );
}
