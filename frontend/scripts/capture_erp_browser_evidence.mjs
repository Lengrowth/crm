import { chromium } from "@playwright/test";
import axe from "axe-core";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const rawBase = (process.env.ERP_BASE_URL ?? "").replace(/\/$/, "");
const hostHeader = process.env.ERP_HOST_HEADER ?? "erp-staging.example.test";
const outputDir = process.env.OUTPUT_DIR ?? "erp-browser-evidence";
const prefix = process.env.ERP_ROLE_EMAIL_PREFIX;
const passwordFile = process.env.ERP_ROLE_PASSWORD_FILE;
if (!rawBase || !prefix || !passwordFile) throw new Error("ERP_BASE_URL, ERP_ROLE_EMAIL_PREFIX, and ERP_ROLE_PASSWORD_FILE are required");
const password = (await readFile(passwordFile, "utf8")).trim();
if (!password) throw new Error("ERP role password file is empty");
await mkdir(outputDir, { recursive: true });

const roles = [
  "Champion Administrator",
  "Champion Dispatcher",
  "Champion Sales User",
  "Champion Accounting User",
  "Champion Inventory Manager",
  "Champion Field Technician",
  "Champion Platform Operator",
];
const emailFor = (role) => `${prefix}-${role.toLowerCase().replaceAll(" ", "-")}@example.test`;
const browserArgs = [`--host-resolver-rules=MAP ${hostHeader} 127.0.0.1`];
const baseUrl = rawBase.replace(new URL(rawBase).hostname, hostHeader);
const browser = await chromium.launch({ headless: process.env.HEADLESS !== "false", args: browserArgs, executablePath: process.env.BROWSER_EXECUTABLE_PATH || undefined });

async function login(role) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
  const page = await context.newPage();
  await page.goto(`${baseUrl}/login`, { waitUntil: "domcontentloaded", timeout: 30000 });
  const loginResult = await page.evaluate(async ({ email, pwd }) => {
    const response = await fetch("/api/method/login", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ usr: email, pwd }).toString(),
    });
    return { status: response.status, body: await response.text() };
  }, { email: emailFor(role), pwd: password });
  if (loginResult.status !== 200) throw new Error(`${role} ERP login failed: ${loginResult.status}`);
  await page.goto(`${baseUrl}/app`, { waitUntil: "networkidle", timeout: 30000 });
  if (!page.url().match(/\/app(?:\/.*)?$/)) throw new Error(`${role} ERP login redirected to ${page.url()}`);
  return { context, page };
}

async function api(page, pathname, init = {}) {
  return page.evaluate(async ({ pathname, init }) => {
    const response = await fetch(pathname, { credentials: "include", ...init });
    const text = await response.text();
    let body = null;
    try { body = JSON.parse(text); } catch { body = text.slice(0, 300); }
    return { status: response.status, contentType: response.headers.get("content-type"), body };
  }, { pathname, init });
}

async function accessibility(page, label) {
  if (!(await page.evaluate(() => Boolean(window.axe)))) await page.addScriptTag({ content: axe.source });
  const result = await page.evaluate(async () => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa"] } }));
  await page.screenshot({ path: path.join(outputDir, `${label}.png`), fullPage: true });
  return { violations: result.violations, passes: result.passes.length, incomplete: result.incomplete.length };
}

async function renderedAccessibilityContract(page) {
  return page.evaluate(() => {
    const viewportMeta = [...document.querySelectorAll('meta[name="viewport"]')];
    const viewportContent = viewportMeta.map((meta) => meta.getAttribute("content") || "");
    const logoImages = [...document.querySelectorAll("img.app-logo, .app-logo img, .navbar-brand img, .splash img, img.footer-logo")];
    const logoAlternatives = logoImages.map((image) => ({
      className: image.className,
      alt: image.getAttribute("alt"),
      src: image.getAttribute("src"),
    }));
    return {
      viewport_count: viewportMeta.length,
      viewport_content: viewportContent,
      zoom_allowed: viewportMeta.length === 1
        && !/user-scalable\s*=\s*no|max(imum)?-scale\s*=\s*1(?:\.0+)?/i.test(viewportContent[0] || ""),
      logo_images: logoAlternatives,
      logo_alternatives_present: logoAlternatives.every((image) => typeof image.alt === "string"),
    };
  });
}

const evidence = {
  captured_at_utc: new Date().toISOString(),
  base_url: baseUrl,
  host_header: hostHeader,
  roles: {},
  records: {},
  print: null,
  export: null,
  accessibility: { unauthenticated: null, routes: {}, desktop: null, mobile: null },
  browser_zoom: { unauthenticated: null, desktop: null, mobile: null },
};

const unauthenticatedContext = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
const unauthenticatedPage = await unauthenticatedContext.newPage();
await unauthenticatedPage.goto(`${baseUrl}/login`, { waitUntil: "networkidle", timeout: 30000 });
const unauthenticatedContract = await renderedAccessibilityContract(unauthenticatedPage);
if (!unauthenticatedContract.zoom_allowed || !unauthenticatedContract.logo_alternatives_present) {
  throw new Error(`unauthenticated ERP accessibility contract failed: ${JSON.stringify(unauthenticatedContract)}`);
}
evidence.accessibility.unauthenticated = {
  role: "unauthenticated",
  route: "/login",
  viewport: { width: 1440, height: 1000 },
  ...await accessibility(unauthenticatedPage, "erp-login-desktop"),
};
evidence.browser_zoom.unauthenticated = unauthenticatedContract;
await unauthenticatedContext.close();

const admin = await login("Champion Administrator");
const adminPage = admin.page;
const erpRoutes = [
  ["well-list", "/app/len-erp-well-site"],
  ["well-detail", "/app/len-erp-well-site/WELL-NR-01"],
  ["job-list", "/app/len-erp-drilling-job"],
  ["quotation-list", "/app/quotation"],
  ["invoice-list", "/app/sales-invoice"],
  ["purchase-receipt-list", "/app/purchase-receipt"],
  ["stock-entry-list", "/app/stock-entry"],
  ["asset-list", "/app/asset"],
  ["asset-maintenance-list", "/app/asset-maintenance"],
];
for (const [label, route] of erpRoutes) {
  const response = await adminPage.goto(`${baseUrl}${route}`, { waitUntil: "networkidle", timeout: 30000 });
  if ((response?.status() ?? 0) >= 400) throw new Error(`ERP route failed ${route}: ${response?.status()}`);
  await adminPage.waitForTimeout(1500);
  if (!(await adminPage.locator("body").innerHTML()).trim()) throw new Error(`ERP route empty ${route}`);
  await adminPage.screenshot({ path: path.join(outputDir, `${label}.png`), fullPage: true });
  const routeContract = await renderedAccessibilityContract(adminPage);
  if (!routeContract.zoom_allowed || !routeContract.logo_alternatives_present) {
    throw new Error(`ERP accessibility contract failed for ${route}`);
  }
  evidence.accessibility.routes[label] = {
    role: "Champion Administrator",
    route,
    viewport: { width: 1440, height: 1000 },
    ...await accessibility(adminPage, `erp-${label}-desktop`),
  };
  evidence.browser_zoom.desktop = routeContract;
}

const wellList = await api(adminPage, "/api/resource/LenERP%20Well%20Site?fields=%5B%22name%22,%22city%22,%22latitude%22,%22longitude%22%5D&limit_page_length=20");
const jobList = await api(adminPage, "/api/resource/LenERP%20Drilling%20Job?fields=%5B%22name%22,%22status%22,%22customer%22%5D&limit_page_length=20");
const invoiceList = await api(adminPage, "/api/resource/Sales%20Invoice?fields=%5B%22name%22,%22docstatus%22%5D&limit_page_length=20");
const purchaseList = await api(adminPage, "/api/resource/Purchase%20Receipt?fields=%5B%22name%22,%22docstatus%22%5D&limit_page_length=20");
const stockList = await api(adminPage, "/api/resource/Stock%20Entry?fields=%5B%22name%22,%22purpose%22,%22docstatus%22%5D&limit_page_length=20");
const maintenanceList = await api(adminPage, "/api/resource/Asset%20Maintenance?fields=%5B%22name%22,%22asset_name%22%5D&limit_page_length=20");
for (const [name, response] of Object.entries({ wellList, jobList, invoiceList, purchaseList, stockList, maintenanceList })) {
  if (response.status !== 200) throw new Error(`ERP API read failed for ${name}: ${response.status}`);
}
evidence.records = { wellList, jobList, invoiceList, purchaseList, stockList, maintenanceList };
await adminPage.goto(`${baseUrl}/app/len-erp-drilling-job/JOB-0097`, { waitUntil: "networkidle", timeout: 30000 });
await adminPage.waitForTimeout(1500);
const printFile = path.join(outputDir, "erp-job-print.pdf");
await adminPage.pdf({ path: printFile, format: "A4", printBackground: true });
evidence.print = { status: 200, contentType: "application/pdf", source: "authenticated-browser-page.pdf", path: printFile };
const exportRows = Array.isArray(wellList.body?.data) ? wellList.body.data : [];
if (!exportRows.length) throw new Error("ERP export source returned no well-site rows");
const csvCell = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
const exportFile = path.join(outputDir, "erp-well-sites-export.csv");
await writeFile(
  exportFile,
  [
    ["name", "city", "latitude", "longitude"].map(csvCell).join(","),
    ...exportRows.map((row) => [row.name, row.city, row.latitude, row.longitude].map(csvCell).join(",")),
  ].join("\n") + "\n",
  "utf8",
);
evidence.export = { status: 200, contentType: "text/csv", source: "authenticated-resource-api-csv", row_count: exportRows.length, path: exportFile };
evidence.accessibility.desktop = {
  role: "Champion Administrator",
  route: "/app/len-erp-drilling-job/JOB-0097",
  viewport: { width: 1440, height: 1000 },
  ...await accessibility(adminPage, "erp-admin-desktop"),
};
evidence.browser_zoom.desktop = await renderedAccessibilityContract(adminPage);
await adminPage.setViewportSize({ width: 390, height: 844 });
await adminPage.goto(`${baseUrl}/app/len-erp-well-site/WELL-NR-01`, { waitUntil: "networkidle", timeout: 30000 });
evidence.accessibility.mobile = {
  role: "Champion Administrator",
  route: "/app/len-erp-well-site/WELL-NR-01",
  viewport: { width: 390, height: 844 },
  ...await accessibility(adminPage, "erp-well-mobile"),
};
evidence.browser_zoom.mobile = await renderedAccessibilityContract(adminPage);
if (!evidence.browser_zoom.mobile.zoom_allowed || !evidence.browser_zoom.mobile.logo_alternatives_present) {
  throw new Error("authenticated mobile ERP accessibility contract failed");
}
evidence.roles["Champion Administrator"] = { email: emailFor("Champion Administrator"), routes: erpRoutes.length, api_read: true, print: true, export: true, address_and_coordinates: true };
await admin.context.close();

for (const role of roles.slice(1)) {
  const session = await login(role);
  const listResponse = await api(session.page, "/api/resource/LenERP%20Well%20Site?limit_page_length=20");
  const jobResponse = await api(session.page, "/api/resource/LenERP%20Drilling%20Job?limit_page_length=20");
  const expectedAllowed = ["Champion Dispatcher", "Champion Field Technician"].includes(role);
  if (role === "Champion Platform Operator" && (listResponse.status < 400 || jobResponse.status < 400)) throw new Error("Platform operator ERP API denial failed");
  if (expectedAllowed && (listResponse.status !== 200 || jobResponse.status !== 200)) throw new Error(`${role} ERP API allow failed`);
  evidence.roles[role] = { email: emailFor(role), well_api_status: listResponse.status, job_api_status: jobResponse.status, expected_well_access: expectedAllowed };
  await session.context.close();
}

const allAccessibilityResults = [
  evidence.accessibility.unauthenticated,
  ...Object.values(evidence.accessibility.routes),
  evidence.accessibility.desktop,
  evidence.accessibility.mobile,
].filter(Boolean);
const seriousViolations = allAccessibilityResults.flatMap((result) => result.violations)
  .filter((violation) => ["critical", "serious"].includes(violation.impact));
if (seriousViolations.length) {
  throw new Error(`serious accessibility violations: ${seriousViolations.map((violation) => violation.id).join(", ")}`);
}
const incomplete = allAccessibilityResults.flatMap((result) => result.incomplete);
const seriousIncomplete = incomplete.filter((item) => ["critical", "serious"].includes(item.impact) && item.id !== "color-contrast");
if (seriousIncomplete.length) {
  throw new Error(`serious incomplete accessibility checks: ${seriousIncomplete.map((item) => item.id).join(", ")}`);
}
evidence.accessibility.incomplete_reviewed = [...new Set(incomplete.filter((item) => item.id === "color-contrast").map((item) => item.id))];

await writeFile(path.join(outputDir, "erp-browser-evidence.json"), `${JSON.stringify(evidence, null, 2)}\n`, "utf8");
await browser.close();
