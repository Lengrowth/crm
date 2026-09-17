import Link from "next/link";
import { ChevronRight } from "lucide-react";
import type { Breadcrumb } from "@/lib/navigation";
import { cn } from "./utils";

export function Breadcrumbs({ items }: { items: Breadcrumb[] }) {
  return <nav className="ui-breadcrumbs" aria-label="Breadcrumb">{items.map((item, index) => <span key={`${item.label}-${index}`} className="inline-flex items-center gap-2">{index > 0 ? <ChevronRight className="h-3.5 w-3.5" aria-hidden="true" /> : null}{item.href && index < items.length - 1 ? <Link href={item.href}>{item.label}</Link> : <span aria-current={index === items.length - 1 ? "page" : undefined}>{item.label}</span>}</span>)}</nav>;
}

export function PageHeader({ eyebrow, title, description, actions, className }: { eyebrow?: string; title: string; description?: string; actions?: React.ReactNode; className?: string }) {
  return <header className={cn("ui-page-header", className)}><div className="min-w-0"><div>{eyebrow ? <p className="ui-eyebrow">{eyebrow}</p> : null}<h1>{title}</h1>{description ? <p>{description}</p> : null}</div></div>{actions ? <div className="ui-page-actions">{actions}</div> : null}</header>;
}
