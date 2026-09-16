export const marketingNav = [
  { href: "/", label: "Partners" },
  { href: "/modules", label: "Platform" },
  { href: "/industries", label: "Industries" },
  { href: "/pricing", label: "Pricing" },
  { href: "/contact", label: "Contact" },
];

export const marketingUtilityNav = [
  { href: "/demo", label: "Book a demo" },
  { href: "/contact", label: "Talk to us" },
  { href: "/login", label: "Sign in" },
];

export const marketingFooterSections = [
  {
    title: "Product",
    links: [
      { href: "/", label: "Partner overview" },
      { href: "/modules", label: "Features" },
      { href: "/pricing", label: "Pricing" },
      { href: "/demo", label: "Book a demo" },
    ],
  },
  {
    title: "Industries",
    links: [
      { href: "/industries", label: "All industries" },
      { href: "/industries", label: "Manufacturing" },
      { href: "/industries", label: "Field operations" },
      { href: "/contact", label: "Talk to us" },
    ],
  },
  {
    title: "Company",
    links: [
      { href: "/contact", label: "Contact" },
      { href: "/login", label: "Client sign in" },
    ],
  },
  {
    title: "Legal",
    links: [
      { href: "/privacy", label: "Privacy" },
      { href: "/terms", label: "Terms" },
    ],
  },
];

export const dashboardNav = [
  { href: "/app", label: "Overview" },
  { href: "/app/organizations", label: "Organizations" },
  { href: "/app/tenants", label: "Tenants" },
  { href: "/app/modules", label: "Modules" },
  { href: "/app/implementation", label: "Implementation" },
  { href: "/app/settings", label: "Settings" },
];

export type NavigationIcon =
  | "home"
  | "building"
  | "server"
  | "route"
  | "grid"
  | "settings";

export type NavigationPermission = "authenticated" | "platform_admin";

export type NavigationBadgeSource =
  | { kind: "count"; key: string }
  | { kind: "status"; key: string };

export type NavigationExtensionPoint = {
  packageId: string;
  slot: "group" | "item";
};

export type NavigationItem = {
  id: string;
  label: string;
  href: string;
  icon: NavigationIcon;
  permission: NavigationPermission;
  featureFlag?: string;
  badgeSource?: NavigationBadgeSource;
  extensionPoint?: NavigationExtensionPoint;
};

export type NavigationGroup = {
  id: string;
  label: string;
  items: NavigationItem[];
  featureFlag?: string;
  extensionPoint?: NavigationExtensionPoint;
};

export type NavigationContext = {
  isAuthenticated: boolean;
  isPlatformAdmin: boolean;
  featureFlags?: Record<string, boolean>;
};

export type Breadcrumb = {
  label: string;
  href?: string;
};

export const operatorNavigation: NavigationGroup[] = [
  {
    id: "work",
    label: "Work",
    items: [
      {
        id: "home",
        label: "Home",
        href: "/app",
        icon: "home",
        permission: "authenticated",
      },
    ],
  },
  {
    id: "customers",
    label: "Customers",
    items: [
      {
        id: "companies",
        label: "Companies",
        href: "/app/organizations",
        icon: "building",
        permission: "authenticated",
      },
      {
        id: "erp-sites",
        label: "ERP Sites",
        href: "/app/tenants",
        icon: "server",
        permission: "authenticated",
      },
    ],
  },
  {
    id: "delivery",
    label: "Delivery",
    items: [
      {
        id: "implementations",
        label: "Implementations",
        href: "/app/implementation",
        icon: "route",
        permission: "platform_admin",
      },
    ],
  },
  {
    id: "product",
    label: "Product",
    items: [
      {
        id: "modules",
        label: "Modules",
        href: "/app/modules",
        icon: "grid",
        permission: "authenticated",
      },
    ],
  },
  {
    id: "system",
    label: "System",
    items: [
      {
        id: "settings",
        label: "Settings",
        href: "/app/settings",
        icon: "settings",
        permission: "authenticated",
      },
    ],
  },
];

export function canViewNavigationItem(
  item: NavigationItem,
  context: NavigationContext,
): boolean {
  if (!context.isAuthenticated) {
    return false;
  }

  if (item.permission === "platform_admin" && !context.isPlatformAdmin) {
    return false;
  }

  return item.featureFlag === undefined || context.featureFlags?.[item.featureFlag] === true;
}

export function filterNavigation(
  groups: NavigationGroup[],
  context: NavigationContext,
): NavigationGroup[] {
  return groups
    .filter((group) => group.featureFlag === undefined || context.featureFlags?.[group.featureFlag] === true)
    .map((group) => ({
      ...group,
      items: group.items.filter((item) => canViewNavigationItem(item, context)),
    }))
    .filter((group) => group.items.length > 0);
}

export function isNavigationItemActive(pathname: string, href: string): boolean {
  return href === "/app"
    ? pathname === href
    : pathname === href || pathname.startsWith(`${href}/`);
}

function titleForSegment(segment: string): string {
  return segment
    .replace(/[-_]/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

export function getPageTitle(pathname: string): string {
  const exact = operatorNavigation
    .flatMap((group) => group.items)
    .find((item) => item.href === pathname);
  if (exact) {
    return exact.label;
  }

  if (pathname === "/app/organizations/new") return "New company";
  if (pathname.includes("/organizations/") && pathname.endsWith("/tenants")) return "Company tenants";
  if (pathname.includes("/organizations/")) return "Company details";
  if (pathname === "/app/tenants/new") return "New ERP site";
  if (pathname.includes("/tenants/")) return "ERP site details";

  const segment = pathname.split("/").filter(Boolean).pop();
  return segment ? titleForSegment(segment) : "Home";
}

export function buildBreadcrumbs(pathname: string): Breadcrumb[] {
  const breadcrumbs: Breadcrumb[] = [{ label: "Home", href: "/app" }];
  if (pathname === "/app") {
    return breadcrumbs;
  }

  if (pathname.startsWith("/app/organizations")) {
    breadcrumbs.push({ label: "Companies", href: "/app/organizations" });
    if (pathname === "/app/organizations/new") {
      breadcrumbs.push({ label: "New company" });
    } else if (pathname !== "/app/organizations") {
      breadcrumbs.push({ label: pathname.endsWith("/tenants") ? "Company tenants" : "Company details" });
    }
    return breadcrumbs;
  }

  if (pathname.startsWith("/app/tenants")) {
    breadcrumbs.push({ label: "ERP Sites", href: "/app/tenants" });
    if (pathname === "/app/tenants/new") {
      breadcrumbs.push({ label: "New ERP site" });
    } else if (pathname !== "/app/tenants") {
      breadcrumbs.push({ label: "ERP site details" });
    }
    return breadcrumbs;
  }

  breadcrumbs.push({ label: getPageTitle(pathname) });
  return breadcrumbs;
}
