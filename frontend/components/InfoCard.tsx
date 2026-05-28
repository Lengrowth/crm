import type { ReactNode } from "react";

type InfoCardProps = {
  title: string;
  description: string;
  eyebrow?: string;
  children?: ReactNode;
};

export function InfoCard({
  title,
  description,
  eyebrow,
  children,
}: InfoCardProps) {
  return (
    <section
      className="rounded-2xl border p-6 backdrop-blur-sm"
      style={{
        borderColor: "var(--border)",
        backgroundColor: "var(--surface)",
        boxShadow: "0 18px 40px var(--shadow)",
      }}
    >
      {eyebrow ? (
        <p
          className="mb-2 text-xs font-semibold uppercase tracking-[0.2em]"
          style={{ color: "var(--muted)" }}
        >
          {eyebrow}
        </p>
      ) : null}
      <h2 className="text-2xl font-semibold" style={{ color: "var(--text)" }}>
        {title}
      </h2>
      <p className="mt-3 max-w-2xl text-sm leading-6" style={{ color: "var(--muted)" }}>
        {description}
      </p>
      {children ? <div className="mt-5">{children}</div> : null}
    </section>
  );
}
