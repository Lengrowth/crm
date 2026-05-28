"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { motion, useInView } from "framer-motion";
import { useRef } from "react";

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

export type MarketingIconName =
  | "spark"
  | "shield"
  | "grid"
  | "chart"
  | "arrow"
  | "dot"
  | "check"
  | "layers"
  | "eye"
  | "bolt"
  | "building"
  | "flag"
  | "link"
  | "clock";

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
    case "check":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M5 12.5l4.5 4.5 9.5-9.5" />
        </svg>
      );
    case "layers":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M12 2.5 20.5 7 12 11.5 3.5 7 12 2.5Z" />
          <path d="M3.5 12 12 16.5 20.5 12" />
          <path d="M3.5 17 12 21.5 20.5 17" />
        </svg>
      );
    case "eye":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M2.5 12C4.5 7.5 7.8 5 12 5s7.5 2.5 9.5 7c-2 4.5-5.3 7-9.5 7s-7.5-2.5-9.5-7Z" />
          <circle cx="12" cy="12" r="2.75" />
        </svg>
      );
    case "bolt":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M13.5 3 6 13.5h6L10.5 21 18 10.5h-6L13.5 3Z" />
        </svg>
      );
    case "building":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <rect x="4" y="3.5" width="16" height="17" rx="1.5" />
          <path d="M9 20.5V13.5h6v7" />
          <path d="M8 8h2M14 8h2M8 11.5h2M14 11.5h2" />
        </svg>
      );
    case "flag":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M6 3.5v17" />
          <path d="M6 3.5h10.5l-2.5 4.5 2.5 4.5H6" />
        </svg>
      );
    case "link":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <path d="M10 14a4.5 4.5 0 0 0 6.36 0l2.12-2.12a4.5 4.5 0 0 0-6.36-6.36l-1.06 1.06" />
          <path d="M14 10a4.5 4.5 0 0 0-6.36 0L5.52 12.12a4.5 4.5 0 0 0 6.36 6.36l1.06-1.06" />
        </svg>
      );
    case "clock":
      return (
        <svg viewBox="0 0 24 24" {...common}>
          <circle cx="12" cy="12" r="8.5" />
          <path d="M12 7.5V12l3 2.5" />
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

export function MarketingIconBadge({ icon, label, className }: IconBadgeProps) {
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
      <div className="marketing-backdrop-orb marketing-backdrop-orb-one absolute left-[1%] top-[2%] h-52 w-52 rounded-full" />
      <div className="marketing-backdrop-orb marketing-backdrop-orb-two absolute right-[35%] top-[40%] h-72 w-72 rounded-full" />
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
        style={{ color: "var(--accent)" }}
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
    <section
      className="marketing-cta-spotlight marketing-reveal rounded-[2rem] border px-8 py-12 sm:px-12 sm:py-14"
    >
      <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
        <div className="max-w-xl">
          <p
            className="text-xs font-semibold uppercase tracking-[0.28em]"
            style={{ color: "var(--accent)" }}
          >
            Get started
          </p>
          <h2
            className="mt-3 text-3xl font-semibold tracking-[-0.04em] sm:text-4xl"
            style={{ color: "var(--text)" }}
          >
            Ready to see the platform in action?
          </h2>
          <p
            className="mt-3 text-base leading-7"
            style={{ color: "var(--muted)" }}
          >
            Book a demo to see the platform running, or get in touch if you
            want to talk through your business first.
          </p>
        </div>
        <div className="flex shrink-0 flex-wrap gap-3">
          <MarketingButtonLink href="/demo">Book a demo</MarketingButtonLink>
          <MarketingButtonLink href="/contact" variant="secondary">
            Talk to us
          </MarketingButtonLink>
        </div>
      </div>
    </section>
  );
}

type ScrollRevealProps = {
  children: ReactNode;
  className?: string;
  delay?: number;
  stagger?: boolean;
};

export function ScrollReveal({
  children,
  className,
  delay = 0,
  stagger = false,
}: ScrollRevealProps) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "0px 0px -60px 0px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 22 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 22 }}
      transition={{
        duration: 0.56,
        delay,
        ease: [0.22, 1, 0.36, 1],
      }}
      className={cx(stagger ? "marketing-stagger" : "", className)}
    >
      {children}
    </motion.div>
  );
}
