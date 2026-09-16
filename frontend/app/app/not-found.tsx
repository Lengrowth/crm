import Link from "next/link";

export default function AppNotFound() {
  return (
    <div className="operator-state-card max-w-xl">
      <p className="operator-eyebrow">Not found</p>
      <h2 className="mt-3 text-2xl font-semibold">That workspace view does not exist.</h2>
      <p className="mt-3 text-sm leading-6" style={{ color: "var(--muted)" }}>The address may be out of date, or the record may have been removed.</p>
      <Link className="operator-primary-button mt-6 inline-flex" href="/app">Back to Home</Link>
    </div>
  );
}
