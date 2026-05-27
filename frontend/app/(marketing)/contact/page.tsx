"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingPageCta,
} from "@/components/MarketingPrimitives";
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
            Talk to us
          </p>
          <h1
            className="mt-4 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl"
            style={{ color: "var(--text)" }}
          >
            Start the conversation before rollout complexity becomes a risk.
          </h1>
          <p
            className="mt-5 text-base leading-8"
            style={{ color: "var(--muted)" }}
          >
            Contact us if you are evaluating a pilot, planning implementation
            work, or trying to structure the boundary between your
            customer-facing SaaS layer and the ERP runtime behind it.
          </p>

          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            {[
              [
                "Pilot scope",
                "Share your timeline, team shape, and what the first launch needs to prove.",
              ],
              [
                "Rollout blockers",
                "Tell us where onboarding, tenants, or implementation visibility are breaking down.",
              ],
              [
                "Commercial fit",
                "Use this route if you need help with packaging, pricing, or a guided deployment conversation.",
              ],
            ].map(([title, description]) => (
              <div
                key={title}
                className="rounded-[1.25rem] border border-[color:var(--border)] bg-[color:var(--surface)] p-4"
              >
                <p
                  className="text-sm font-semibold"
                  style={{ color: "var(--text)" }}
                >
                  {title}
                </p>
                <p
                  className="mt-2 text-sm leading-6"
                  style={{ color: "var(--muted)" }}
                >
                  {description}
                </p>
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
            Contact form
          </p>
          <form
            className="mt-6 grid gap-4 md:grid-cols-2"
            onSubmit={handleSubmit}
          >
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
            <label className="block space-y-2 md:col-span-2">
              <span
                className="text-xs font-semibold uppercase tracking-[0.18em]"
                style={{ color: "var(--muted)" }}
              >
                What do you need help with?
              </span>
              <textarea
                name="message"
                rows={6}
                className="marketing-textarea"
                placeholder="Tell us about your timeline, operating model, rollout blockers, or what you want the platform to make easier."
              />
            </label>
            <div className="md:col-span-2">
              <button
                type="submit"
                className="marketing-button marketing-button-primary disabled:cursor-not-allowed disabled:opacity-60"
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
        </MarketingCard>
      </section>

      <section className="grid gap-5 md:grid-cols-2">
        <MarketingCard className="rounded-[1.85rem] p-6" tone="default">
          <h2
            className="text-2xl font-semibold"
            style={{ color: "var(--text)" }}
          >
            Prefer a walkthrough first?
          </h2>
          <p
            className="mt-3 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            Book a demo if you would rather see the product live before
            discussing scope.
          </p>
          <div className="mt-5">
            <MarketingButtonLink href="/demo">Book a demo</MarketingButtonLink>
          </div>
        </MarketingCard>

        <MarketingCard className="rounded-[1.85rem] p-6" tone="muted">
          <h2
            className="text-2xl font-semibold"
            style={{ color: "var(--text)" }}
          >
            Existing client or operator?
          </h2>
          <p
            className="mt-3 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            Sign in if you are returning to the dashboard for tenant,
            organization, or implementation work.
          </p>
          <div className="mt-5">
            <MarketingButtonLink href="/login" variant="secondary">
              Sign in
            </MarketingButtonLink>
          </div>
        </MarketingCard>
      </section>

      <MarketingPageCta />
    </div>
  );
}
