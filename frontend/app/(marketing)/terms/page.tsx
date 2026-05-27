import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Terms of service",
  description: "Website and pilot-use terms for the SaaS Control Plane.",
};

export default function TermsPage() {
  return (
    <div className="max-w-4xl space-y-8">
      <section>
        <p className="text-xs font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>
          Terms of service
        </p>
        <h1 className="mt-4 text-4xl font-semibold tracking-tight" style={{ color: "var(--text)" }}>
          Terms for website access, demos, and pilot application use.
        </h1>
      </section>

      <div className="space-y-6 text-sm leading-7" style={{ color: "var(--muted)" }}>
        <p>
          The SaaS Control Plane website and pilot application are provided for evaluation, onboarding, operational
          planning, and early customer use. Access may be limited, suspended, or changed as the product matures.
        </p>
        <p>
          You are responsible for using the platform lawfully, protecting your access credentials, and providing accurate
          information when requesting demos, support, or pilot access.
        </p>
        <p>
          During the current phase, the platform does not promise live ERPNext cutover or production tenant provisioning.
          Any live integration work remains subject to later readiness and operator approval.
        </p>
        <p>
          To the extent permitted by law, the service is provided on an as-available basis during this pilot stage. More
          detailed commercial and support terms can be defined in separate customer agreements as the product moves to
          full launch.
        </p>
      </div>
    </div>
  );
}
