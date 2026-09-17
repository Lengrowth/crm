import { chromium } from "@playwright/test";
import axe from "axe-core";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

let baseUrl = (process.env.BASE_URL ?? "").replace(/\/$/, "");
const tokenFile = process.env.AUTH_TOKEN_FILE;
const nonAdminTokenFile = process.env.NON_ADMIN_AUTH_TOKEN_FILE;
const outputDir = process.env.OUTPUT_DIR ?? "browser-evidence";
const expectedShell = process.env.EXPECTED_PHASE_ONE_SHELL ?? "on";
const cookieName = process.env.AUTH_COOKIE_NAME ?? "crm-auth-token";
const hostHeader = process.env.HOST_HEADER;
const organizationId = process.env.ORGANIZATION_ID ?? "synthetic-organization";
const tenantId = process.env.TENANT_ID ?? "synthetic-tenant";

if (!baseUrl) throw new Error("BASE_URL is required");
await mkdir(outputDir, { recursive: true });

const routes = [
  "/app",
  "/app/organizations",
  "/app/organizations/new",
  `/app/organizations/${organizationId}`,
  `/app/organizations/${organizationId}/tenants`,
  "/app/tenants",
  "/app/tenants/new",
  `/app/tenants/${tenantId}`,
  "/app/implementation",
  "/app/modules",
  "/app/settings",
];

const browserArgs = process.env.HEADLESS === "false" ? ["--headless=new", "--no-sandbox"] : [];
if (hostHeader) {
  const requestedUrl = new URL(baseUrl);
  const hostName = hostHeader.split(":", 1)[0];
  if (requestedUrl.hostname === "127.0.0.1" || requestedUrl.hostname === "localhost") {
    requestedUrl.hostname = hostName;
    baseUrl = requestedUrl.toString().replace(/\/$/, "");
    browserArgs.push(`--host-resolver-rules=MAP ${hostName} 127.0.0.1`);
  }
}
const browser = await chromium.launch({ headless: process.env.HEADLESS !== "false", args: browserArgs, executablePath: process.env.BROWSER_EXECUTABLE_PATH || undefined });
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
if (tokenFile) {
  const token = (await readFile(tokenFile, "utf8")).trim();
  if (!token) throw new Error("AUTH_TOKEN_FILE is empty");
  await context.addCookies([{ name: cookieName, value: token, url: `${baseUrl}/` }]);
}

const results = [];
for (const route of routes) {
  const page = await context.newPage();
  const response = await page.goto(`${baseUrl}${route}`, { waitUntil: "networkidle", timeout: 30000 });
  await page.locator("main").waitFor({ state: "attached", timeout: 10000 });
  const bodyText = await page.locator("body").innerText();
  if (!bodyText.trim()) throw new Error(`empty browser document for ${route}`);
  results.push({ route, status: response?.status() ?? null, title: await page.title(), main: await page.locator("main").count(), navigation: await page.locator("nav").count() });
  await page.screenshot({ path: path.join(outputDir, `${route.replaceAll("/", "_").replace(/^_/, "")}.png`), fullPage: true });
  await page.close();
}

const desktop = await context.newPage();
await desktop.goto(`${baseUrl}/app`, { waitUntil: "networkidle", timeout: 30000 });
await desktop.addScriptTag({ content: axe.source });
const desktopA11y = await desktop.evaluate(async () => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa"] } }));
await desktop.screenshot({ path: path.join(outputDir, "app-desktop.png"), fullPage: true });

await desktop.setViewportSize({ width: 390, height: 844 });
await desktop.reload({ waitUntil: "networkidle", timeout: 30000 });
await desktop.addScriptTag({ content: axe.source });
let mobileA11y;
const shellMarker = await desktop.locator("nav[aria-label='Primary navigation']").count() ? "on" : await desktop.locator("nav[aria-label='Dashboard navigation']").count() ? "off" : "unknown";
if (shellMarker !== expectedShell) throw new Error(`expected shell ${expectedShell}, observed ${shellMarker}`);
if (expectedShell === "on") {
  await desktop.locator("button[aria-label='Open navigation']").click();
  const drawer = desktop.locator("aside[role='dialog'][aria-label='Mobile navigation']");
  await drawer.waitFor({ state: "visible", timeout: 10000 });
  mobileA11y = await desktop.evaluate(async () => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa"] } }));
  await desktop.screenshot({ path: path.join(outputDir, "app-mobile-drawer.png"), fullPage: true });
} else {
  mobileA11y = await desktop.evaluate(async () => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa"] } }));
  await desktop.screenshot({ path: path.join(outputDir, "app-mobile.png"), fullPage: true });
}

const report = {
  captured_at_utc: new Date().toISOString(),
  base_url: baseUrl,
  expected_phase1_shell: expectedShell,
  observed_shell: shellMarker,
  routes: results,
  accessibility: { desktop: desktopA11y, mobile: mobileA11y },
};
if (nonAdminTokenFile) {
  const nonAdminToken = (await readFile(nonAdminTokenFile, "utf8")).trim();
  if (!nonAdminToken) throw new Error("NON_ADMIN_AUTH_TOKEN_FILE is empty");
  const nonAdminContext = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
  await nonAdminContext.addCookies([{ name: cookieName, value: nonAdminToken, url: `${baseUrl}/` }]);
  const nonAdminPage = await nonAdminContext.newPage();
  const nonAdminResponse = await nonAdminPage.goto(`${baseUrl}/app/implementation`, { waitUntil: "networkidle", timeout: 30000 });
  await nonAdminPage.locator("main").waitFor({ state: "attached", timeout: 10000 });
  const nonAdminBody = await nonAdminPage.locator("body").innerText();
  const accessDenied = nonAdminBody.includes("Access denied") && nonAdminBody.includes("You do not have access to this area.");
  const restrictedLinkCount = await nonAdminPage.getByRole("link", { name: "Implementations" }).count();
  if (!accessDenied || restrictedLinkCount !== 0 || nonAdminBody.includes("Track rollout readiness from discovery through go-live.")) {
    throw new Error(`non-admin implementation access check failed: denied=${accessDenied}, restricted_links=${restrictedLinkCount}, body=${nonAdminBody.replace(/\s+/g, " ").slice(0, 500)}`);
  }
  await nonAdminPage.screenshot({ path: path.join(outputDir, "non-admin-implementation-denied.png"), fullPage: true });
  report.authorization = { route: "/app/implementation", status: nonAdminResponse?.status() ?? null, non_admin_access_denied: accessDenied, restricted_navigation_links: restrictedLinkCount };
  await nonAdminContext.close();
}
const seriousViolations = [...desktopA11y.violations, ...mobileA11y.violations].filter((violation) => ["critical", "serious"].includes(violation.impact));
if (seriousViolations.length) throw new Error(`serious accessibility violations: ${seriousViolations.map((violation) => violation.id).join(", ")}`);
await writeFile(path.join(outputDir, "browser-evidence.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");
await browser.close();
