import { chromium } from "@playwright/test";
import axe from "axe-core";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const manifest = JSON.parse(await readFile(process.env.PHASE3_IDENTITY_MANIFEST, "utf8"));
const outputDir = process.env.OUTPUT_DIR ?? "phase3-identity-evidence";
const controlBase = manifest.control_base_url.replace(/\/$/, "");
const erpBase = manifest.erp_base_url.replace(/\/$/, "");
const token = (await readFile(manifest.champion_token_file, "utf8")).trim();
await mkdir(outputDir, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: process.env.BROWSER_EXECUTABLE_PATH || undefined,
  args: [
    "--ignore-certificate-errors",
    `--host-resolver-rules=MAP staging.example.test 127.0.0.1,MAP erp-staging.example.test 127.0.0.1`,
  ],
});

async function addIdentityCookie(context) {
  await context.addCookies([{ name: "crm-auth-token", value: token, url: `${controlBase}/` }]);
}

async function accessibility(page) {
  await page.evaluate(axe.source);
  const result = await page.evaluate(async () => window.axe.run(document, { resultTypes: ["violations"] }));
  return { violations: result.violations.map((item) => ({ id: item.id, impact: item.impact, nodes: item.nodes.length })) };
}

async function assertReady(page, url) {
  const response = await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
  if (!response || response.status() >= 400) throw new Error(`identity browser route failed: ${url} (${response?.status()})`);
  await page.locator("body").waitFor({ state: "attached", timeout: 10000 });
}

const evidence = {
  synthetic: true,
  tenant_id: manifest.tenant_id,
  organization_id: manifest.organization_id,
  control_to_erp: {},
  direct_erp: {},
  erp_to_control: {},
  responsive: {},
};

const context = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
await addIdentityCookie(context);
const controlPage = await context.newPage();
await assertReady(controlPage, `${controlBase}/app/tenants/${manifest.tenant_id}`);
const openLink = controlPage.getByRole("link", { name: /^Open ERP for /i });
if (await openLink.count() !== 1) throw new Error("ready tenant page did not expose exactly one Open ERP action");
await controlPage.screenshot({ path: path.join(outputDir, "control-tenant-open-erp.png"), fullPage: true });
await openLink.click();
await controlPage.waitForURL(new RegExp(`^${erpBase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\/app`), { timeout: 60000 });
evidence.control_to_erp = { final_url: new URL(controlPage.url()).pathname, no_second_password_prompt: true };
await controlPage.screenshot({ path: path.join(outputDir, "control-to-erp.png"), fullPage: true });

const directContext = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
await addIdentityCookie(directContext);
const directPage = await directContext.newPage();
await assertReady(directPage, `${erpBase}/lenerp-sso?next_path=%2Fapp`);
if (!directPage.url().startsWith(`${erpBase}/app`)) throw new Error(`direct ERP visit did not land on ERP app: ${directPage.url()}`);
evidence.direct_erp = { final_url: new URL(directPage.url()).pathname, no_second_password_prompt: true };
await directPage.screenshot({ path: path.join(outputDir, "direct-erp.png"), fullPage: true });

await directPage.waitForTimeout(1500);
let returnLink = directPage.locator("[data-lenerp-control-plane]");
if (await returnLink.count() === 0) {
  const toggles = directPage.locator(".dropdown-toggle, [data-toggle='dropdown'], [aria-haspopup='true']");
  for (let index = 0; index < Math.min(await toggles.count(), 8) && await returnLink.count() === 0; index += 1) {
    await toggles.nth(index).click().catch(() => undefined);
  }
}
if (await returnLink.count() !== 1) throw new Error("ERP user navigation did not expose the LenERP Control Plane link");
await Promise.all([directPage.waitForURL(new RegExp(`${controlBase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}/app/tenants/${manifest.tenant_id}`), { timeout: 60000 }), returnLink.click()]);
evidence.erp_to_control = { final_url: new URL(directPage.url()).pathname, exact_tenant_return: true };
await directPage.screenshot({ path: path.join(outputDir, "erp-to-control.png"), fullPage: true });

await directPage.setViewportSize({ width: 390, height: 844 });
await assertReady(directPage, `${erpBase}/app`);
const responsive = await directPage.evaluate(() => ({ viewport_width: window.innerWidth, scroll_width: document.documentElement.scrollWidth, horizontal_overflow: document.documentElement.scrollWidth > window.innerWidth + 1 }));
if (responsive.horizontal_overflow) throw new Error(`identity ERP mobile route overflows horizontally: ${JSON.stringify(responsive)}`);
evidence.responsive = { ...responsive, accessibility: await accessibility(directPage) };
await directPage.screenshot({ path: path.join(outputDir, "erp-mobile.png"), fullPage: true });

await controlPage.close();
await directPage.close();
await directContext.close();
await context.close();
await browser.close();
await writeFile(path.join(outputDir, "phase3-identity-browser-evidence.json"), `${JSON.stringify(evidence, null, 2)}\n`, "utf8");
