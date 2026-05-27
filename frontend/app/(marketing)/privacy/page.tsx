import type { Metadata } from "next";
import {
  MarketingButtonLink,
  MarketingCard,
  MarketingPageCta,
  MarketingSectionIntro,
} from "@/components/MarketingPrimitives";

export const metadata: Metadata = {
  title: "Privacy policy",
  description:
    "Privacy commitments for LenQuant website visitors, demo requests, pilot users, and authenticated workspace access.",
};

const privacyPoints = [
  {
    title: "What we collect",
    description:
      "We collect the information needed to respond to demo requests, contact inquiries, pilot onboarding, and authenticated product access. That may include your name, email address, organization information, and the messages you send through the site.",
  },
  {
    title: "How we use it",
    description:
      "We use this information to operate the website, support pilot and implementation conversations, maintain account access, and improve the LenQuant product experience.",
  },
  {
    title: "What we do not do silently",
    description:
      "We do not use your information to silently provision a live ERPNext environment in this phase of the product. Runtime cutover remains a deliberate operational step.",
  },
  {
    title: "Access and handling",
    description:
      "Access to pilot and operational data is limited to authorized operators and service providers supporting the platform. We do not intentionally expose customer operational data publicly.",
  },
];

export default function PrivacyPage() {
  return (
    <div className="space-y-8 sm:space-y-10 lg:space-y-12">
      <MarketingCard
        className="rounded-[2.25rem] px-7 py-8 sm:px-10 sm:py-10"
        tone="accent"
      >
        <MarketingSectionIntro
          eyebrow="Privacy policy"
          title="Privacy commitments for website visitors, leads, and pilot users."
          description="LenQuant keeps the public website, contact flows, and pilot access aligned with the same principle as the product itself: collect what is necessary, keep access controlled, and avoid blurring the runtime boundary."
        />
      </MarketingCard>

      <div className="grid gap-5 md:grid-cols-2">
        {privacyPoints.map((item) => (
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
            Requests and updates
          </p>
          <p
            className="mt-4 text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            If you need your contact information updated or removed, contact us
            through the website and we will handle the request through our
            support process.
          </p>
        </MarketingCard>

        <MarketingCard className="rounded-[2rem] p-7 sm:p-8" tone="muted">
          <p
            className="text-xs font-semibold uppercase tracking-[0.24em]"
            style={{ color: "var(--muted)" }}
          >
            Need help now?
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <MarketingButtonLink href="/contact">
              Talk to us
            </MarketingButtonLink>
            <MarketingButtonLink href="/demo" variant="secondary">
              Book a demo
            </MarketingButtonLink>
          </div>
        </MarketingCard>
      </section>

      <MarketingPageCta />
    </div>
  );
}
