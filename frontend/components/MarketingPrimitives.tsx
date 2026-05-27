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

function cx(...classes: Array<string | false | null | undefined>) {
  return classes.filter(Boolean).join(" ");
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
