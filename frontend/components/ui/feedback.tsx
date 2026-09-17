import Link from "next/link";
import { AlertTriangle, Inbox, RefreshCw } from "lucide-react";
import { Button } from "./button";

export function Alert({ title, children, tone = "info" }: { title?: string; children: React.ReactNode; tone?: "info" | "warning" | "danger" | "success" }) {
  return <div className={`ui-alert ui-alert-${tone}`} role={tone === "danger" ? "alert" : "status"}><AlertTriangle className="h-4 w-4 shrink-0" aria-hidden="true" /><div>{title ? <p className="font-semibold">{title}</p> : null}<div className="text-sm leading-6">{children}</div></div></div>;
}

export function Skeleton({ className = "" }: { className?: string }) { return <div className={`ui-skeleton ${className}`} aria-hidden="true" />; }

export function EmptyState({ title, description, action }: { title: string; description: string; action?: { label: string; href: string } }) {
  return <div className="ui-state" role="status"><Inbox className="h-7 w-7" aria-hidden="true" /><h2>{title}</h2><p>{description}</p>{action ? <Link className="ui-button ui-button-secondary" href={action.href}>{action.label}</Link> : null}</div>;
}

export function ErrorState({ title = "We couldn't load this view", description = "Try again. If the problem continues, contact support.", onRetry }: { title?: string; description?: string; onRetry?: () => void }) {
  return <div className="ui-state ui-state-error" role="alert"><AlertTriangle className="h-7 w-7" aria-hidden="true" /><h2>{title}</h2><p>{description}</p>{onRetry ? <Button variant="secondary" onClick={onRetry}><RefreshCw className="h-4 w-4" aria-hidden="true" /> Try again</Button> : null}</div>;
}
