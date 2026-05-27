import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy policy",
  description: "Privacy commitments for the SaaS Control Plane website and pilot application.",
};

export default function PrivacyPage() {
  return (
    <div className="max-w-4xl space-y-8">
      <section>
        <p className="text-xs font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>
          Privacy policy
        </p>
        <h1 className="mt-4 text-4xl font-semibold tracking-tight" style={{ color: "var(--text)" }}>
          Privacy commitments for website visitors, leads, and pilot users.
        </h1>
      </section>

      <div className="space-y-6 text-sm leading-7" style={{ color: "var(--muted)" }}>
        <p>
          We collect only the information needed to respond to demo requests, contact inquiries, pilot onboarding, and
          authenticated product access. This may include your name, email address, organization information, and the
          messages you send through the site.
        </p>
        <p>
          We use this information to operate the website, support pilot and implementation conversations, maintain
          account access, and improve the SaaS control platform. We do not use your information to silently provision a
          live ERPNext environment in this phase of the product.
        </p>
        <p>
          Access to pilot and operational data is limited to authorized operators and service providers supporting the
          platform. We do not intentionally expose customer operational data publicly.
        </p>
        <p>
          If you need your contact information updated or removed, contact us through the website and we will handle the
          request through our support process.
        </p>
      </div>
    </div>
  );
}
