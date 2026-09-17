import { env } from "@/lib/env";

export type RuntimeRelease = {
  release_id: string;
  commit: string;
  environment: string;
  feature_flags: Record<string, boolean>;
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export function parseRuntimeRelease(value: unknown): RuntimeRelease | null {
  if (!isRecord(value)) return null;
  if (typeof value.release_id !== "string" || value.release_id.trim() === "") return null;
  if (typeof value.commit !== "string" || value.commit.trim() === "") return null;
  if (typeof value.environment !== "string" || value.environment.trim() === "") return null;
  if (!isRecord(value.feature_flags)) return null;
  if (Object.values(value.feature_flags).some((flag) => typeof flag !== "boolean")) return null;

  return {
    release_id: value.release_id,
    commit: value.commit,
    environment: value.environment,
    feature_flags: value.feature_flags as Record<string, boolean>,
  };
}

export function isPhaseOneShellEnabled(runtime: RuntimeRelease | null): boolean {
  return parseRuntimeRelease(runtime)?.feature_flags.platform_phase1_shell === true;
}

export async function fetchRuntimeRelease(): Promise<RuntimeRelease> {
  const response = await fetch(`${env.apiBaseUrl}/runtime/release`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Runtime configuration unavailable (${response.status}).`);
  }

  const runtime = parseRuntimeRelease(await response.json());
  if (!runtime) {
    throw new Error("Runtime configuration is malformed.");
  }
  return runtime;
}
