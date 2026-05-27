"use client";

import type { FormEvent } from "react";
import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { setAuthTokenCookie } from "@/lib/auth";
import { loginLocalUser, registerLocalUser } from "@/lib/auth-api";
import type { OrganizationMembershipRole } from "@/features/auth/types";

type Mode = "login" | "register";

const DEFAULT_ROLE: OrganizationMembershipRole = "owner";

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="grid w-full gap-8 lg:grid-cols-[1.15fr_0.85fr]">
          <section
            className="rounded-[2rem] border p-8 lg:p-10"
            style={{
              borderColor: "var(--border)",
              backgroundColor: "var(--surface)",
            }}
          >
            <p className="text-sm" style={{ color: "var(--muted)" }}>
              Loading sign-in experience...
            </p>
          </section>
        </div>
      }
    >
      <LoginPageContent />
    </Suspense>
  );
}

function LoginPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const nextPath = searchParams.get("next") ?? "/app";

  const [mode, setMode] = useState<Mode>("login");
  const [fullName, setFullName] = useState("");
  const [organizationName, setOrganizationName] = useState("Pilot Workspace");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState<"idle" | "submitting">("idle");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy("submitting");
    setError(null);

    try {
      const response =
        mode === "login"
          ? await loginLocalUser({ email, password })
          : await registerLocalUser({
              email,
              password,
              full_name: fullName,
              organization_name: organizationName,
              membership_role: DEFAULT_ROLE,
              is_platform_admin: false,
            });

      setAuthTokenCookie(response.access_token);
      router.push(nextPath);
      router.refresh();
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Unable to complete auth request.",
      );
    } finally {
      setBusy("idle");
    }
  }

  return (
    <div className="grid w-full gap-8 lg:grid-cols-[1.15fr_0.85fr]">
      <section
        className="rounded-[2rem] border p-8 lg:p-10"
        style={{
          borderColor: "var(--border)",
          backgroundColor: "var(--surface)",
        }}
      >
        <p
          className="text-xs font-semibold uppercase tracking-[0.24em]"
          style={{ color: "var(--muted)" }}
        >
          Secure access
        </p>
        <h1
          className="mt-4 max-w-xl text-4xl font-semibold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          Sign in to the SaaS control plane.
        </h1>
        <p
          className="mt-4 max-w-2xl text-sm leading-7"
          style={{ color: "var(--muted)" }}
        >
          Authentication lives in the SaaS layer so operators and pilot users
          can manage organizations, tenants, and rollout work without mixing
          credentials with ERPNext tenant access.
        </p>

        <div className="mt-8 grid gap-4 sm:grid-cols-3">
          {[
            [
              "Protected shell",
              "Access the dashboard routes for organizations, tenants, modules, and implementation views.",
            ],
            [
              "Separate boundary",
              "ERPNext remains an external runtime target; live cutover is not part of this login flow.",
            ],
            [
              "Pilot-ready",
              "Use the same control-plane account model for demos, pilot setups, and pre-launch validation.",
            ],
          ].map(([title, copy]) => (
            <div
              key={title}
              className="rounded-2xl border p-4"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface-strong)",
              }}
            >
              <p
                className="text-sm font-semibold"
                style={{ color: "var(--text)" }}
              >
                {title}
              </p>
              <p
                className="mt-2 text-sm leading-6"
                style={{ color: "var(--muted)" }}
              >
                {copy}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section
        className="rounded-[2rem] border p-8 lg:p-10"
        style={{
          borderColor: "var(--border)",
          backgroundColor: "var(--surface-strong)",
          boxShadow: "0 24px 50px var(--shadow)",
        }}
      >
        <div
          className="flex gap-2 rounded-2xl border p-1"
          style={{ borderColor: "var(--border)" }}
        >
          {(["login", "register"] as Mode[]).map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => {
                setMode(item);
                setError(null);
              }}
              className="flex-1 rounded-xl px-4 py-3 text-sm font-semibold transition"
              style={{
                backgroundColor:
                  mode === item ? "var(--surface)" : "transparent",
                color: "var(--text)",
              }}
            >
              {item === "login" ? "Sign in" : "Create account"}
            </button>
          ))}
        </div>

        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          {mode === "register" ? (
            <>
              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Full name
                </span>
                <input
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface)",
                    color: "var(--text)",
                  }}
                  placeholder="Jane Smith"
                />
              </label>
              <label className="block space-y-2">
                <span
                  className="text-xs font-semibold uppercase tracking-[0.18em]"
                  style={{ color: "var(--muted)" }}
                >
                  Organization name
                </span>
                <input
                  value={organizationName}
                  onChange={(event) => setOrganizationName(event.target.value)}
                  className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
                  style={{
                    borderColor: "var(--border)",
                    backgroundColor: "var(--surface)",
                    color: "var(--text)",
                  }}
                  placeholder="North Ridge Operations"
                />
              </label>
            </>
          ) : null}

          <label className="block space-y-2">
            <span
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              Email
            </span>
            <input
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface)",
                color: "var(--text)",
              }}
              placeholder="name@company.com"
              autoComplete="email"
            />
          </label>

          <label className="block space-y-2">
            <span
              className="text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ color: "var(--muted)" }}
            >
              Password
            </span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
              style={{
                borderColor: "var(--border)",
                backgroundColor: "var(--surface)",
                color: "var(--text)",
              }}
              placeholder="Enter your password"
              autoComplete={
                mode === "login" ? "current-password" : "new-password"
              }
            />
          </label>

          {error ? (
            <div
              className="rounded-xl border px-4 py-3 text-sm"
              style={{ borderColor: "var(--border)", color: "var(--text)" }}
            >
              {error}
            </div>
          ) : null}

          <button
            type="submit"
            disabled={busy === "submitting"}
            className="w-full rounded-xl px-4 py-3 text-sm font-semibold transition hover:translate-y-[-1px] disabled:cursor-not-allowed disabled:opacity-60"
            style={{
              backgroundColor: "var(--accent)",
              color: "var(--accent-foreground)",
              boxShadow: "0 16px 32px var(--shadow)",
            }}
          >
            {busy === "submitting"
              ? "Working..."
              : mode === "login"
                ? "Sign in to dashboard"
                : "Create workspace account"}
          </button>
        </form>

        <p className="mt-5 text-xs leading-5" style={{ color: "var(--muted)" }}>
          This environment uses SaaS-layer authentication for dashboard access.
          Live ERPNext integration remains a later, explicit cutover step.
        </p>
      </section>
    </div>
  );
}
