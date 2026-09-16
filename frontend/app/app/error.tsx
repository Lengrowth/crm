"use client";

export default function AppError({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div className="operator-state-card max-w-xl" role="alert">
      <p className="operator-eyebrow">Something went wrong</p>
      <h2 className="mt-3 text-2xl font-semibold">We could not load this workspace view.</h2>
      <p className="mt-3 text-sm leading-6" style={{ color: "var(--muted)" }}>Try the view again. If the problem continues, contact support and include the time of the failed request.</p>
      <button type="button" className="operator-primary-button mt-6" onClick={() => reset()}>Try again</button>
    </div>
  );
}
