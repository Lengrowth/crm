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
import { sendContact, trackMarketingEvent } from "@/lib/api";

const reasons = [
  {
    icon: "flag" as const,
    title: "Getting started",
    description:
      "Tell us about your business, team size, and what you want the platform to do for you.",
  },
  {
    icon: "eye" as const,
    title: "Specific requirements",
    description:
      "Share what your current software isn't doing, and we'll show you how LenERP addresses it.",
  },
  {
    icon: "building" as const,
    title: "Pricing and implementation",
    description:
      "Get a clear picture of what an engagement looks like — cost, timeline, and what’s included.",
  },
];

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
      setSuccess(resp.detail ?? "Message sent");
      trackMarketingEvent({ type: "contact", path: window.location.pathname });
      form.reset();
    } catch (err: any) {
      setError(err?.message ?? "Failed to send message");
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
          Talk to us
        </p>
        <h1
          className="marketing-reveal mt-4 text-5xl font-semibold tracking-[-0.05em] sm:text-6xl"
          style={{ color: "var(--text)", animationDelay: "60ms" }}
        >
          Let’s talk about your business.
        </h1>
        <p
          className="marketing-reveal mt-5 max-w-lg text-lg leading-8"
          style={{ color: "var(--muted)", animationDelay: "120ms" }}
        >
          Whether you’re evaluating a CRM & ERP for the first time or
          replacing an existing system, we’re happy to walk through how
          LenERP fits your operations.
        </p>
      </div>

      {/* Reasons + Form */}
      <ScrollReveal>
      <section className="grid gap-12 lg:grid-cols-2 lg:items-start">
        {/* Reasons */}
        <div className="space-y-8">
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            Good reasons to get in touch
          </p>
          {reasons.map((item) => (
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
            <p className="text-sm leading-6" style={{ color: "var(--muted)" }}>
              Prefer to see the product first?
            </p>
            <div className="mt-3">
              <MarketingButtonLink href="/demo" variant="secondary">
                Book a demo instead
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
            Send a message
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
                rows={5}
                className="marketing-textarea"
                placeholder="Your industry, current software, what you’re looking to improve, or any questions about the platform…"
              />
            </label>
            <div className="md:col-span-2">
              <button
                type="submit"
                className="marketing-button marketing-button-primary disabled:cursor-not-allowed disabled:opacity-60"
                disabled={loading}
              >
                {loading ? "Sending…" : "Send message"}
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
      </ScrollReveal>

      <MarketingPageCta />
    </div>
  );
}
