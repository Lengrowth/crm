import Link from "next/link";
import { marketingNav } from "@/lib/navigation";
import { ThemeToggle } from "@/components/ThemeToggle";

export function MarketingHeader() {
  return (
    <header
      className="border-b backdrop-blur"
      style={{
        borderColor: "var(--border)",
        backgroundColor: "var(--surface)",
      }}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-4">
        <Link
          href="/"
          className="text-sm font-semibold uppercase tracking-[0.2em]"
          style={{ color: "var(--text)" }}
        >
          SaaS Control Plane
        </Link>
        <div className="flex items-center gap-4">
          <nav
            className="flex flex-wrap gap-4 text-sm"
            style={{ color: "var(--muted)" }}
          >
            {marketingNav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="transition hover:opacity-80"
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
