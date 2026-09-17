import Link from "next/link";
import { redirect } from "next/navigation";
import { canAccessImplementation, getServerAuthUser } from "@/lib/server-auth";
import PortfolioClient from "./PortfolioClient";

export default async function AppImplementationPage() {
  const user = await getServerAuthUser();
  if (!user) redirect("/login?next=%2Fapp%2Fimplementation");
  if (!canAccessImplementation(user)) return <div className="ui-state ui-state-error max-w-xl"><p className="ui-eyebrow">Access denied</p><h1>You do not have access to implementation work.</h1><p>This area is restricted to platform administrators. Your company and site access remain unchanged.</p><Link className="ui-button ui-button-secondary" href="/app">Back to overview</Link></div>;
  return <PortfolioClient />;
}
