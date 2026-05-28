import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingPageCta,
  MarketingSectionIntro,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Terms of service",
  description:
    "Website and pilot-use terms for LenERP demos, public access, and authenticated workspace usage.",
};

const termPoints = [
  {
    title: "Evaluation and pilot use",
    description:
      "The LenERP website and pilot application are provided for evaluation, onboarding, operational planning, and early customer use. Access may be limited, suspended, or changed as the product matures.",
  },
  {
    title: "Your responsibilities",
    description:
      "You are responsible for using the platform lawfully, protecting your access credentials, and providing accurate information when requesting demos, support, or pilot access.",
  },
  {
    title: "Runtime readiness",
    description:
      "During the current phase, the platform does not promise live ERPNext cutover or production tenant provisioning. Any live integration work remains subject to later readiness and operator approval.",
  },
  {
    title: "Commercial detail",
    description:
      "To the extent permitted by law, the service is provided on an as-available basis during this pilot stage. More detailed commercial and support terms can be defined in separate customer agreements as the product moves toward full launch.",
  },
];

export default function TermsPage() {
  return (
    <div className="space-y-8 sm:space-y-10 lg:space-y-12">
      <MarketingCard
        className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10"
        tone="accent"
      >
        <MarketingSectionIntro
          eyebrow="Terms of service"
          title="Terms for website access, demos, and pilot application use."
          description="These terms reflect the current product stage: launch-oriented, pilot-ready, and explicit about what is available now versus what remains part of a later operational cutover."
        />
      </MarketingCard>

      <div className="grid gap-5 md:grid-cols-2">
        {termPoints.map((item) => (
          <MarketingCard
            key={item.title}
            className="rounded-[1.85rem] p-6"
            tone="default"
            interactive
          >
            <h2
              className="text-2xl font-semibold tracking-[-0.03em]"
              style={{ color: "var(--text)" }}
            >
              {item.title}
            </h2>
            <p
              className="mt-3 text-sm leading-7"
              style={{ color: "var(--muted)" }}
            >
              {item.description}
            </p>
          </MarketingCard>
        ))}
      </div>

      <section className="grid gap-6 lg:grid-cols-[1fr_0.95fr]">
        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="default">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Pilot-stage clarity
          </p>
          <p
            className="mt-4 text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            The product is intended to support demos, onboarding, implementation
            planning, and controlled early use. If you need more specific
            commercial or operational terms, those should be handled through a
            separate agreement.
          </p>
        </MarketingCard>

        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="muted">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Continue the conversation
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <MarketingButtonLink href="/contact">
              Talk to us
            </MarketingButtonLink>
            <MarketingButtonLink href="/pricing" variant="secondary">
              View pricing
            </MarketingButtonLink>
          </div>
        </MarketingCard>
      </section>

      <MarketingPageCta />
    </div>
  );
}
