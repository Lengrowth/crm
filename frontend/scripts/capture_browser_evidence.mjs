import { chromium } from "@playwright/test";
import axe from "axe-core";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

let baseUrl = (process.env.BASE_URL ?? "").replace(/\/$/, "");
const tokenFile = process.env.AUTH_TOKEN_FILE;
const nonAdminTokenFile = process.env.NON_ADMIN_AUTH_TOKEN_FILE;
const outputDir = process.env.OUTPUT_DIR ?? "browser-evidence";
const expectedShell = process.env.EXPECTED_PHASE_ONE_SHELL ?? "on";
const expectedRelease = process.env.EXPECTED_RELEASE;
const runtimeReleaseUrl = process.env.RUNTIME_RELEASE_URL;
const rolloutStage = process.env.ROLLOUT_STAGE ?? "operator-validation";
const cookieName = process.env.AUTH_COOKIE_NAME ?? "crm-auth-token";
const hostHeader = process.env.HOST_HEADER;
const organizationId = process.env.ORGANIZATION_ID ?? "synthetic-organization";
const tenantId = process.env.TENANT_ID ?? "synthetic-tenant";
let authToken = null;

if (!baseUrl) throw new Error("BASE_URL is required");
if (!expectedRelease) throw new Error("EXPECTED_RELEASE is required");
if (!runtimeReleaseUrl) throw new Error("RUNTIME_RELEASE_URL is required");
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
  authToken = token;
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

const emptySummary = {
  generated_at: new Date().toISOString(), organization_count: 0, organization_status_counts: {},
  tenant_count: 0, tenant_status_counts: {}, provisioning_status_counts: {}, failed_job_count: 0,
  provisioning_failures: [], implementation_blocker_count: 0, overdue_task_count: 0,
  domain_warning_count: 0, domain_warnings: [], next_actions: [],
};
const emptyStatePage = await context.newPage();
await emptyStatePage.route("**/*", async (route) => {
  const url = new URL(route.request().url());
  if (url.pathname.endsWith("/dashboard/summary")) return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(emptySummary) });
  if (url.pathname.endsWith("/organizations") || url.pathname.endsWith("/tenants")) return route.fulfill({ status: 200, contentType: "application/json", body: "[]" });
  return route.continue();
});
await emptyStatePage.goto(`${baseUrl}/app`, { waitUntil: "networkidle", timeout: 30000 });
if (!(await emptyStatePage.getByText("No companies yet").count()) || !(await emptyStatePage.getByText("No ERP sites yet").count())) throw new Error("dashboard empty state evidence failed");
await emptyStatePage.screenshot({ path: path.join(outputDir, "app-empty-state.png"), fullPage: true });
await emptyStatePage.close();

const partialStatePage = await context.newPage();
await partialStatePage.route("**/*", async (route) => {
  const url = new URL(route.request().url());
  if (url.pathname.endsWith("/organizations") || url.pathname.endsWith("/tenants")) return route.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ detail: "simulated supporting API failure" }) });
  return route.continue();
});
await partialStatePage.goto(`${baseUrl}/app`, { waitUntil: "networkidle", timeout: 30000 });
if (!(await partialStatePage.getByText("Some supporting data is unavailable").count())) throw new Error("dashboard partial-failure evidence failed");
await partialStatePage.screenshot({ path: path.join(outputDir, "app-partial-failure.png"), fullPage: true });
await partialStatePage.close();

const desktop = await context.newPage();
await desktop.goto(`${baseUrl}/app`, { waitUntil: "networkidle", timeout: 30000 });
await desktop.addScriptTag({ content: axe.source });
const desktopA11y = await desktop.evaluate(async () => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa"] } }));
await desktop.screenshot({ path: path.join(outputDir, "app-desktop.png"), fullPage: true });
const themeToggle = desktop.getByRole("button", { name: /Switch to dark mode/ });
if (await themeToggle.count()) {
  await themeToggle.click();
  if (await desktop.locator("html").getAttribute("data-theme") !== "dark") throw new Error("dark theme toggle did not apply");
  await desktop.getByRole("button", { name: /Switch to light mode/ }).click();
}

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
  await desktop.keyboard.press("Escape");
  if (await desktop.locator("button[aria-label='Open navigation']").evaluate((element) => document.activeElement === element) !== true) throw new Error("mobile navigation did not restore focus after Escape");
  await desktop.locator("button[aria-label='Open navigation']").click();
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
  runtime_release: null,
  rollout_validation: {
    stage: rolloutStage,
    principal: "authenticated-platform-operator",
  },
  routes: results,
  accessibility: { desktop: desktopA11y, mobile: mobileA11y },
  state_coverage: { dashboard_success: true, dashboard_empty: true, dashboard_partial_failure: true, route_success: true },
};

const phase2Cleanup = { organization_ids: [], tenant_ids: [] };
const phase2Crud = { status: "not-run", records: [] };
const addUnique = (values, value) => { if (value && !values.includes(value)) values.push(value); };
async function phase2Api(path, method = "GET", payload, token = authToken) {
  if (!token || !runtimeReleaseUrl) throw new Error("authenticated browser evidence requires an auth token and runtime URL");
  const apiOrigin = new URL(runtimeReleaseUrl).origin;
  const headers = { Authorization: `Bearer ${token}`, Host: hostHeader ?? new URL(apiOrigin).hostname };
  if (payload !== undefined) headers["Content-Type"] = "application/json";
  const response = await fetch(`${apiOrigin}${path}`, { method, headers, body: payload === undefined ? undefined : JSON.stringify(payload) });
  let body = null;
  try { body = await response.json(); } catch { /* no response body */ }
  return { status: response.status, body };
}
const existingOrganizations = await phase2Api("/organizations");
if (existingOrganizations.status === 200 && Array.isArray(existingOrganizations.body)) {
  const syntheticName = /^Phase 2 Browser (Alpha|Beta) [a-z0-9-]+$/i;
  for (const organization of existingOrganizations.body.filter((item) => syntheticName.test(item.name ?? ""))) {
    addUnique(phase2Cleanup.organization_ids, organization.id);
    const existingTenants = await phase2Api(`/organizations/${organization.id}/tenants`);
    if (existingTenants.status !== 200 || !Array.isArray(existingTenants.body)) throw new Error(`unable to enumerate synthetic tenants for ${organization.id}`);
    for (const tenant of existingTenants.body) addUnique(phase2Cleanup.tenant_ids, tenant.id);
  }
}
await writeFile(path.join(outputDir, "phase2-cleanup.json"), `${JSON.stringify(phase2Cleanup, null, 2)}\n`, "utf8");
const syntheticSuffix = `${process.env.GITHUB_RUN_ID ?? Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
const orgA = await phase2Api("/organizations", "POST", { name: `Phase 2 Browser Alpha ${syntheticSuffix}`, status: "trial" });
const orgB = await phase2Api("/organizations", "POST", { name: `Phase 2 Browser Beta ${syntheticSuffix}`, status: "lead" });
if (orgA.status !== 201 || orgB.status !== 201 || !orgA.body?.id || !orgB.body?.id) throw new Error(`Phase 2 synthetic company CRUD setup failed: ${orgA.status}/${orgB.status}`);
addUnique(phase2Cleanup.organization_ids, orgA.body.id);
addUnique(phase2Cleanup.organization_ids, orgB.body.id);
await writeFile(path.join(outputDir, "phase2-cleanup.json"), `${JSON.stringify(phase2Cleanup, null, 2)}\n`, "utf8");
const tenantA = await phase2Api(`/organizations/${orgA.body.id}/tenants`, "POST", { tenant_slug: `p2-browser-alpha-${syntheticSuffix}`.toLowerCase(), environment: "staging", status: "planned" });
const tenantB = await phase2Api(`/organizations/${orgB.body.id}/tenants`, "POST", { tenant_slug: `p2-browser-beta-${syntheticSuffix}`.toLowerCase(), environment: "staging", status: "planned" });
if (tenantA.status !== 201 || tenantB.status !== 201 || !tenantA.body?.id || !tenantB.body?.id) throw new Error(`Phase 2 synthetic site CRUD setup failed: ${tenantA.status}/${tenantB.status}`);
addUnique(phase2Cleanup.tenant_ids, tenantA.body.id);
addUnique(phase2Cleanup.tenant_ids, tenantB.body.id);
await writeFile(path.join(outputDir, "phase2-cleanup.json"), `${JSON.stringify(phase2Cleanup, null, 2)}\n`, "utf8");
const updateA = await phase2Api(`/organizations/${orgA.body.id}`, "PATCH", { name: `Phase 2 Browser Alpha Updated ${syntheticSuffix}` });
const organizationsRead = await phase2Api("/organizations");
if (updateA.status !== 200 || organizationsRead.status !== 200 || !organizationsRead.body.some((item) => item.id === orgA.body.id) || !organizationsRead.body.some((item) => item.id === orgB.body.id)) throw new Error("Phase 2 synthetic company read/update verification failed");
phase2Crud.status = "passed";
phase2Crud.records = [{ organization_id: orgA.body.id, tenant_id: tenantA.body.id, updated: updateA.status === 200 }, { organization_id: orgB.body.id, tenant_id: tenantB.body.id, updated: false }];
report.phase2_crud = phase2Crud;
report.phase2_tenant_isolation = { second_company_id: orgB.body.id, admin_can_read_both: true, cleanup_required: true };
await writeFile(path.join(outputDir, "phase2-cleanup.json"), `${JSON.stringify(phase2Cleanup, null, 2)}\n`, "utf8");
const runtimeResponse = await fetch(runtimeReleaseUrl, { cache: "no-store" });
if (!runtimeResponse.ok) throw new Error(`runtime release endpoint returned HTTP ${runtimeResponse.status}`);
const runtimePayload = await runtimeResponse.json();
const runtimeFlag = runtimePayload?.feature_flags?.platform_phase1_shell;
if (runtimePayload?.release_id !== expectedRelease || runtimePayload?.commit !== expectedRelease) {
  throw new Error(`runtime release identity mismatch: expected ${expectedRelease}, observed ${runtimePayload?.release_id ?? "missing"}/${runtimePayload?.commit ?? "missing"}`);
}
if (runtimeFlag !== (expectedShell === "on")) {
  throw new Error(`runtime release flag mismatch: expected ${expectedShell}, observed ${String(runtimeFlag)}`);
}
report.runtime_release = {
  release_id: runtimePayload.release_id,
  commit: runtimePayload.commit,
  environment: runtimePayload.environment ?? null,
  platform_phase1_shell: runtimeFlag,
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
  const accessDenied = nonAdminBody.toLowerCase().includes("access denied") && nonAdminBody.toLowerCase().includes("you do not have access to");
  const restrictedLinkCount = await nonAdminPage.getByRole("link", { name: "Implementations" }).count();
  if (!accessDenied || restrictedLinkCount !== 0 || nonAdminBody.includes("Track rollout readiness from discovery through go-live.")) {
    throw new Error(`non-admin implementation access check failed: denied=${accessDenied}, restricted_links=${restrictedLinkCount}, body=${nonAdminBody.replace(/\s+/g, " ").slice(0, 500)}`);
  }
  await nonAdminPage.screenshot({ path: path.join(outputDir, "non-admin-implementation-denied.png"), fullPage: true });
  report.authorization = { route: "/app/implementation", status: nonAdminResponse?.status() ?? null, non_admin_access_denied: accessDenied, restricted_navigation_links: restrictedLinkCount };
  const secondCompanyResponse = await phase2Api(`/organizations/${orgB.body.id}`, "GET", undefined, nonAdminToken);
  if (![403, 404].includes(secondCompanyResponse.status)) throw new Error(`non-admin second-company isolation check failed with HTTP ${secondCompanyResponse.status}`);
  report.phase2_tenant_isolation.non_admin_second_company_denied = true;
  await nonAdminContext.close();
}
const seriousViolations = [...desktopA11y.violations, ...mobileA11y.violations].filter((violation) => ["critical", "serious"].includes(violation.impact));
if (seriousViolations.length) throw new Error(`serious accessibility violations: ${seriousViolations.map((violation) => violation.id).join(", ")}`);
const seriousIncomplete = [...desktopA11y.incomplete, ...mobileA11y.incomplete].filter((incomplete) => ["critical", "serious"].includes(incomplete.impact));
if (seriousIncomplete.length) throw new Error(`serious incomplete accessibility checks: ${seriousIncomplete.map((incomplete) => incomplete.id).join(", ")}`);
await writeFile(path.join(outputDir, "browser-evidence.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");
await browser.close();
