import type { ReactNode } from "react";
import { MarketingHeader } from "@/components/MarketingHeader";
import { MarketingFooter } from "@/components/MarketingFooter";
import { AnalyticsTracker } from "@/components/AnalyticsTracker";
import { MarketingBackdrop } from "@/components/MarketingPrimitives";

export default function MarketingLayout({ children }: { children: ReactNode }) {
  return (
    <div className="marketing-site theme-shell relative min-h-screen text-[color:var(--text)]">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[32rem] blur-3xl">
        <MarketingBackdrop />
      </div>
      <MarketingHeader />
      <AnalyticsTracker />
      <main className="relative z-10 mx-auto max-w-7xl px-6 pb-20 pt-12 md:px-8 md:pt-16 lg:pb-24">
        {children}
      </main>
      <MarketingFooter />
    </div>
  );
}
