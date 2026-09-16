import type { Metadata } from "next";
import { ResellerExperience } from "@/components/resellers/ResellerExperience";

export const metadata: Metadata = {
  title: "Launch your own ERP business | LenERP Partner Network",
  description:
    "Build a recurring-revenue ERP business with a fully white-labelled platform, isolated customer sites, partner-controlled pricing, and implementation support.",
};

export default function HomePage() {
  return <ResellerExperience />;
}
