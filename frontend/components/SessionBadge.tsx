"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { clearAuthTokenCookie, getAuthTokenCookie } from "@/lib/auth";
import { fetchLocalSession, logoutLocalUser } from "@/lib/auth-api";
import type { AuthUser } from "@/features/auth/types";

type SessionState = "loading" | "anonymous" | "authenticated";

export function SessionBadge() {
  const router = useRouter();
  const [state, setState] = useState<SessionState>("loading");
  const [user, setUser] = useState<AuthUser | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = getAuthTokenCookie();
    if (!token) {
      setState("anonymous");
      return;
    }

    let active = true;
    setState("loading");

    fetchLocalSession()
      .then((payload) => {
        if (!active) {
          return;
        }

        setUser(payload.user);
        setState("authenticated");
      })
      .catch((sessionError: Error) => {
        if (!active) {
          return;
        }

        clearAuthTokenCookie();
        setError(sessionError.message);
        setUser(null);
        setState("anonymous");
      });

    return () => {
      active = false;
    };
  }, []);

  async function handleSignOut() {
    try {
      await logoutLocalUser();
    } catch {
      // Local sign-out should still clear the session cookie even if the backend call fails.
    }

    clearAuthTokenCookie();
    setUser(null);
    setState("anonymous");
    router.push("/login");
    router.refresh();
  }

  return (
    <div
      className="rounded-2xl border p-4 text-sm"
      style={{
        borderColor: "var(--border)",
        backgroundColor: "var(--surface-strong)",
        boxShadow: "0 14px 28px var(--shadow)",
      }}
    >
      <p className="text-[0.65rem] font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>
        Session
      </p>
      {state === "loading" ? (
        <p className="mt-2" style={{ color: "var(--text)" }}>
          Checking local auth...
        </p>
      ) : state === "authenticated" && user ? (
        <div className="mt-2 space-y-3">
          <div>
            <p className="font-semibold" style={{ color: "var(--text)" }}>
              {user.full_name}
            </p>
            <p className="text-xs" style={{ color: "var(--muted)" }}>
              {user.email}
            </p>
          </div>
          <p className="text-xs leading-5" style={{ color: "var(--muted)" }}>
            {user.is_platform_admin
              ? "Platform admin access"
              : `${user.memberships.length} organization membership${user.memberships.length === 1 ? "" : "s"}`}
          </p>
          {!user.email_verified_at ? (
            <div className="rounded-xl border px-3 py-2 text-xs leading-5" style={{ borderColor: "var(--border)", color: "var(--text)" }}>
              <p className="font-semibold">Email not verified</p>
              <p className="mt-1" style={{ color: "var(--muted)" }}>
                Verify your address to keep password recovery and account notifications reliable.
              </p>
              <Link href="/resend-verification" className="mt-2 inline-flex underline underline-offset-4" style={{ color: "var(--accent)" }}>
                Resend verification email
              </Link>
            </div>
          ) : null}
          {error ? (
            <p className="text-xs" style={{ color: "var(--muted)" }}>
              {error}
            </p>
          ) : null}
          <button
            type="button"
            onClick={handleSignOut}
            className="w-full rounded-xl border px-3 py-2 text-xs font-semibold uppercase tracking-[0.18em] transition hover:translate-y-[-1px]"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface)",
              color: "var(--text)",
            }}
          >
            Sign out
          </button>
        </div>
      ) : (
        <div className="mt-2 space-y-3">
          <p style={{ color: "var(--text)" }}>Logged out</p>
          <p className="text-xs leading-5" style={{ color: "var(--muted)" }}>
            Your sign-in uses a secure session shared with the application API.
          </p>
        </div>
      )}
    </div>
  );
}
