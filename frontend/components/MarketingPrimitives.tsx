import type { ReactNode } from "react";
import Link from "next/link";

type ButtonVariant = "primary" | "secondary" | "ghost";
type CardTone = "default" | "muted" | "accent";

type LinkButtonProps = {
  href: string;
  children: ReactNode;
  variant?: ButtonVariant;
  className?: string;
};

type CardProps = {
  children: ReactNode;
  className?: string;
  tone?: CardTone;
  interactive?: boolean;
};

type SectionIntroProps = {
  eyebrow: string;
  title: string;
  description: string;
  align?: "left" | "center";
  className?: string;
};

type StatProps = {
  value: string;
  label: string;
  description?: string;
};

export type MarketingIconName = "spark" | "shield" | "grid" | "chart" | "arrow" | "dot";

type IconBadgeProps = {
  icon: MarketingIconName;
  label: string;
  className?: string;
};

function cx(...classes: Array<string | false | null | undefined>) {
  return classes.filter(Boolean).join(" ");
}

export function MarketingIcon({
  icon,
  className,
}: {
  icon: MarketingIconName;
  className?: string;
}) {
  const common = {
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    className,
    "aria-hidden": true,
  };

  switch (icon) {
    case "spark":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M12 2.75l1.86 5.39L19.25 10l-5.39 1.86L12 17.25l-1.86-5.39L4.75 10l5.39-1.86L12 2.75Z" />
        </svg>
      );
    case "shield":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M12 3.25 19 6.1v5.39c0 4.63-3.06 7.49-7 9.26-3.94-1.77-7-4.63-7-9.26V6.1L12 3.25Z" />
          <path d="m9.25 12.1 1.8 1.8 3.7-3.7" />
        </svg>
      );
    case "grid":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <rect x="4.5" y="4.5" width="6.5" height="6.5" rx="1.6" />
          <rect x="13" y="4.5" width="6.5" height="6.5" rx="1.6" />
          <rect x="4.5" y="13" width="6.5" height="6.5" rx="1.6" />
          <rect x="13" y="13" width="6.5" height="6.5" rx="1.6" />
        </svg>
      );
    case "chart":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M4.5 18.5h15" />
          <path d="M6.25 15.75v-3.5" />
          <path d="M11.25 15.75v-6.5" />
          <path d="M16.25 15.75V8.25" />
        </svg>
      );
    case "arrow":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M6 12h12" />
          <path d="m13 6 5 6-5 6" />
        </svg>
      );
    case "dot":
    default:
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <circle cx="12" cy="12" r="3.5" />
        </svg>
      );
  }
}

export function MarketingIconBadge({
  icon,
  label,
  className,
}: IconBadgeProps) {
  return (
    <span
      className={cx(
        "marketing-chip rounded-full px-3 py-2 text-xs font-semibold uppercase tracking-[0.18em]",
        className,
      )}
    >
      <MarketingIcon icon={icon} className="h-4 w-4" />
      <span>{label}</span>
    </span>
  );
}

export function MarketingBackdrop() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden rounded-[inherit]">
      <div className="marketing-backdrop-orb marketing-backdrop-orb-one absolute left-[7%] top-[8%] h-52 w-52 rounded-full" />
      <div className="marketing-backdrop-orb marketing-backdrop-orb-two absolute right-[10%] top-[12%] h-72 w-72 rounded-full" />
      <div className="marketing-backdrop-grid absolute inset-x-0 bottom-0 h-[60%]" />
    </div>
  );
}

export function MarketingButtonLink({
  href,
  children,
  variant = "primary",
  className,
}: LinkButtonProps) {
  const variantClass =
    variant === "primary"
      ? "marketing-button-primary"
      : variant === "secondary"
        ? "marketing-button-secondary"
        : "marketing-button-ghost";

  return (
    <Link
      href={href}
      className={cx(
        "marketing-button marketing-reveal",
        variantClass,
        className,
      )}
    >
      {children}
    </Link>
  );
}

export function MarketingCard({
  children,
  className,
  tone = "default",
  interactive = false,
}: CardProps) {
  const toneClass =
    tone === "accent"
      ? "marketing-panel-accent"
      : tone === "muted"
        ? "marketing-panel-muted"
        : "marketing-panel";

  return (
    <section
      className={cx(
        "marketing-reveal",
        interactive ? "marketing-card-interactive" : "",
        toneClass,
        className,
      )}
    >
      {children}
    </section>
  );
}

export function MarketingSectionIntro({
  eyebrow,
  title,
  description,
  align = "left",
  className,
}: SectionIntroProps) {
  const centered = align === "center";

  return (
    <div
      className={cx(
        "marketing-reveal",
        centered ? "mx-auto max-w-3xl text-center" : "max-w-3xl",
        className,
      )}
    >
      <p
        className="text-xs font-semibold uppercase tracking-[0.28em]"
        style={{ color: "var(--muted)" }}
      >
        {eyebrow}
      </p>
      <h1
        className="mt-4 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl lg:text-6xl"
        style={{ color: "var(--text)" }}
      >
        {title}
      </h1>
      <p
        className="mt-5 text-base leading-8 sm:text-lg"
        style={{ color: "var(--muted)" }}
      >
        {description}
      </p>
    </div>
  );
}

export function MarketingStat({ value, label, description }: StatProps) {
  return (
    <div className="marketing-reveal rounded-[1.5rem] border border-[color:var(--border)] bg-[color:var(--surface-overlay)] p-5">
      <p
        className="text-3xl font-semibold tracking-[-0.04em]"
        style={{ color: "var(--text)" }}
      >
        {value}
      </p>
      <p
        className="mt-2 text-sm font-semibold"
        style={{ color: "var(--text)" }}
      >
        {label}
      </p>
      {description ? (
        <p className="mt-2 text-sm leading-6" style={{ color: "var(--muted)" }}>
          {description}
        </p>
      ) : null}
    </div>
  );
}

export function MarketingPageCta() {
  return (
    <MarketingCard
      className="rounded-[2rem] px-8 py-8 sm:px-10 sm:py-10"
      tone="accent"
    >
      <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-2xl">
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--muted)" }}
          >
            Next step
          </p>
          <h2
            className="mt-3 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
            style={{ color: "var(--text)" }}
          >
            Bring the rollout conversation into one controlled product surface.
          </h2>
          <p
            className="mt-4 text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            Book a demo if you want to see the workflow live, or talk to us if
            you already have a pilot scope, rollout blockers, or a timing
            question.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <MarketingButtonLink href="/demo">Book a demo</MarketingButtonLink>
          <MarketingButtonLink href="/contact" variant="secondary">
            Talk to us
          </MarketingButtonLink>
        </div>
      </div>
    </MarketingCard>
  );
}
