import { env } from "@/lib/env";

export type RuntimeRelease = {
  release_id: string;
  commit: string;
  environment: string;
  feature_flags: Record<string, boolean>;
};

export function isPhaseOneShellEnabled(runtime: RuntimeRelease | null): boolean {
  return runtime?.feature_flags?.platform_phase1_shell === true;
}

export async function fetchRuntimeRelease(): Promise<RuntimeRelease> {
  const response = await fetch(`${env.apiBaseUrl}/runtime/release`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Runtime configuration unavailable (${response.status}).`);
  }

  return (await response.json()) as RuntimeRelease;
}
