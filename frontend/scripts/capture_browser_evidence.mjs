import { chromium } from "@playwright/test";
import axe from "axe-core";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const baseUrl = (process.env.BASE_URL ?? "").replace(/\/$/, "");
const tokenFile = process.env.AUTH_TOKEN_FILE;
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

const browser = await chromium.launch({ headless: process.env.HEADLESS !== "false", args: process.env.HEADLESS === "false" ? ["--headless=new", "--no-sandbox"] : undefined, executablePath: process.env.BROWSER_EXECUTABLE_PATH || undefined });
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce", extraHTTPHeaders: hostHeader ? { Host: hostHeader } : undefined });
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
await desktop.locator("button[aria-label='Open navigation']").click();
const drawer = desktop.locator("aside[role='dialog'][aria-label='Mobile navigation']");
await drawer.waitFor({ state: "visible", timeout: 10000 });
const mobileA11y = await desktop.evaluate(async () => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa"] } }));
await desktop.screenshot({ path: path.join(outputDir, "app-mobile-drawer.png"), fullPage: true });
const shellMarker = await desktop.locator("nav[aria-label='Primary navigation']").count() ? "on" : await desktop.locator("nav[aria-label='Dashboard navigation']").count() ? "off" : "unknown";
if (shellMarker !== expectedShell) throw new Error(`expected shell ${expectedShell}, observed ${shellMarker}`);

const report = {
  captured_at_utc: new Date().toISOString(),
  base_url: baseUrl,
  expected_phase1_shell: expectedShell,
  observed_shell: shellMarker,
  routes: results,
  accessibility: { desktop: desktopA11y, mobile: mobileA11y },
};
const seriousViolations = [...desktopA11y.violations, ...mobileA11y.violations].filter((violation) => ["critical", "serious"].includes(violation.impact));
if (seriousViolations.length) throw new Error(`serious accessibility violations: ${seriousViolations.map((violation) => violation.id).join(", ")}`);
await writeFile(path.join(outputDir, "browser-evidence.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");
await browser.close();
