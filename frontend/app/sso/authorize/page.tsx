"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { ApiError, authorizeSso } from "@/lib/api";

export default function SsoAuthorizePage() {
  return <Suspense fallback={<main className="mx-auto flex min-h-[70vh] max-w-2xl items-center px-6 py-12"><p role="status">Checking your authorized ERP destination…</p></main>}><SsoAuthorizeContent /></Suspense>;
}

function SsoAuthorizeContent() {
  const params = useSearchParams();
  const router = useRouter();
  const [state, setState] = useState<"loading" | "denied" | "error">("loading");
  const [message, setMessage] = useState("Checking your authorized ERP destination…");
  const requestPath = useMemo(() => `/sso/authorize?${params.toString()}`, [params]);

  useEffect(() => {
    const required = ["tenant_id", "client_id", "audience", "redirect_uri", "state", "code_challenge", "code_challenge_method"];
    if (required.some((key) => !params.get(key))) {
      setState("denied");
      setMessage("This sign-in request is incomplete. Start again from the ERP site.");
      return;
    }
    authorizeSso({
      tenant_id: params.get("tenant_id"),
      client_id: params.get("client_id"),
      audience: params.get("audience"),
      redirect_uri: params.get("redirect_uri"),
      state: params.get("state"),
      code_challenge: params.get("code_challenge"),
      code_challenge_method: params.get("code_challenge_method"),
      requested_path: params.get("requested_path") ?? "/app",
    }).then((response) => {
      const callback = new URL(response.redirect_uri);
      callback.searchParams.set("code", response.code);
      callback.searchParams.set("state", response.state);
      window.location.assign(callback.toString());
    }).catch((cause) => {
      if (cause instanceof ApiError && cause.status === 401) {
        router.replace(`/login?next=${encodeURIComponent(requestPath)}`);
        return;
      }
      setState(cause instanceof ApiError && cause.status < 500 ? "denied" : "error");
      setMessage(cause instanceof Error ? cause.message : "Central sign-in is temporarily unavailable.");
    });
  }, [params, requestPath, router]);

  return (
    <main className="mx-auto flex min-h-[70vh] max-w-2xl items-center px-6 py-12">
      <section className="w-full rounded-[2rem] border p-8 shadow-xl" style={{ borderColor: "var(--border)", backgroundColor: "var(--surface)" }} aria-live="polite">
        <p className="text-xs font-semibold uppercase tracking-[0.24em]" style={{ color: "var(--muted)" }}>LenERP identity</p>
        <h1 className="mt-4 text-3xl font-semibold" style={{ color: "var(--text)" }}>{state === "loading" ? "Opening your ERP workspace" : state === "denied" ? "ERP access was not approved" : "Central sign-in is temporarily unavailable"}</h1>
        <p className="mt-4 text-sm leading-7" style={{ color: "var(--muted)" }}>{message}</p>
        <div className="mt-6 flex flex-wrap gap-3">
          {state !== "loading" ? <Link className="ui-button ui-button-secondary" href="/app">Return to control plane</Link> : null}
          {state === "error" ? <button className="ui-button ui-button-primary" type="button" onClick={() => window.location.reload()}>Try again</button> : null}
        </div>
      </section>
    </main>
  );
}
