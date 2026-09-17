import Link from "next/link";
import { redirect } from "next/navigation";
import { canAccessImplementation, getServerAuthUser } from "@/lib/server-auth";

const milestones = [
  "Discovery",
  "Configuration",
  "Testing",
  "Training",
  "Go-live",
];

export default async function AppImplementationPage() {
  const user = await getServerAuthUser();
  if (!user) redirect("/login?next=%2Fapp%2Fimplementation");
  if (!canAccessImplementation(user)) {
    return (
      <div className="operator-state-card max-w-xl">
        <p className="operator-eyebrow">Access denied</p>
        <h1 className="mt-3 text-2xl font-semibold">You do not have access to this area.</h1>
        <p className="mt-3 text-sm leading-6" style={{ color: "var(--muted)" }}>
          This area is reserved for platform administrators. Your session and organization access remain unchanged.
        </p>
        <Link className="operator-primary-button mt-6 inline-flex" href="/app">Back to Home</Link>
      </div>
    );
  }

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
          Implementation
        </p>
        <h1
          className="mt-4 text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Track rollout readiness from discovery through go-live.
        </h1>
        <p
          className="mt-4 max-w-2xl text-sm leading-7"
          style={{ color: "var(--muted)" }}
        >
          This view frames the implementation journey for pilot customers and
          internal operators: what has been planned, what still needs
          coordination, and what must be true before launch.
        </p>
      </section>

      <div className="grid gap-4 md:grid-cols-5">
        {milestones.map((milestone, index) => (
          <div
            key={milestone}
            className="rounded-2xl border p-4 text-sm"
            style={{
              borderColor: "var(--border)",
              backgroundColor:
                index % 2 === 0 ? "var(--surface)" : "var(--surface-strong)",
            }}
          >
            <p
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              Step {index + 1}
            </p>
            <p className="mt-2 font-semibold" style={{ color: "var(--text)" }}>
              {milestone}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
