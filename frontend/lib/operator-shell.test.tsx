import { fireEvent, render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import type { ReactNode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { OperatorShellFrame, Sidebar } from "@/components/AppShell";
import { operatorNavigation } from "@/lib/navigation";
import {
  COMPACT_STORAGE_KEY,
  GROUPS_STORAGE_KEY,
  persistSidebarPreferences,
  readCollapsedGroups,
  readCompactPreference,
} from "@/lib/operator-preferences";

vi.mock("next/link", () => ({
  default: ({ href, children, ...props }: { href: string; children: ReactNode; [key: string]: unknown }) => (
    <a href={href} {...props}>{children}</a>
  ),
}));

vi.mock("next/navigation", () => ({
  usePathname: () => "/app/organizations/acme/tenants",
  useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }),
}));

vi.mock("@/components/ThemeToggle", () => ({
  ThemeToggle: () => <button type="button" aria-label="Theme">Theme</button>,
}));

const groups = operatorNavigation.slice(0, 2);

afterEach(() => {
  document.body.innerHTML = "";
  window.localStorage.clear();
});

describe("operator shell preferences", () => {
  it("round-trips compact and collapsed-group preferences and rejects malformed data", () => {
    const values = new Map<string, string>();
    const storage = {
      getItem: (key: string) => values.get(key) ?? null,
      setItem: (key: string, value: string) => values.set(key, value),
    };

    persistSidebarPreferences(storage, true, { customers: true, system: false });
    expect(values.get(COMPACT_STORAGE_KEY)).toBe("true");
    expect(readCompactPreference(storage)).toBe(true);
    expect(readCollapsedGroups(storage)).toEqual({ customers: true, system: false });

    values.set(GROUPS_STORAGE_KEY, "not-json");
    expect(readCollapsedGroups(storage)).toEqual({});
    values.set(GROUPS_STORAGE_KEY, JSON.stringify({ customers: "yes", system: false, "": true }));
    expect(readCollapsedGroups(storage)).toEqual({ system: false });
  });
});

describe("operator shell interaction and accessibility", () => {
  it("exposes active links, mobile drawer controls, and keyboard-close behavior", () => {
    const onCloseMobile = vi.fn();
    render(
      <Sidebar
        groups={groups}
        pathname="/app/organizations/acme/tenants"
        compact={false}
        collapsedGroups={{}}
        mobileOpen={true}
        onCloseMobile={onCloseMobile}
        onToggleCompact={vi.fn()}
        onToggleGroup={vi.fn()}
      />,
    );

    const closeButtons = screen.getAllByRole("button", { name: "Close navigation" });
    expect(closeButtons).toHaveLength(2);
    expect(closeButtons[1]).toHaveAttribute("type", "button");
    expect(screen.getAllByRole("link", { name: "Companies" }).filter((link) => link.getAttribute("aria-current") === "page")).toHaveLength(2);
    expect(screen.getAllByRole("link", { name: "ERP Sites" }).every((link) => link.getAttribute("aria-current") !== "page")).toBe(true);
    fireEvent.click(closeButtons[1]);
    expect(onCloseMobile).toHaveBeenCalledTimes(1);
  });

  it("provides the skip target, breadcrumb semantics, and focusable main content", () => {
    render(
      <OperatorShellFrame groups={groups} runtime={{ release_id: "test", commit: "test", environment: "production", feature_flags: { platform_phase1_shell: true } }} user={{ full_name: "Test Operator", email: "operator@example.test", is_platform_admin: true } as never}>
        <p>Page content</p>
      </OperatorShellFrame>,
    );

    expect(screen.getByRole("link", { name: "Skip to main content" })).toHaveAttribute("href", "#main-content");
    expect(screen.getByRole("main")).toHaveAttribute("id", "main-content");
    expect(screen.getByRole("main")).toHaveAttribute("tabindex", "-1");
    expect(screen.getByLabelText("Breadcrumb")).toBeInTheDocument();
    expect(screen.getAllByText("Company tenants")).toHaveLength(2);

    const openButton = screen.getByRole("button", { name: "Open navigation" });
    expect(openButton).toHaveAttribute("aria-expanded", "false");
    fireEvent.click(openButton);
    expect(openButton).toHaveAttribute("aria-expanded", "true");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(openButton).toHaveAttribute("aria-expanded", "false");
  });
});
