import Link from "next/link";

export default function AccessDeniedPage() {
  return (
    <div className="operator-state-card max-w-xl">
      <p className="operator-eyebrow">Access denied</p>
      <h1 className="mt-3 text-2xl font-semibold">You do not have access to this area.</h1>
      <p className="mt-3 text-sm leading-6" style={{ color: "var(--muted)" }}>Ask a platform administrator to confirm your role, or return to the operator workspace.</p>
      <Link className="operator-primary-button mt-6 inline-flex" href="/app">Back to Home</Link>
    </div>
  );
}
