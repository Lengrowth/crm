import type { ReactNode } from "react";
import Link from "next/link";
import { ThemeToggle } from "@/components/ThemeToggle";

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="theme-shell min-h-screen px-6 py-6">
      <div className="mx-auto flex max-w-6xl items-center justify-between">
        <Link
          href="/"
          className="text-sm font-semibold uppercase tracking-[0.24em]"
          style={{ color: "var(--text)" }}
        >
          SaaS Control Plane
        </Link>
        <ThemeToggle />
      </div>
      <main className="mx-auto flex min-h-[calc(100vh-88px)] max-w-6xl items-center py-8">
        {children}
      </main>
    </div>
  );
}
