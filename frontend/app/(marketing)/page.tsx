import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingPageCta,
  MarketingSectionIntro,
  MarketingStat,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Operational ERP rollout control for implementation-led teams",
  description:
    "LenQuant gives operations-heavy teams a premium SaaS control plane for onboarding, tenant readiness, module packaging, and rollout visibility around ERPNext-backed delivery.",
};

const tensionPoints = [
  {
    title: "Custom delivery gets messy fast",
    description:
      "Sales, implementation, provisioning, and launch work often live across inboxes, spreadsheets, and ad hoc notes instead of one controlled workflow.",
  },
  {
    title: "ERP runtime work should not carry the whole customer journey",
    description:
      "The product, the rollout process, and tenant administration need their own SaaS layer instead of being forced directly into the runtime.",
  },
  {
    title: "Pilots fail when readiness is invisible",
    description:
      "Without a visible path for onboarding, modules, domains, and launch signoff, teams lose confidence before go-live even begins.",
  },
];

const workflowSteps = [
  {
    step: "01",
    title: "Qualify the account",
    description:
      "Create the organization, define the commercial package, and keep the customer relationship inside the SaaS product surface.",
  },
  {
    step: "02",
    title: "Prepare the rollout",
    description:
      "Track modules, tenant metadata, implementation work, and operational handoffs before runtime cutover is even considered.",
  },
  {
    step: "03",
    title: "Coordinate readiness",
    description:
      "Keep operators, implementation leads, and support teams aligned on what is complete, what is blocked, and what launches next.",
  },
  {
    step: "04",
    title: "Cut over deliberately",
    description:
      "Connect to the ERPNext runtime through an explicit integration path instead of collapsing the boundary too early.",
  },
];

const modulePreview = [
  {
    title: "CRM and commercial control",
    description:
      "Package the offer, manage the customer relationship, and keep entitlement decisions visible from the SaaS layer first.",
  },
  {
    title: "Implementation visibility",
    description:
      "Track onboarding milestones, rollout ownership, and launch readiness without hiding progress in back-channel conversations.",
  },
  {
    title: "Tenant and domain operations",
    description:
      "Manage environments, tenant records, provisioning signals, and white-label preparation from one operational control room.",
  },
  {
    title: "Operational module packaging",
    description:
      "Present vertical-fit modules like drilling, field ops, inventory, and reporting with a repeatable product structure.",
  },
];

const trustSignals = [
  "Clear SaaS vs ERP runtime boundary",
  "Pilot-ready onboarding and launch workflow",
  "Implementation-led product positioning",
  "Mobile-friendly, operator-friendly public experience",
];

export default function HomePage() {
  return (
    <div className="space-y-8 sm:space-y-10 lg:space-y-12">
      <MarketingCard
        className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10 lg:px-12 lg:py-12"
        tone="accent"
      >
        <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-end">
          <div>
            <div className="flex flex-wrap gap-3">
              <span className="marketing-chip rounded-full px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em]">
                Premium SaaS experience
              </span>
              <span className="marketing-chip rounded-full px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em]">
                ERPNext-aware rollout control
              </span>
            </div>

            <MarketingSectionIntro
              eyebrow="LenQuant control plane"
              title="Operational ERP rollouts need a control layer, not more chaos."
              description="LenQuant gives product owners, operators, and implementation teams a launch-ready SaaS surface for onboarding, tenant readiness, module packaging, and rollout visibility — while ERPNext stays the runtime behind a deliberate boundary."
              className="mt-7"
            />

            <div className="mt-8 flex flex-wrap gap-3">
              <MarketingButtonLink href="/demo">
                Book a demo
              </MarketingButtonLink>
              <MarketingButtonLink href="/contact" variant="secondary">
                Talk to us
              </MarketingButtonLink>
              <MarketingButtonLink href="/login" variant="ghost">
                Sign in
              </MarketingButtonLink>
            </div>
          </div>

          <div className="grid gap-4">
            <MarketingCard className="rounded-[1.75rem] p-6" tone="default">
              <p
                className="text-xs font-semibold uppercase tracking-[0.24em]"
                style={{ color: "var(--muted)" }}
              >
                Product boundary
              </p>
              <div className="mt-5 grid gap-4 sm:grid-cols-2">
                <div className="rounded-[1.25rem] border border-[color:var(--border)] bg-[color:var(--surface-strong)] p-4">
                  <p
                    className="text-sm font-semibold"
                    style={{ color: "var(--text)" }}
                  >
                    SaaS control plane
                  </p>
                  <p
                    className="mt-2 text-sm leading-6"
                    style={{ color: "var(--muted)" }}
                  >
                    Accounts, tenants, modules, implementation, launch
                    visibility.
                  </p>
                </div>
                <div className="rounded-[1.25rem] border border-[color:var(--border)] bg-[color:var(--surface-strong)] p-4">
                  <p
                    className="text-sm font-semibold"
                    style={{ color: "var(--text)" }}
                  >
                    ERPNext runtime
                  </p>
                  <p
                    className="mt-2 text-sm leading-6"
                    style={{ color: "var(--muted)" }}
                  >
                    Operational tenant execution after a controlled integration
                    cutover.
                  </p>
                </div>
              </div>
            </MarketingCard>

            <div className="grid gap-4 sm:grid-cols-3">
              <MarketingStat
                value="1"
                label="Visible control surface"
                description="One place for commercial, implementation, and launch coordination."
              />
              <MarketingStat
                value="4"
                label="Critical rollout layers"
                description="Organizations, tenants, modules, and implementation readiness."
              />
              <MarketingStat
                value="0"
                label="Silent runtime coupling"
                description="The product boundary stays explicit until cutover is ready."
              />
            </div>
          </div>
        </div>
      </MarketingCard>

      <div className="grid gap-5 lg:grid-cols-3">
        {tensionPoints.map((item) => (
          <MarketingCard
            key={item.title}
            className="rounded-[1.75rem] p-6"
            tone="muted"
          >
            <p
              className="text-lg font-semibold"
              style={{ color: "var(--text)" }}
            >
              {item.title}
            </p>
            <p
              className="mt-3 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {item.description}
            </p>
          </MarketingCard>
        ))}
      </div>

      <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Why the model works
          </p>
          <h2
            className="mt-4 text-3xl font-semibold tracking-[-0.04em]"
            style={{ color: "var(--text)" }}
          >
            Separate the product layer from the runtime, and the rollout gets
            easier to trust.
          </h2>
          <p
            className="mt-4 text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            LenQuant is not trying to hide ERPNext. It is putting the
            customer-facing product, implementation workflow, and launch
            coordination in the right place so the runtime can stay stable and
            deliberate.
          </p>
          <ul
            className="mt-6 space-y-3 text-sm leading-7"
            style={{ color: "var(--muted)" }}
          >
            <li>
              • Better onboarding visibility for clients and internal teams.
            </li>
            <li>
              • Cleaner entitlement and tenant operations before runtime work
              starts.
            </li>
            <li>
              • Stronger commercial presentation during demos, pilots, and early
              rollout conversations.
            </li>
          </ul>
        </MarketingCard>

        <div className="grid gap-4 sm:grid-cols-2">
          {workflowSteps.map((item) => (
            <MarketingCard
              key={item.step}
              className="rounded-[1.75rem] p-6"
              tone="default"
            >
              <p
                className="text-xs font-semibold uppercase tracking-[0.28em]"
                style={{ color: "var(--muted)" }}
              >
                Step {item.step}
              </p>
              <h3
                className="mt-3 text-xl font-semibold"
                style={{ color: "var(--text)" }}
              >
                {item.title}
              </h3>
              <p
                className="mt-3 text-sm leading-7"
                style={{ color: "var(--muted)" }}
              >
                {item.description}
              </p>
            </MarketingCard>
          ))}
        </div>
      </section>

      <section className="space-y-6">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <p
              className="text-xs font-semibold uppercase tracking-[0.24em]"
              style={{ color: "var(--muted)" }}
            >
              Capability preview
            </p>
            <h2
              className="mt-3 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
              style={{ color: "var(--text)" }}
            >
              Product modules that support repeatable delivery instead of custom
              chaos.
            </h2>
          </div>
          <MarketingButtonLink href="/modules" variant="secondary">
            View modules
          </MarketingButtonLink>
        </div>

        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          {modulePreview.map((item) => (
            <MarketingCard
              key={item.title}
              className="rounded-[1.75rem] p-6"
              tone="default"
            >
              <h3
                className="text-xl font-semibold"
                style={{ color: "var(--text)" }}
              >
                {item.title}
              </h3>
              <p
                className="mt-3 text-sm leading-7"
                style={{ color: "var(--muted)" }}
              >
                {item.description}
              </p>
            </MarketingCard>
          ))}
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Industry fit
          </p>
          <h2
            className="mt-4 text-3xl font-semibold tracking-[-0.04em]"
            style={{ color: "var(--text)" }}
          >
            Built to feel credible for operations-heavy businesses from the
            first conversation.
          </h2>
          <p
            className="mt-4 text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            The first flagship vertical is drilling, but the control model is
            intentionally reusable across field service, fleet, inventory-led
            operations, and implementation-heavy deployments.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <MarketingButtonLink href="/industries">
              Explore industries
            </MarketingButtonLink>
            <MarketingButtonLink href="/drilling" variant="secondary">
              See drilling fit
            </MarketingButtonLink>
          </div>
        </MarketingCard>

        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="muted">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Trust and readiness
          </p>
          <ul className="mt-5 space-y-4">
            {trustSignals.map((item) => (
              <li
                key={item}
                className="rounded-[1.25rem] border border-[color:var(--border)] bg-[color:var(--surface)] px-4 py-4 text-sm font-medium"
                style={{ color: "var(--text)" }}
              >
                {item}
              </li>
            ))}
          </ul>
        </MarketingCard>
      </section>

      <MarketingPageCta />
    </div>
  );
}
