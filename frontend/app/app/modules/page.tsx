const modules = [
  {
    title: "CRM",
    description: "Customer and opportunity management for the SaaS layer.",
  },
  {
    title: "Field Ops",
    description:
      "Field-work coordination built for drilling and service teams.",
  },
  {
    title: "Drilling",
    description:
      "Industry-specific capabilities that shape the future ERPNext template.",
  },
  {
    title: "Fleet",
    description: "Vehicle and equipment support for operations-heavy teams.",
  },
  {
    title: "Inventory",
    description: "Stock and materials tracking for site operations.",
  },
  {
    title: "Reporting",
    description: "Simple operational reporting and admin visibility.",
  },
];

export default function AppModulesPage() {
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
          Modules
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Review the module catalog that shapes packaging, onboarding, and
          rollout scope.
        </h1>
        <p
          className="mt-4 max-w-2xl text-sm leading-7"
          style={{ color: "var(--muted)" }}
        >
          Module choices influence implementation plans, tenant readiness, and
          future ERPNext configuration. This route keeps the control-plane
          vocabulary visible inside the dashboard.
        </p>
      </section>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {modules.map((item) => (
          <article
            key={item.title}
            className="rounded-2xl border p-5"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface-strong)",
            }}
          >
            <p
              className="text-sm font-semibold"
              style={{ color: "var(--text)" }}
            >
              {item.title}
            </p>
            <p
              className="mt-2 text-sm leading-6"
              style={{ color: "var(--muted)" }}
            >
              {item.description}
            </p>
          </article>
        ))}
      </div>
    </div>
  );
}
