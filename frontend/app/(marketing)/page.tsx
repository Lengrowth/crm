import type { Metadata } from "next";
import {
  MarketingBackdrop,
  MarketingButtonLink,
  MarketingCard,
  MarketingIcon,
  MarketingIconBadge,
  MarketingPageCta,
  MarketingSectionIntro,
  MarketingStat,
  type MarketingIconName,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Operational ERP rollout control for implementation-led teams",
  description:
    "LenQuant gives operations-heavy teams a premium SaaS control plane for onboarding, tenant readiness, module packaging, and rollout visibility around ERPNext-backed delivery.",
};

const tensionPoints = [
  {
    icon: "spark",
    title: "Delivery gets noisy fast",
    description:
      "Sales, implementation, and launch work spread across inboxes and spreadsheets instead of one visible workflow.",
  },
  {
    icon: "shield",
    title: "The product boundary should stay clear",
    description:
      "The public site should explain the SaaS layer first and keep the runtime relationship deliberate.",
  },
  {
    icon: "chart",
    title: "Readiness has to be visible",
    description:
      "Teams should see onboarding, module fit, and launch status before go-live pressure shows up.",
  },
];

const workflowSteps = [
  {
    step: "01",
    icon: "grid",
    title: "Map the account",
    description:
      "Set the organization, package, and commercial story in the SaaS control plane first.",
  },
  {
    step: "02",
    icon: "spark",
    title: "Shape the rollout",
    description:
      "Track modules, readiness, and implementation ownership before any runtime cutover begins.",
  },
  {
    step: "03",
    icon: "shield",
    title: "Coordinate the boundary",
    description:
      "Keep operators, delivery teams, and customers aligned on what belongs in the front door and what stays behind it.",
  },
  {
    step: "04",
    icon: "arrow",
    title: "Cut over deliberately",
    description:
      "Move to runtime only when the rollout is ready, visible, and approved.",
  },
];

const capabilityHighlights = [
  {
    icon: "grid",
    title: "Product packaging",
    description:
      "Shape CRM, modules, and rollout offer structure from one public surface.",
  },
  {
    icon: "spark",
    title: "Implementation visibility",
    description:
      "Show the current state of onboarding and launch work without clutter.",
  },
  {
    icon: "chart",
    title: "Operational signal",
    description:
      "Surface the status, pacing, and readiness story in a way customers can scan quickly.",
  },
  {
    icon: "shield",
    title: "Controlled cutover",
    description:
      "Keep the runtime boundary explicit so the product stays credible during launch.",
  },
];

const industrySignals = [
  {
    icon: "dot",
    title: "Drilling first",
    description:
      "A flagship vertical that proves the product can handle field reality and launch discipline.",
  },
  {
    icon: "grid",
    title: "Field operations next",
    description:
      "Extend the same model to crews, dispatch, and execution-heavy workflows.",
  },
  {
    icon: "chart",
    title: "Inventory and assets",
    description:
      "Keep materials, maintenance, and rollout readiness in a coherent product story.",
  },
];

const trustSignals = [
  "Clear SaaS control plane story",
  "Icon-led public experience",
  "Compact, premium navigation",
  "Zinc-based dark mode surfaces",
];

export default function HomePage() {
  return (
    <div className="space-y-10 lg:space-y-14">
      <MarketingCard
        className="relative overflow-hidden rounded-[2.5rem] px-7 py-8 sm:px-10 sm:py-10 lg:px-12 lg:py-12"
        tone="accent"
      >
        <MarketingBackdrop />
        <div className="relative grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
          <div className="max-w-2xl">
            <div className="flex flex-wrap gap-3">
              <MarketingIconBadge icon="spark" label="Startup-like website" />
              <MarketingIconBadge icon="shield" label="Clear product boundary" />
              <MarketingIconBadge icon="grid" label="Zinc dark mode" />
            </div>

            <p
              className="mt-7 text-xs font-semibold uppercase tracking-[0.28em]"
              style={{ color: "var(--muted)" }}
            >
              LenQuant control plane
            </p>
            <h1
              className="mt-4 max-w-3xl text-5xl font-semibold tracking-[-0.06em] sm:text-6xl lg:text-7xl"
              style={{ color: "var(--text)" }}
            >
              Control the rollout before it turns into operational noise.
            </h1>
            <p
              className="mt-6 max-w-2xl text-base leading-8 sm:text-lg"
              style={{ color: "var(--muted)" }}
            >
              LenQuant gives ops-heavy teams a premium SaaS front door for
              onboarding, tenant readiness, module packaging, and launch
              coordination. The runtime stays behind a deliberate boundary.
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <MarketingButtonLink href="/demo">Book a demo</MarketingButtonLink>
              <MarketingButtonLink href="/contact" variant="secondary">
                Talk to us
              </MarketingButtonLink>
              <MarketingButtonLink href="/login" variant="ghost">
                Sign in
              </MarketingButtonLink>
            </div>

            <div className="mt-8 grid gap-3 sm:grid-cols-3">
              {trustSignals.map((item) => (
                <div
                  key={item}
                  className="rounded-[1.25rem] border border-[color:var(--border)] bg-[color:var(--surface-overlay)] px-4 py-4"
                >
                  <div className="flex items-center gap-3">
                    <span className="flex h-9 w-9 items-center justify-center rounded-full border border-[color:var(--border)] bg-[color:var(--surface-strong)] text-[color:var(--text)]">
                      <MarketingIcon icon="dot" className="h-4 w-4" />
                    </span>
                    <p className="text-sm font-semibold leading-6" style={{ color: "var(--text)" }}>
                      {item}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="grid gap-4">
            <MarketingCard className="rounded-[1.9rem] p-6" tone="default">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p
                    className="text-xs font-semibold uppercase tracking-[0.24em]"
                    style={{ color: "var(--muted)" }}
                  >
                    Public surface
                  </p>
                  <h2
                    className="mt-3 text-2xl font-semibold tracking-[-0.04em]"
                    style={{ color: "var(--text)" }}
                  >
                    One place to explain the product, the rollout, and the next step.
                  </h2>
                </div>
                <span className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[color:var(--border)] bg-[color:var(--surface-strong)] text-[color:var(--text)]">
                  <MarketingIcon icon="grid" className="h-6 w-6" />
                </span>
              </div>

              <div className="mt-5 grid gap-3 sm:grid-cols-2">
                <div className="rounded-[1.35rem] border border-[color:var(--border)] bg-[color:var(--surface-strong)] p-4">
                  <p className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                    SaaS control plane
                  </p>
                  <p className="mt-2 text-sm leading-6" style={{ color: "var(--muted)" }}>
                    Accounts, tenants, modules, implementation, and launch visibility.
                  </p>
                </div>
                <div className="rounded-[1.35rem] border border-[color:var(--border)] bg-[color:var(--surface-strong)] p-4">
                  <p className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                    Runtime boundary
                  </p>
                  <p className="mt-2 text-sm leading-6" style={{ color: "var(--muted)" }}>
                    Operational execution stays explicit until cutover is ready.
                  </p>
                </div>
              </div>
            </MarketingCard>

            <div className="grid gap-4 sm:grid-cols-2">
              <MarketingStat
                value="01"
                label="Primary front door"
                description="Homepage, pricing, demo, and contact all follow one design system."
              />
              <MarketingStat
                value="04"
                label="Core rollout layers"
                description="Organization, tenant, module, and launch readiness are visible."
              />
            </div>
          </div>
        </div>
      </MarketingCard>

      <section className="grid gap-6 lg:grid-cols-[0.88fr_1.12fr] lg:items-start">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
          <MarketingSectionIntro
            eyebrow="Why this matters"
            title="The site should feel designed, not assembled."
            description="Public pages need stronger hierarchy, lighter copy, and a more confident lead-in so the product feels credible before a sales conversation starts."
          />
          <div className="mt-6 flex flex-wrap gap-3">
            <MarketingIconBadge icon="spark" label="More breathing room" />
            <MarketingIconBadge icon="chart" label="Clear primary CTA" />
          </div>
        </MarketingCard>

        <div className="space-y-4">
          {tensionPoints.map((item) => (
            <MarketingCard
              key={item.title}
              className="rounded-[1.75rem] p-5 sm:p-6"
              tone="muted"
              interactive
            >
              <div className="flex items-start gap-4">
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-[color:var(--border)] bg-[color:var(--surface-strong)] text-[color:var(--text)]">
                  <MarketingIcon icon={item.icon as MarketingIconName} className="h-5 w-5" />
                </span>
                <div>
                  <h2
                    className="text-lg font-semibold tracking-[-0.03em]"
                    style={{ color: "var(--text)" }}
                  >
                    {item.title}
                  </h2>
                  <p
                    className="mt-2 text-sm leading-7"
                    style={{ color: "var(--muted)" }}
                  >
                    {item.description}
                  </p>
                </div>
              </div>
            </MarketingCard>
          ))}
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[0.92fr_1.08fr] lg:items-start">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="accent">
          <MarketingSectionIntro
            eyebrow="How it works"
            title="A simple operating sequence that reads quickly."
            description="Each step gives visitors a clearer sense of what happens first, what is controlled in the SaaS layer, and when runtime cutover is allowed."
          />
          <div className="mt-6 flex flex-wrap gap-3">
            <MarketingButtonLink href="/modules">View modules</MarketingButtonLink>
            <MarketingButtonLink href="/industries" variant="secondary">
              Explore industries
            </MarketingButtonLink>
          </div>
        </MarketingCard>

        <div className="space-y-4">
          {workflowSteps.map((item) => (
            <MarketingCard
              key={item.step}
              className="rounded-[1.75rem] p-5 sm:p-6"
              tone="default"
            >
              <div className="flex items-start gap-4">
                <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-[color:var(--border)] bg-[color:var(--surface-strong)] text-[color:var(--text)]">
                  <MarketingIcon icon={item.icon as MarketingIconName} className="h-5 w-5" />
                </span>
                <div className="min-w-0">
                  <p
                    className="text-xs font-semibold uppercase tracking-[0.24em]"
                    style={{ color: "var(--muted)" }}
                  >
                    Step {item.step}
                  </p>
                  <h3
                    className="mt-2 text-xl font-semibold tracking-[-0.03em]"
                    style={{ color: "var(--text)" }}
                  >
                    {item.title}
                  </h3>
                  <p
                    className="mt-2 text-sm leading-7"
                    style={{ color: "var(--muted)" }}
                  >
                    {item.description}
                  </p>
                </div>
              </div>
            </MarketingCard>
          ))}
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[1fr_0.95fr] lg:items-start">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
          <MarketingSectionIntro
            eyebrow="Capability preview"
            title="The product story becomes easier to trust when the sections stop looking identical."
            description="This page uses a mix of cards, split layouts, timeline rows, and proof bands so the site feels intentional instead of templated."
          />

          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            {capabilityHighlights.map((item) => (
              <div
                key={item.title}
                className="rounded-[1.4rem] border border-[color:var(--border)] bg-[color:var(--surface-strong)] p-5"
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-10 w-10 items-center justify-center rounded-xl border border-[color:var(--border)] bg-[color:var(--surface)] text-[color:var(--text)]">
                    <MarketingIcon icon={item.icon as MarketingIconName} className="h-4 w-4" />
                  </span>
                  <h3 className="text-base font-semibold" style={{ color: "var(--text)" }}>
                    {item.title}
                  </h3>
                </div>
                <p className="mt-3 text-sm leading-7" style={{ color: "var(--muted)" }}>
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        </MarketingCard>

        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="muted">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Trust signals
          </p>
          <div className="mt-5 space-y-4">
            {trustSignals.map((item) => (
              <div
                key={item}
                className="flex items-center gap-3 rounded-[1.25rem] border border-[color:var(--border)] bg-[color:var(--surface)] px-4 py-4"
              >
                <span className="flex h-10 w-10 items-center justify-center rounded-xl border border-[color:var(--border)] bg-[color:var(--surface-strong)] text-[color:var(--text)]">
                  <MarketingIcon icon="shield" className="h-4 w-4" />
                </span>
                <p className="text-sm font-medium" style={{ color: "var(--text)" }}>
                  {item}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-6 flex flex-wrap gap-3">
            <MarketingIconBadge icon="dot" label="Mobile-friendly" />
            <MarketingIconBadge icon="dot" label="Premium pacing" />
            <MarketingIconBadge icon="dot" label="Modern CTA flow" />
          </div>
        </MarketingCard>
      </section>

      <section className="grid gap-6 lg:grid-cols-[0.96fr_1.04fr] lg:items-start">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="accent">
          <MarketingSectionIntro
            eyebrow="Industry fit"
            title="Drilling leads because it makes the product feel specific instead of generic."
            description="The same control model can extend into adjacent operations-heavy work once the flagship vertical proves the story."
          />
          <div className="mt-6 flex flex-wrap gap-3">
            <MarketingButtonLink href="/drilling">See drilling</MarketingButtonLink>
            <MarketingButtonLink href="/demo" variant="secondary">
              Book an industry demo
            </MarketingButtonLink>
          </div>
        </MarketingCard>

        <div className="space-y-4">
          {industrySignals.map((item) => (
            <MarketingCard
              key={item.title}
              className="rounded-[1.75rem] p-5 sm:p-6"
              tone="default"
            >
              <div className="flex items-start gap-4">
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-[color:var(--border)] bg-[color:var(--surface-strong)] text-[color:var(--text)]">
                  <MarketingIcon icon={item.icon as MarketingIconName} className="h-5 w-5" />
                </span>
                <div>
                  <h3
                    className="text-lg font-semibold tracking-[-0.03em]"
                    style={{ color: "var(--text)" }}
                  >
                    {item.title}
                  </h3>
                  <p
                    className="mt-2 text-sm leading-7"
                    style={{ color: "var(--muted)" }}
                  >
                    {item.description}
                  </p>
                </div>
              </div>
            </MarketingCard>
          ))}
        </div>
      </section>

      <MarketingPageCta />
    </div>
  );
}
