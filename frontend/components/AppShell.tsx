"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import type { ReactNode } from "react";
import { useEffect, useMemo, useRef, useState } from "react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { SessionBadge } from "@/components/SessionBadge";
import { clearAuthTokenCookie, getAuthTokenCookie } from "@/lib/auth";
import { fetchLocalSession, logoutLocalUser } from "@/lib/auth-api";
import { env } from "@/lib/env";
import {
  buildBreadcrumbs,
  filterNavigation,
  getPageTitle,
  isNavigationItemActive,
  operatorNavigation,
  type NavigationGroup,
  type NavigationIcon,
} from "@/lib/navigation";
import { fetchRuntimeRelease, isPhaseOneShellEnabled, type RuntimeRelease } from "@/lib/runtime-config";
import { COMPACT_STORAGE_KEY, GROUPS_STORAGE_KEY, readCollapsedGroups, readCompactPreference } from "@/lib/operator-preferences";
import type { AuthUser } from "@/features/auth/types";

type AppShellProps = { children: ReactNode };
type SessionState = "loading" | "anonymous" | "authenticated";

export function AppShell({ children }: AppShellProps) {
  const pathname = usePathname();
  const [runtime, setRuntime] = useState<RuntimeRelease | null>(null);
  const [sessionState, setSessionState] = useState<SessionState>("loading");
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    fetchRuntimeRelease().then(setRuntime).catch(() => setRuntime(null));
  }, []);

  useEffect(() => {
    const token = getAuthTokenCookie();
    if (!token) {
      setSessionState("anonymous");
      return;
    }

    let active = true;
    fetchLocalSession()
      .then(({ user: sessionUser }) => {
        if (!active) return;
        setUser(sessionUser);
        setSessionState("authenticated");
      })
      .catch(() => {
        if (!active) return;
        clearAuthTokenCookie();
        setUser(null);
        setSessionState("anonymous");
      });

    return () => {
      active = false;
    };
  }, []);

  if (!isPhaseOneShellEnabled(runtime)) {
    return <LegacyAppShell>{children}</LegacyAppShell>;
  }

  if (sessionState === "anonymous") {
    return <SessionRequired />;
  }

  const groups = filterNavigation(operatorNavigation, {
    isAuthenticated: sessionState === "authenticated",
    isPlatformAdmin: user?.is_platform_admin === true,
    featureFlags: runtime?.feature_flags,
  });

  return (
    <OperatorShellFrame groups={groups} runtime={runtime} user={user}>
      {pathname.startsWith("/app/implementation") && user && !user.is_platform_admin ? <AccessDenied /> : children}
    </OperatorShellFrame>
  );
}

export function OperatorShellFrame({ children, groups, runtime, user }: { children: ReactNode; groups: NavigationGroup[]; runtime: RuntimeRelease | null; user: AuthUser | null }) {
  const pathname = usePathname();
  const router = useRouter();
  const [compact, setCompact] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [sessionOpen, setSessionOpen] = useState(false);
  const [collapsedGroups, setCollapsedGroups] = useState<Record<string, boolean>>({});
  const sessionMenuRef = useRef<HTMLDivElement>(null);
  const breadcrumbs = useMemo(() => buildBreadcrumbs(pathname), [pathname]);
  const pageTitle = useMemo(() => getPageTitle(pathname), [pathname]);

  useEffect(() => {
    setCompact(readCompactPreference(window.localStorage));
    setCollapsedGroups(readCollapsedGroups(window.localStorage));
  }, []);

  useEffect(() => { window.localStorage.setItem(COMPACT_STORAGE_KEY, String(compact)); }, [compact]);
  useEffect(() => { window.localStorage.setItem(GROUPS_STORAGE_KEY, JSON.stringify(collapsedGroups)); }, [collapsedGroups]);
  useEffect(() => {
    function closeOnEscape(event: KeyboardEvent) {
      if (event.key === "Escape") { setMobileOpen(false); setSessionOpen(false); }
    }
    document.addEventListener("keydown", closeOnEscape);
    return () => document.removeEventListener("keydown", closeOnEscape);
  }, []);
  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [mobileOpen]);
  useEffect(() => {
    function closeWhenOutside(event: MouseEvent) {
      if (sessionMenuRef.current && !sessionMenuRef.current.contains(event.target as Node)) setSessionOpen(false);
    }
    document.addEventListener("mousedown", closeWhenOutside);
    return () => document.removeEventListener("mousedown", closeWhenOutside);
  }, []);

  async function signOut() {
    try { await logoutLocalUser(); } catch { /* Local sign-out still clears the session cookie. */ }
    clearAuthTokenCookie();
    router.push("/login");
    router.refresh();
  }

  // The build/deployment configuration owns the operator-facing label. The
  // runtime manifest intentionally remains a staging-built candidate even
  // after promotion, so it must not relabel a production shell as staging.
  const displayEnvironment = env.environmentLabel;
  return (
    <div className="operator-shell min-h-screen">
      <a href="#main-content" className="operator-skip-link">Skip to main content</a>
      <div className="flex min-h-screen">
        <Sidebar groups={groups} pathname={pathname} compact={compact} collapsedGroups={collapsedGroups} mobileOpen={mobileOpen} onCloseMobile={() => setMobileOpen(false)} onToggleCompact={() => setCompact((value) => !value)} onToggleGroup={(id) => setCollapsedGroups((value) => ({ ...value, [id]: !value[id] }))} />
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="operator-header">
            <div className="flex min-w-0 items-center gap-3">
              <button type="button" className="operator-icon-button lg:hidden" aria-label="Open navigation" aria-expanded={mobileOpen} onClick={() => setMobileOpen(true)}><MenuIcon /></button>
              <div className="min-w-0">
                <div className="operator-breadcrumbs" aria-label="Breadcrumb">
                  {breadcrumbs.map((crumb, index) => <span key={`${crumb.label}-${index}`} className="flex items-center gap-2">{index > 0 ? <ChevronIcon /> : null}{crumb.href ? <Link href={crumb.href}>{crumb.label}</Link> : <span aria-current="page">{crumb.label}</span>}</span>)}
                </div>
                <h1 className="operator-page-title">{pageTitle}</h1>
              </div>
            </div>
            <div className="operator-header-actions">
              <span className="operator-status" title="Runtime status"><span className="operator-status-dot" aria-hidden="true" /><span className="hidden sm:inline">Operational</span></span>
              <span className="operator-environment">{displayEnvironment}</span>
              <ThemeToggle />
              <div className="relative" ref={sessionMenuRef}>
                <button type="button" className="operator-profile-button" aria-label="Open session menu" aria-expanded={sessionOpen} onClick={() => setSessionOpen((value) => !value)}><span className="operator-avatar" aria-hidden="true">{user ? initials(user.full_name) : "?"}</span><span className="hidden max-w-32 truncate text-left md:block">{user?.full_name ?? "Session"}</span><ChevronDownIcon /></button>
                {sessionOpen ? <div className="operator-session-menu" role="menu"><div className="border-b px-4 py-3" style={{ borderColor: "var(--border)" }}><p className="text-sm font-semibold">{user?.full_name ?? "Session"}</p><p className="mt-1 text-xs" style={{ color: "var(--muted)" }}>{user?.email ?? "Authenticated operator"}</p></div><Link className="operator-menu-item" href="/app/settings" role="menuitem" onClick={() => setSessionOpen(false)}>Account settings</Link><button className="operator-menu-item text-left" type="button" role="menuitem" onClick={signOut}>Sign out</button></div> : null}
              </div>
            </div>
          </header>
          <main id="main-content" tabIndex={-1} className="operator-main">{children}</main>
          <footer className="operator-footer"><span>{env.appName}</span><span aria-hidden="true">·</span><a href={env.supportUrl}>Support</a>{env.statusUrl ? <><span aria-hidden="true">·</span><a href={env.statusUrl}>Status</a></> : null}</footer>
        </div>
      </div>
    </div>
  );
}

export function Sidebar({ groups, pathname, compact, collapsedGroups, mobileOpen, onCloseMobile, onToggleCompact, onToggleGroup }: { groups: NavigationGroup[]; pathname: string; compact: boolean; collapsedGroups: Record<string, boolean>; mobileOpen: boolean; onCloseMobile: () => void; onToggleCompact: () => void; onToggleGroup: (id: string) => void }) {
  const content = <>
    <div className="operator-brand-row"><Link href="/app" className="operator-brand" onClick={onCloseMobile}><span className="operator-brand-mark" aria-hidden="true">L</span><span className={compact ? "sr-only" : ""}>{env.appName}</span></Link><button type="button" className="operator-icon-button lg:hidden" aria-label="Close navigation" onClick={onCloseMobile}><CloseIcon /></button></div>
    <div className={`operator-rail-label ${compact ? "sr-only" : ""}`}><span>Workspace</span><span className="operator-environment">{env.environmentLabel}</span></div>
    <nav aria-label="Primary navigation" className="operator-nav">
      {groups.map((group) => { const collapsed = !compact && collapsedGroups[group.id]; return <div key={group.id} className="operator-nav-group"><button type="button" className={`operator-group-heading ${compact ? "justify-center" : ""}`} aria-expanded={!collapsed} title={compact ? group.label : undefined} onClick={() => onToggleGroup(group.id)}><span className={compact ? "sr-only" : ""}>{group.label}</span>{!compact ? <ChevronDownIcon className={collapsed ? "-rotate-90" : ""} /> : <span className="operator-group-dot" aria-hidden="true" />}</button>{!collapsed ? <div className="space-y-1">{group.items.map((item) => { const active = isNavigationItemActive(pathname, item.href); return <Link key={item.id} href={item.href} className={`operator-nav-link ${active ? "is-active" : ""} ${compact ? "justify-center" : ""}`} aria-current={active ? "page" : undefined} title={compact ? item.label : undefined} onClick={onCloseMobile}><NavIcon name={item.icon} /><span className={compact ? "sr-only" : ""}>{item.label}</span>{active && !compact ? <span className="operator-active-bar" aria-hidden="true" /> : null}</Link>; })}</div> : null}</div>; })}
    </nav>
    <div className="mt-auto pt-6"><button type="button" className={`operator-compact-toggle ${compact ? "justify-center" : ""}`} onClick={onToggleCompact} aria-pressed={compact}><CollapseIcon /><span className={compact ? "sr-only" : ""}>{compact ? "Expand sidebar" : "Compact sidebar"}</span></button></div>
  </>;
  return <><aside className={`operator-sidebar operator-sidebar-desktop ${compact ? "is-compact" : ""}`} aria-label="Desktop navigation">{content}</aside>{mobileOpen ? <div className="operator-mobile-layer" aria-hidden="true" onClick={onCloseMobile} /> : null}<aside className={`operator-sidebar operator-sidebar-mobile ${mobileOpen ? "is-open" : ""}`} aria-label="Mobile navigation">{content}</aside></>;
}

function LegacyAppShell({ children }: AppShellProps) { return <div className="theme-shell min-h-screen"><div className="grid min-h-screen lg:grid-cols-[260px_1fr]"><aside className="border-r p-6" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface)" }}><div className="mb-8"><p className="text-xs font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>Workspace</p><h1 className="mt-2 text-xl font-semibold" style={{ color: "var(--text)" }}>{env.appName}</h1><p className="mt-2 text-sm leading-6" style={{ color: "var(--muted)" }}>Operator routes for customers, sites, modules, and delivery work.</p></div><SessionBadge /><nav className="mt-6 space-y-2 text-sm" aria-label="Dashboard navigation">{operatorNavigation.flatMap((group) => group.items).map((item) => <Link key={item.href} href={item.href} className="block rounded-xl border px-4 py-3 transition hover:translate-x-0.5" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface-strong)", color: "var(--text)", boxShadow: "0 10px 30px var(--shadow)" }}>{item.label}</Link>)}</nav><div className="mt-8"><ThemeToggle /></div></aside><main className="p-6 lg:p-10">{children}</main></div></div>; }
function SessionRequired() { return <div className="theme-shell flex min-h-screen items-center justify-center p-6"><div className="operator-state-card"><p className="operator-eyebrow">Session required</p><h1 className="mt-3 text-2xl font-semibold">Sign in to continue</h1><p className="mt-3 text-sm leading-6" style={{ color: "var(--muted)" }}>Your session is no longer valid. Sign in again to access the operator workspace.</p><Link className="operator-primary-button mt-6 inline-flex" href="/login">Return to sign in</Link></div></div>; }
function AccessDenied() { return <div className="operator-state-card max-w-xl"><p className="operator-eyebrow">Access denied</p><h2 className="mt-3 text-2xl font-semibold">You do not have access to this area</h2><p className="mt-3 text-sm leading-6" style={{ color: "var(--muted)" }}>This area is reserved for platform administrators. Your session and organization access remain unchanged.</p><Link className="operator-primary-button mt-6 inline-flex" href="/app">Back to Home</Link></div>; }
function initials(name: string) { return name.split(/\s+/).filter(Boolean).slice(0, 2).map((part) => part[0]).join("").toUpperCase() || "?"; }

function NavIcon({ name }: { name: NavigationIcon }) { const common = { fill: "none", stroke: "currentColor", strokeWidth: 1.8, strokeLinecap: "round" as const, strokeLinejoin: "round" as const }; const paths: Record<NavigationIcon, ReactNode> = { home: <><path d="m3 10 9-7 9 7" /><path d="M5 9.5V21h14V9.5" /><path d="M9 21v-6h6v6" /></>, building: <><path d="M4 21V5a2 2 0 0 1 2-2h8v18" /><path d="M14 9h4a2 2 0 0 1 2 2v10" /><path d="M8 7h2M8 11h2M8 15h2M17 13h1M17 17h1" /></>, server: <><rect x="3" y="4" width="18" height="6" rx="1.5" /><rect x="3" y="14" width="18" height="6" rx="1.5" /><path d="M7 7h.01M7 17h.01M11 7h7M11 17h7" /></>, route: <><circle cx="5" cy="6" r="2" /><circle cx="19" cy="18" r="2" /><path d="M7 6h5a4 4 0 0 1 4 4v4a4 4 0 0 0 4 4M17 18h-1" /></>, grid: <><rect x="4" y="4" width="6" height="6" rx="1" /><rect x="14" y="4" width="6" height="6" rx="1" /><rect x="4" y="14" width="6" height="6" rx="1" /><rect x="14" y="14" width="6" height="6" rx="1" /></>, settings: <><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1" /><circle cx="12" cy="12" r="4" /></> }; return <svg aria-hidden="true" viewBox="0 0 24 24" className="operator-nav-icon" {...common}>{paths[name]}</svg>; }
function MenuIcon() { return <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 7h16M4 12h16M4 17h16" /></svg>; }
function CloseIcon() { return <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2"><path d="m6 6 12 12M18 6 6 18" /></svg>; }
function ChevronIcon() { return <svg aria-hidden="true" viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth="2"><path d="m9 18 6-6-6-6" /></svg>; }
function ChevronDownIcon({ className = "" }: { className?: string }) { return <svg aria-hidden="true" viewBox="0 0 24 24" className={`h-4 w-4 transition-transform ${className}`} fill="none" stroke="currentColor" strokeWidth="2"><path d="m6 9 6 6 6-6" /></svg>; }
function CollapseIcon() { return <svg aria-hidden="true" viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2"><path d="m15 6-6 6 6 6M20 4v16M4 4v16" /></svg>; }
