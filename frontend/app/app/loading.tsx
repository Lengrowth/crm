export default function AppLoading() {
  return (
    <div className="operator-state-card" role="status" aria-live="polite">
      <p className="operator-eyebrow">Loading workspace</p>
      <div className="mt-4 h-5 w-48 animate-pulse rounded-full" style={{ backgroundColor: "var(--surface-muted)" }} />
      <div className="mt-3 h-4 max-w-xl animate-pulse rounded-full" style={{ backgroundColor: "var(--surface-muted)" }} />
    </div>
  );
}
