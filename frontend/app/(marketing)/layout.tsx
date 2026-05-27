import type { ReactNode } from "react";
import { MarketingHeader } from "@/components/MarketingHeader";
import { MarketingFooter } from "@/components/MarketingFooter";
import { AnalyticsTracker } from "@/components/AnalyticsTracker";

export default function MarketingLayout({ children }: { children: ReactNode }) {
  return (
    <div className="theme-shell relative min-h-screen text-[color:var(--text)]">
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-[28rem] blur-3xl"
        style={{
          background:
            "radial-gradient(circle at 20% 10%, var(--glow) 0%, transparent 42%), radial-gradient(circle at 80% 0%, color-mix(in srgb, var(--accent) 18%, transparent) 0%, transparent 28%)",
        }}
      />
      <MarketingHeader />
      <AnalyticsTracker />
      <main className="relative z-10 mx-auto max-w-7xl px-6 pb-20 pt-10 md:px-8 md:pt-14">
        {children}
      </main>
      <MarketingFooter />
    </div>
  );
}
