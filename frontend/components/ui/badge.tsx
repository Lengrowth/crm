import type { HTMLAttributes } from "react";
import { cn } from "./utils";

export type BadgeTone = "neutral" | "info" | "success" | "warning" | "danger";

export function Badge({ tone = "neutral", className, ...props }: HTMLAttributes<HTMLSpanElement> & { tone?: BadgeTone }) {
  return <span className={cn("ui-badge", `ui-badge-${tone}`, className)} {...props} />;
}

export function statusTone(status: string | null | undefined): BadgeTone {
  const value = String(status ?? "").toLowerCase();
  if (["ready", "active", "success", "completed", "closed", "verified"].includes(value)) return "success";
  if (["failed", "cancelled", "suspended", "blocked", "error"].includes(value)) return "danger";
  if (["warning", "pending_dns", "unknown", "provisioning", "running", "queued", "todo", "in_progress"].includes(value)) return "warning";
  if (["trial", "planned", "discovery", "planning", "setup", "configuration", "training", "go_live"].includes(value)) return "info";
  return "neutral";
}

export function StatusBadge({ status }: { status: string | null | undefined }) {
  const label = String(status ?? "Unknown").replaceAll("_", " ");
  return <Badge tone={statusTone(status)}>{label}</Badge>;
}
