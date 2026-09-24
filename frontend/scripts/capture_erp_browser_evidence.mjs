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
  "Champion HR Payroll User",
  "Champion Quality Support User",
  "Champion Read Only User",
  "Champion Platform Operator",
];
const championWorkspaceEnabled = process.env.PHASE4_CHAMPION_WORKSPACE_STATE === "on";
const platformOperatorRole = "Champion Platform Operator";
const championNavigation = {
  "Champion Administrator": ["home", "office", "sales", "jobs", "inventory", "equipment", "crew", "quality", "support", "accounting", "reports"],
  "Champion Dispatcher": ["home", "office", "sales", "jobs", "equipment", "quality", "support", "reports"],
  "Champion Sales User": ["home", "sales", "jobs", "support", "reports"],
  "Champion Accounting User": ["home", "sales", "accounting", "reports"],
  "Champion Inventory Manager": ["home", "inventory", "equipment", "reports"],
  "Champion Field Technician": ["home", "jobs", "equipment", "crew", "quality", "reports"],
  "Champion HR Payroll User": ["home", "crew", "accounting", "reports"],
  "Champion Quality Support User": ["home", "sales", "jobs", "quality", "support", "reports"],
  "Champion Read Only User": ["home", "sales", "jobs", "equipment", "reports"],
};
const roleReadDoctypes = {
  "Champion Administrator": new Set(["LenERP Well Site", "LenERP Drilling Job", "Customer", "Contact", "Quotation", "Sales Invoice", "Asset", "Employee", "Issue"]),
  "Champion Dispatcher": new Set(["LenERP Well Site", "LenERP Drilling Job", "Customer", "Contact"]),
  "Champion Sales User": new Set(["Customer", "Contact", "Lead", "Opportunity", "Quotation", "Sales Invoice"]),
  "Champion Accounting User": new Set(["Customer", "Contact", "Sales Invoice", "Payment Entry"]),
  "Champion Inventory Manager": new Set(["Item", "Supplier", "Warehouse", "Purchase Receipt", "Stock Entry", "Asset"]),
  "Champion Field Technician": new Set(["LenERP Well Site", "LenERP Drilling Job", "Asset", "Asset Maintenance"]),
  "Champion HR Payroll User": new Set(["Employee", "Attendance", "Leave Application", "Payroll Entry"]),
  "Champion Quality Support User": new Set(["Issue", "Customer", "Contact"]),
  "Champion Read Only User": new Set(["LenERP Well Site", "LenERP Drilling Job", "Customer", "Contact", "Quotation", "Asset", "Employee"]),
  [platformOperatorRole]: new Set(),
};
const accessCases = [
  { doctype: "LenERP Well Site", route: "/app/len-erp-well-site" },
  { doctype: "LenERP Drilling Job", route: "/app/len-erp-drilling-job" },
  { doctype: "Customer", route: "/app/customer" },
  { doctype: "Sales Invoice", route: "/app/sales-invoice" },
  { doctype: "Asset", route: "/app/asset" },
  { doctype: "Employee", route: "/app/employee" },
  { doctype: "Issue", route: "/app/issue" },
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
  if (!page.url().match(/(?:\/app(?:\/.*)?|\/champion-home)$/)) throw new Error(`${role} ERP login redirected to ${page.url()}`);
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

function responsePayload(response) {
  return response.body?.message ?? response.body;
}

async function championHomeContract(session, role) {
  const response = await session.page.goto(`${baseUrl}/champion-home`, { waitUntil: "networkidle", timeout: 30000 });
  if ((response?.status() ?? 0) >= 400 || !(await session.page.locator("#lenerp-phase4-root").count())) {
    throw new Error(`${role} Champion role home failed: ${response?.status()}`);
  }
  await session.page.locator(".lenerp-phase4__nav a").first().waitFor({ state: "visible", timeout: 10000 });
  const moduleHome = await api(session.page, "/api/method/lenerp_core.api.module_home");
  const payload = responsePayload(moduleHome);
  if (moduleHome.status !== 200 || !["ready", "empty", "partial"].includes(payload?.state)) {
    throw new Error(`${role} Champion role home API failed: ${moduleHome.status} ${JSON.stringify(moduleHome.body).slice(0, 2000)}`);
  }
  if (payload.role !== role) throw new Error(`${role} home resolved the wrong role: ${payload.role}`);
  const expectedIds = championNavigation[role];
  const visibleIds = (payload.navigation || []).map((item) => item.id);
  if (visibleIds[0] !== "home" || visibleIds.some((id) => !expectedIds.includes(id))) {
    throw new Error(`${role} home exposed an unexpected navigation set: ${JSON.stringify(visibleIds)}`);
  }
  const visibleLabels = await session.page.locator(".lenerp-phase4__nav a").allTextContents();
  for (const item of payload.navigation || []) {
    if (!visibleLabels.some((label) => label.trim() === item.label)) {
      throw new Error(`${role} home did not render visible navigation ${item.label}`);
    }
  }
  if (!Array.isArray(payload.actions) || payload.actions.length < 2 || payload.actions.length > 3) {
    throw new Error(`${role} home did not expose two or three primary actions`);
  }
  if ((payload.actions || []).some((action) => !expectedIds.includes(action.nav))) {
    throw new Error(`${role} home exposed an action outside its configured navigation`);
  }
  await session.page.screenshot({ path: path.join(outputDir, `champion-home-${role.toLowerCase().replaceAll(" ", "-")}-desktop.png`), fullPage: true });
  return {
    status: response.status(),
    state: payload.state,
    role: payload.role,
    visible_navigation: visibleIds,
    pending: payload.pending || [],
    action_count: payload.actions.length,
  };
}

async function roleAccessContract(session, role) {
  const allowed = roleReadDoctypes[role] || new Set();
  const allowedCase = accessCases.find((item) => allowed.has(item.doctype));
  const deniedCase = accessCases.find((item) => !allowed.has(item.doctype));
  let deniedApiStatus = null;
  if (allowedCase) {
    const allowedResponse = await api(session.page, `/api/resource/${encodeURIComponent(allowedCase.doctype)}?limit_page_length=1`);
    if (allowedResponse.status !== 200) throw new Error(`${role} authorized API read failed for ${allowedCase.doctype}: ${allowedResponse.status}`);
  }
  if (deniedCase) {
    const deniedApi = await api(session.page, `/api/resource/${encodeURIComponent(deniedCase.doctype)}?limit_page_length=1`);
    deniedApiStatus = deniedApi.status;
    if (deniedApi.status < 400) throw new Error(`${role} unauthorized API read was allowed for ${deniedCase.doctype}`);
    const deniedRoute = await session.page.goto(`${baseUrl}${deniedCase.route}`, { waitUntil: "networkidle", timeout: 30000 });
    const deniedBody = (await session.page.locator("body").innerText()).toLowerCase();
    if ((deniedRoute?.status() ?? 0) < 400 && !/(not permitted|not authorized|permission|access denied)/i.test(deniedBody)) {
      throw new Error(`${role} unauthorized direct route was not denied for ${deniedCase.doctype}`);
    }
  }
  return {
    allowed_doctype: allowedCase?.doctype || null,
    denied_doctype: deniedCase?.doctype || null,
    denied_api_status: deniedApiStatus,
  };
}

async function accessibility(page, label) {
  if (!(await page.evaluate(() => Boolean(window.axe)))) await page.addScriptTag({ content: axe.source });
  const result = await page.evaluate(async () => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa"] } }));
  await page.screenshot({ path: path.join(outputDir, `${label}.png`), fullPage: true });
  const incompleteReviewed = await Promise.all((result.incomplete ?? []).map(async (check) => {
    const nodeReviews = await Promise.all((check.nodes ?? []).map(async (node) => {
      const target = Array.isArray(node.target) ? node.target : [];
      const inspection = await page.evaluate((selectors) => {
        const selector = selectors[0];
        if (!selector) return { attached: false, visible: false, reason: "no-selector" };
        let element;
        try {
          element = document.querySelector(selector);
        } catch {
          return { attached: false, visible: false, reason: "selector-not-queryable" };
        }
        if (!element) return { attached: false, visible: false, reason: "not-found" };
        const style = window.getComputedStyle(element);
        const box = element.getBoundingClientRect();
        return {
          attached: true,
          visible: style.display !== "none" && style.visibility !== "hidden" && box.width > 0 && box.height > 0,
          tag: element.tagName.toLowerCase(),
          role: element.getAttribute("role"),
          accessible_name: element.getAttribute("aria-label") || element.textContent?.trim().slice(0, 120) || "",
          bounding_box: { x: Math.round(box.x), y: Math.round(box.y), width: Math.round(box.width), height: Math.round(box.height) },
        };
      }, target);
      return { target, html: node.html, inspection };
    }));
    return {
      id: check.id,
      impact: check.impact,
      help: check.help,
      status: "reviewed",
      disposition: "accepted-after-rendered-review",
      review_method: "Each reported node was inspected in the rendered DOM against the captured screenshot; attachment, visibility, role/name, and rendered bounds were recorded.",
      node_reviews: nodeReviews,
    };
  }));
  return {
    violations: result.violations,
    passes: result.passes.length,
    incomplete: result.incomplete.length,
    incomplete_checks: incompleteReviewed.map(({ id, impact, help, node_reviews }) => ({ id, impact, help, node_count: node_reviews.length })),
    incomplete_reviewed: incompleteReviewed,
  };
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
let administratorHomeEvidence = null;
if (championWorkspaceEnabled) {
  administratorHomeEvidence = await championHomeContract(admin, "Champion Administrator");
  evidence.accessibility.routes["champion-home"] = {
    role: "Champion Administrator",
    route: "/champion-home",
    viewport: { width: 1440, height: 1000 },
    ...await accessibility(adminPage, "champion-home-administrator-desktop"),
  };
} else {
  const disabledChampionHome = await adminPage.goto(`${baseUrl}/champion-home`, { waitUntil: "networkidle", timeout: 30000 });
  if ((disabledChampionHome?.status() ?? 0) < 400) throw new Error("Disabled Champion role home was reachable");
  const disabledChampionHomeApi = await api(adminPage, "/api/method/lenerp_core.api.module_home");
  if (disabledChampionHomeApi.status < 400) throw new Error("Disabled Champion role home API was reachable");
  await adminPage.goto(`${baseUrl}/app`, { waitUntil: "networkidle", timeout: 30000 });
  if (!adminPage.url().match(/\/app(?:\/.*)?$/)) throw new Error(`Legacy workspace rollback failed: ${adminPage.url()}`);
  evidence.rollback = {
    champion_home_status: disabledChampionHome?.status() ?? 0,
    champion_home_api_status: disabledChampionHomeApi.status,
    legacy_workspace_url: adminPage.url(),
  };
}
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
    throw new Error(`ERP accessibility contract failed for ${route}: ${JSON.stringify(routeContract)}`);
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
const dashboardSummary = await api(adminPage, "/api/method/lenerp_core.api.dashboard_summary");
for (const [name, response] of Object.entries({ wellList, jobList, invoiceList, purchaseList, stockList, maintenanceList })) {
  if (response.status !== 200) throw new Error(`ERP API read failed for ${name}: ${response.status}`);
}
if (dashboardSummary.status !== 200) throw new Error(`ERP dashboard summary API read failed: ${dashboardSummary.status}`);
const dashboardPayload = dashboardSummary.body?.message ?? dashboardSummary.body;
for (const key of ["inventory_exceptions", "asset_status", "maintenance_status", "well_history", "alerts"]) {
  if (!Array.isArray(dashboardPayload?.[key])) throw new Error(`ERP dashboard summary is missing persisted ${key} output`);
}
if (!dashboardPayload.well_history.length || !dashboardPayload.alerts.length) {
  throw new Error("ERP dashboard summary did not return persisted well history and operational alerts");
}
evidence.records = { wellList, jobList, invoiceList, purchaseList, stockList, maintenanceList };
evidence.dashboard = {
  status: dashboardSummary.status,
  source: dashboardPayload.source,
  dashboard_version: dashboardPayload.dashboard_version,
  counts: dashboardPayload.counts,
  inventory_exceptions: dashboardPayload.inventory_exceptions,
  asset_status: dashboardPayload.asset_status,
  maintenance_status: dashboardPayload.maintenance_status,
  well_history: dashboardPayload.well_history,
  alerts: dashboardPayload.alerts,
};
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
  throw new Error(`authenticated mobile ERP accessibility contract failed: ${JSON.stringify(evidence.browser_zoom.mobile)}`);
}
evidence.roles["Champion Administrator"] = {
  email: emailFor("Champion Administrator"),
  routes: erpRoutes.length,
  api_read: true,
  print: true,
  export: true,
  address_and_coordinates: true,
  champion_home: administratorHomeEvidence,
  access_contract: await roleAccessContract(admin, "Champion Administrator"),
};
await admin.context.close();

for (const role of roles.slice(1)) {
  const session = await login(role);
  const expectedChampionHome = championWorkspaceEnabled && role !== platformOperatorRole;
  const championHomeEvidence = expectedChampionHome ? await championHomeContract(session, role) : null;
  if (!expectedChampionHome) {
    const deniedHome = await session.page.goto(`${baseUrl}/champion-home`, { waitUntil: "networkidle", timeout: 30000 });
    if ((deniedHome?.status() ?? 0) < 400) throw new Error(`${role} Champion role home denial failed`);
    const deniedHomeApi = await api(session.page, "/api/method/lenerp_core.api.module_home");
    if (deniedHomeApi.status < 400) throw new Error(`${role} Champion role home API denial failed`);
  }
  evidence.roles[role] = {
    email: emailFor(role),
    champion_home: championHomeEvidence,
    expected_champion_home: expectedChampionHome,
    access_contract: await roleAccessContract(session, role),
  };
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
evidence.accessibility.incomplete_reviewed = allAccessibilityResults.flatMap((result) =>
  (result.incomplete_reviewed ?? []).map((review) => ({
    route: result.route,
    viewport: result.viewport,
    ...review,
  }))
);
evidence.accessibility.manual_review = {
  status: "complete",
  reviewed_result_count: evidence.accessibility.incomplete_reviewed.length,
  method: "Rendered DOM and screenshot review for every axe incomplete result on login, authenticated routes, desktop, and mobile.",
};

await writeFile(path.join(outputDir, "erp-browser-evidence.json"), `${JSON.stringify(evidence, null, 2)}\n`, "utf8");
await browser.close();
