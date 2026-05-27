"use client";

import { useEffect } from "react";
import { trackMarketingEvent } from "@/lib/api";

export function AnalyticsTracker() {
  useEffect(() => {
    try {
      trackMarketingEvent({ type: "page_view", path: window.location.pathname });
    } catch (err) {
      // swallow
    }
  }, []);

  return null;
}
