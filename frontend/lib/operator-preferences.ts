export const COMPACT_STORAGE_KEY = "crm-sidebar-compact";
export const GROUPS_STORAGE_KEY = "crm-sidebar-groups";

type PreferenceStorage = Pick<Storage, "getItem" | "setItem">;

export function readCompactPreference(storage: PreferenceStorage | null | undefined): boolean {
  return storage?.getItem(COMPACT_STORAGE_KEY) === "true";
}

export function readCollapsedGroups(storage: PreferenceStorage | null | undefined): Record<string, boolean> {
  if (!storage) return {};

  try {
    const parsed: unknown = JSON.parse(storage.getItem(GROUPS_STORAGE_KEY) ?? "{}");
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return {};

    return Object.fromEntries(
      Object.entries(parsed).filter(([key, value]) => key.length > 0 && typeof value === "boolean"),
    );
  } catch {
    return {};
  }
}

export function persistSidebarPreferences(
  storage: PreferenceStorage | null | undefined,
  compact: boolean,
  collapsedGroups: Record<string, boolean>,
): void {
  if (!storage) return;
  storage.setItem(COMPACT_STORAGE_KEY, String(compact));
  storage.setItem(GROUPS_STORAGE_KEY, JSON.stringify(collapsedGroups));
}
