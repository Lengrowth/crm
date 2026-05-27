export default function AppSettingsPage() {
  return (
    <div className="space-y-6">
      <section
        className="rounded-[2rem] border p-8 lg:p-10"
        style={{
          borderColor: "var(--border)",
          backgroundColor: "var(--surface)",
          boxShadow: "0 24px 60px var(--shadow)",
        }}
      >
        <p
          className="text-xs font-semibold uppercase tracking-[0.24em]"
          style={{ color: "var(--muted)" }}
        >
          Settings
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Platform controls, environment safety, and operator guidance.
        </h1>
        <p
          className="mt-4 max-w-2xl text-sm leading-7"
          style={{ color: "var(--muted)" }}
        >
          Use this area to keep the control plane grounded in safe operational
          defaults while broader admin and integration controls continue to
          mature.
        </p>
      </section>

      <div className="grid gap-6 md:grid-cols-3">
        {[
          [
            "Theme",
            "Light and dark mode remain available for operator comfort across demos and internal reviews.",
          ],
          [
            "Integration safety",
            "Mock ERPNext behavior stays available for local work, while production-like environments now default to an explicit non-mock state.",
          ],
          [
            "Admin readiness",
            "Future phases can expand this area with platform-level policies, secret references, and runtime status checks.",
          ],
        ].map(([title, description]) => (
          <div
            key={title}
            className="rounded-2xl border p-6"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
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
          </div>
        ))}
      </div>
    </div>
  );
}
