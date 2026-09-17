import { describe, expect, it } from "vitest";
import { canAccessImplementation } from "@/lib/server-auth";

describe("implementation route authorization", () => {
  it("allows only platform administrators", () => {
    expect(canAccessImplementation(null)).toBe(false);
    expect(canAccessImplementation({ is_platform_admin: false } as never)).toBe(false);
    expect(canAccessImplementation({ is_platform_admin: true } as never)).toBe(true);
  });
});
