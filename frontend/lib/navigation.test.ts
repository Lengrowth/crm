import { describe, expect, it } from "vitest";
import {
  buildBreadcrumbs,
  filterNavigation,
  getPageTitle,
  isNavigationItemActive,
  operatorNavigation,
} from "@/lib/navigation";
import { isPhaseOneShellEnabled } from "@/lib/runtime-config";

describe("operator navigation", () => {
  it("filters platform-admin items while retaining authenticated routes", () => {
    const memberGroups = filterNavigation(operatorNavigation, {
      isAuthenticated: true,
      isPlatformAdmin: false,
    });
    const memberLabels = memberGroups.flatMap((group) => group.items.map((item) => item.label));
    expect(memberLabels).toContain("Companies");
    expect(memberLabels).not.toContain("Implementations");

    const adminLabels = filterNavigation(operatorNavigation, {
      isAuthenticated: true,
      isPlatformAdmin: true,
    }).flatMap((group) => group.items.map((item) => item.label));
    expect(adminLabels).toContain("Implementations");
  });

  it("hides all navigation for an anonymous session and honors item flags", () => {
    expect(filterNavigation(operatorNavigation, { isAuthenticated: false, isPlatformAdmin: true })).toEqual([]);
    const flagged = [{ ...operatorNavigation[0], items: [{ ...operatorNavigation[0].items[0], featureFlag: "future" }] }];
    expect(filterNavigation(flagged, { isAuthenticated: true, isPlatformAdmin: true, featureFlags: { future: false } })).toEqual([]);
    expect(filterNavigation(flagged, { isAuthenticated: true, isPlatformAdmin: true, featureFlags: { future: true } })).toHaveLength(1);
  });

  it("marks only the exact home route active and supports nested routes", () => {
    expect(isNavigationItemActive("/app", "/app")).toBe(true);
    expect(isNavigationItemActive("/app/organizations/abc", "/app")).toBe(false);
    expect(isNavigationItemActive("/app/organizations/abc", "/app/organizations")).toBe(true);
    expect(isNavigationItemActive("/app/organization", "/app/organizations")).toBe(false);
  });

  it("builds stable titles and breadcrumbs for dynamic routes", () => {
    expect(getPageTitle("/app/organizations/abc/tenants")).toBe("Company tenants");
    expect(buildBreadcrumbs("/app/organizations/abc/tenants")).toEqual([
      { label: "Home", href: "/app" },
      { label: "Companies", href: "/app/organizations" },
      { label: "Company tenants" },
    ]);
    expect(buildBreadcrumbs("/app/tenants/new")).toEqual([
      { label: "Home", href: "/app" },
      { label: "ERP Sites", href: "/app/tenants" },
      { label: "New ERP site" },
    ]);
  });

  it("keeps the legacy shell as the fail-closed runtime fallback", () => {
    expect(isPhaseOneShellEnabled(null)).toBe(false);
    expect(isPhaseOneShellEnabled({ release_id: "test", commit: "test", environment: "staging", feature_flags: {} })).toBe(false);
    expect(isPhaseOneShellEnabled({ release_id: "test", commit: "test", environment: "staging", feature_flags: { platform_phase1_shell: true } })).toBe(true);
    expect(isPhaseOneShellEnabled({ release_id: "", commit: "test", environment: "staging", feature_flags: { platform_phase1_shell: true } })).toBe(false);
    expect(isPhaseOneShellEnabled({ release_id: "test", commit: "test", environment: "staging", feature_flags: { platform_phase1_shell: "true" } } as never)).toBe(false);
    expect(isPhaseOneShellEnabled({ release_id: "test", commit: "test", environment: "", feature_flags: { platform_phase1_shell: true } })).toBe(false);
  });
});
