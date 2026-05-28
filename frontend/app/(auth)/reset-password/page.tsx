"use client";

import type { FormEvent } from "react";
import { useMemo, useState, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { confirmPasswordReset } from "@/lib/auth-api";

function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") ?? "";
  const tokenMissing = !token;
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const passwordsMatch = useMemo(() => newPassword === confirmPassword, [confirmPassword, newPassword]);
  const formIsReady = newPassword.length >= 8 && confirmPassword.length >= 8 && passwordsMatch;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (tokenMissing) {
      setError("A reset token is required.");
      return;
    }
    if (newPassword.length < 8) {
      setError("Passwords must be at least 8 characters long.");
      return;
    }
    if (!passwordsMatch) {
      setError("Passwords do not match.");
      return;
    }

    setBusy(true);
    setError(null);
    setStatus(null);

    try {
      const response = await confirmPasswordReset({ token, new_password: newPassword });
      setStatus(response.detail);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Unable to update the password.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto grid w-full max-w-3xl gap-6 rounded-[2rem] border p-8 lg:p-10" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface-strong)", boxShadow: "0 24px 50px var(--shadow)" }}>
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>
          Account recovery
        </p>
        <h1 className="mt-4 text-3xl font-semibold tracking-tight" style={{ color: "var(--text)" }}>
          Set a new password
        </h1>
        <p className="mt-3 text-sm leading-7" style={{ color: "var(--muted)" }}>
          Enter a new password for your control-plane account. The reset link can only be used once.
        </p>
      </div>

      {tokenMissing ? (
        <div className="rounded-xl border px-4 py-3 text-sm" style={{ borderColor: "var(--border)", color: "var(--text)" }}>
          The reset link is missing a token. Please request a new one.
        </div>
      ) : null}

      <form className="space-y-4" onSubmit={handleSubmit}>
        <label className="block space-y-2">
          <span className="text-xs font-semibold uppercase tracking-[0.18em]" style={{ color: "var(--muted)" }}>
            New password
          </span>
          <input
            type="password"
            value={newPassword}
            onChange={(event) => setNewPassword(event.target.value)}
            className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
            style={{ borderColor: "var(--border)", backgroundColor: "var(--surface)", color: "var(--text)" }}
            placeholder="Create a new password"
            autoComplete="new-password"
          />
        </label>

        <label className="block space-y-2">
          <span className="text-xs font-semibold uppercase tracking-[0.18em]" style={{ color: "var(--muted)" }}>
            Confirm new password
          </span>
          <input
            type="password"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
            className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
            style={{ borderColor: "var(--border)", backgroundColor: "var(--surface)", color: "var(--text)" }}
            placeholder="Repeat the new password"
            autoComplete="new-password"
          />
        </label>

        {error ? (
          <div className="rounded-xl border px-4 py-3 text-sm" style={{ borderColor: "var(--border)", color: "var(--text)" }}>
            {error}
          </div>
        ) : null}

        {status ? (
          <div className="rounded-xl border px-4 py-3 text-sm" style={{ borderColor: "var(--border)", color: "var(--text)" }}>
            {status}
          </div>
        ) : null}

        <button
          type="submit"
          disabled={busy || tokenMissing || !formIsReady}
          className="w-full rounded-xl px-4 py-3 text-sm font-semibold transition hover:translate-y-[-1px] disabled:cursor-not-allowed disabled:opacity-60"
          style={{ backgroundColor: "var(--accent)", color: "var(--accent-foreground)", boxShadow: "0 16px 32px var(--shadow)" }}
        >
          {busy ? "Updating password..." : "Update password"}
        </button>
      </form>

      <div className="flex flex-wrap gap-4 text-sm">
        <Link href="/login" className="underline underline-offset-4" style={{ color: "var(--accent)" }}>
          Back to sign in
        </Link>
        <Link href="/forgot-password" className="underline underline-offset-4" style={{ color: "var(--accent)" }}>
          Request a new reset link
        </Link>
      </div>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<div className="mx-auto grid w-full max-w-3xl gap-6 rounded-[2rem] border p-8 lg:p-10" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface-strong)" }}>Loading...</div>}>
      <ResetPasswordForm />
    </Suspense>
  );
}
