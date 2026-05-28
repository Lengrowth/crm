"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import Link from "next/link";
import { requestEmailVerification } from "@/lib/auth-api";

export default function ResendVerificationPage() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    setStatus(null);

    try {
      const response = await requestEmailVerification({ email });
      setStatus(response.detail);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Unable to request a verification email.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto grid w-full max-w-3xl gap-6 rounded-[2rem] border p-8 lg:p-10" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface-strong)", boxShadow: "0 24px 50px var(--shadow)" }}>
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>
          Email verification
        </p>
        <h1 className="mt-4 text-3xl font-semibold tracking-tight" style={{ color: "var(--text)" }}>
          Resend the verification email
        </h1>
        <p className="mt-3 text-sm leading-7" style={{ color: "var(--muted)" }}>
          If your account is still waiting on verification, send a fresh verification link to the same email address.
        </p>
      </div>

      <form className="space-y-4" onSubmit={handleSubmit}>
        <label className="block space-y-2">
          <span className="text-xs font-semibold uppercase tracking-[0.18em]" style={{ color: "var(--muted)" }}>
            Email
          </span>
          <input
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            className="w-full rounded-xl border px-4 py-3 text-sm outline-none transition focus:translate-y-[-1px]"
            style={{ borderColor: "var(--border)", backgroundColor: "var(--surface)", color: "var(--text)" }}
            placeholder="name@company.com"
            autoComplete="email"
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
          disabled={busy}
          className="w-full rounded-xl px-4 py-3 text-sm font-semibold transition hover:translate-y-[-1px] disabled:cursor-not-allowed disabled:opacity-60"
          style={{ backgroundColor: "var(--accent)", color: "var(--accent-foreground)", boxShadow: "0 16px 32px var(--shadow)" }}
        >
          {busy ? "Sending verification email..." : "Send verification email"}
        </button>
      </form>

      <div className="flex flex-wrap gap-4 text-sm">
        <Link href="/login" className="underline underline-offset-4" style={{ color: "var(--accent)" }}>
          Back to sign in
        </Link>
        <Link href="/forgot-password" className="underline underline-offset-4" style={{ color: "var(--accent)" }}>
          Forgot your password?
        </Link>
      </div>
    </div>
  );
}
