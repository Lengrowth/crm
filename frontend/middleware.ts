import { NextRequest, NextResponse } from "next/server";

const AUTH_COOKIE = "crm-auth-token";
const PROTECTED_PREFIXES = ["/app", "/dashboard", "/organizations", "/tenants", "/billing", "/settings"];

function isProtectedPath(pathname: string): boolean {
  return PROTECTED_PREFIXES.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`));
}

export function middleware(request: NextRequest) {
  const { pathname, searchParams } = request.nextUrl;
  const hasSession = Boolean(request.cookies.get(AUTH_COOKIE)?.value);

  if (pathname === "/login" && hasSession) {
    const url = new URL("/app", request.url);
    return NextResponse.redirect(url);
  }

  if (isProtectedPath(pathname) && !hasSession) {
    const url = new URL("/login", request.url);
    url.searchParams.set("next", `${pathname}${searchParams.toString() ? `?${searchParams.toString()}` : ""}`);
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/login", "/app/:path*", "/dashboard/:path*", "/organizations/:path*", "/tenants/:path*", "/billing/:path*", "/settings/:path*"],
};
