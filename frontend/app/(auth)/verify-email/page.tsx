"use client";

import { useEffect, useState, Suspense } from "react";
import Link from "next/link";
import { useSearchParams, useRouter } from "next/navigation";
import { confirmEmailVerification } from "@/lib/auth-api";

function VerifyEmailForm() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token") ?? "";
  const [status, setStatus] = useState<string>(token ? "Verifying your email..." : "");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setError("The verification link is missing a token.");
      setStatus("");
      return;
    }

    let active = true;
    confirmEmailVerification({ token })
      .then((response) => {
        if (!active) return;
        setStatus(response.detail);
        router.replace("/login?verified=1");
      })
      .catch((submitError) => {
        if (!active) return;
        setError(submitError instanceof Error ? submitError.message : "Unable to verify the email address.");
        setStatus("");
      });

    return () => {
      active = false;
    };
  }, [router, token]);

  return (
    <div className="mx-auto grid w-full max-w-3xl gap-6 rounded-[2rem] border p-8 lg:p-10" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface-strong)", boxShadow: "0 24px 50px var(--shadow)" }}>
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>
          Email verification
        </p>
        <h1 className="mt-4 text-3xl font-semibold tracking-tight" style={{ color: "var(--text)" }}>
          Verify your email address
        </h1>
        <p className="mt-3 text-sm leading-7" style={{ color: "var(--muted)" }}>
          We're confirming your email so your account can be trusted for future recovery and lifecycle actions.
        </p>
      </div>

      {status ? (
        <div className="rounded-xl border px-4 py-3 text-sm" style={{ borderColor: "var(--border)", color: "var(--text)" }}>
          {status}
        </div>
      ) : null}

      {error ? (
        <div className="rounded-xl border px-4 py-3 text-sm" style={{ borderColor: "var(--border)", color: "var(--text)" }}>
          {error}
        </div>
      ) : null}

      <div className="flex flex-wrap gap-4 text-sm">
        <Link href="/login" className="underline underline-offset-4" style={{ color: "var(--accent)" }}>
          Back to sign in
        </Link>
        <Link href="/resend-verification" className="underline underline-offset-4" style={{ color: "var(--accent)" }}>
          Send another verification email
        </Link>
      </div>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={<div className="mx-auto grid w-full max-w-3xl gap-6 rounded-[2rem] border p-8 lg:p-10" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface-strong)" }}>Loading...</div>}>
      <VerifyEmailForm />
    </Suspense>
  );
}
