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

function safeUrl(raw) {
  const parsed = new URL(raw);
  return `${parsed.origin}${parsed.pathname}`;
}

function safeText(raw) {
  return raw
    .replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/(?:code|state|token|secret|password|cookie|authorization)[^<\s]*/gi, "[REDACTED]")
    .replace(/[A-Za-z0-9_-]{24,}/g, "[REDACTED]")
    .replace(/[\w.+-]+@[\w.-]+/g, "[REDACTED_EMAIL]")
    .replace(/\s+/g, " ")
    .slice(0, 1200);
}

async function assertReady(page, url) {
  const response = await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
  if (!response || response.status() >= 400) {
    const preview = response
      ? (await response.text().catch(() => ""))
          .replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi, " ")
          .replace(/<[^>]+>/g, " ")
          .replace(/(?:code|state|token|secret|password|cookie|authorization)[^<\s]*/gi, "[REDACTED]")
          .replace(/[A-Za-z0-9_-]{24,}/g, "[REDACTED]")
          .replace(/[\w.+-]+@[\w.-]+/g, "[REDACTED_EMAIL]")
          .replace(/\s+/g, " ")
          .slice(0, 800)
      : "";
    console.error(`identity route failure detail: ${safeText(preview)}`);
    throw new Error(`identity browser route failed: ${safeUrl(url)} (${response?.status()})`);
  }
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
  session_isolation: {},
};

// Start a transaction in one browser, then deliver its callback through a
// second browser that has the control-plane session but not the ERP nonce.
// The victim must be denied before any Frappe session is created.
const attackerContext = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
const attackerPage = await attackerContext.newPage();
const transactionUrl = `${erpBase}/api/method/lenerp_core.sso.begin?next_path=%2Fapp%2Fasset-maintenance`;
const transactionResponse = await attackerPage.goto(transactionUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
const transaction = {
  status: transactionResponse?.status() ?? 0,
  body: JSON.parse(await attackerPage.locator("body").innerText()),
};
if (transaction.status !== 200 || !transaction.body.authorization_url) throw new Error("ERP did not issue a browser-bound identity transaction");
const victimContext = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
await addIdentityCookie(victimContext);
const victimPage = await victimContext.newPage();
const victimResponse = await victimPage.goto(transaction.body.authorization_url, { waitUntil: "domcontentloaded", timeout: 60000 }).catch(() => null);
if (victimResponse && victimResponse.status() < 400) throw new Error("cross-browser callback was not rejected");
evidence.session_isolation = { attacker_transaction_issued: true, victim_callback_denied: true, no_victim_erp_session: !victimPage.url().includes("/app") };
await attackerPage.close();
await victimPage.close();
await attackerContext.close();
await victimContext.close();

const context = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
await addIdentityCookie(context);
const controlPage = await context.newPage();
await assertReady(controlPage, `${controlBase}/app/tenants/${manifest.tenant_id}`);
const openLink = controlPage.getByRole("link", { name: /^Open ERP for /i });
if (await openLink.count() !== 1) throw new Error("ready tenant page did not expose exactly one Open ERP action");
await controlPage.screenshot({ path: path.join(outputDir, "control-tenant-open-erp.png"), fullPage: true });
controlPage.on("response", async (response) => {
  if (response.url().includes("/app") || response.url().includes("sso") || response.url().includes("callback")) {
    console.error(`identity response ${response.status()} ${safeUrl(response.url())} location=${safeUrl(response.headers().location ?? response.url())}`);
    if (response.status() >= 400) {
      const body = await response.text().catch(() => "");
      const tokenStatus = body.match(/token exchange status (\d{3})/i)?.[1] ?? "unknown";
      console.error(`identity token exchange status: ${tokenStatus}`);
      console.error(`identity response detail ${response.status()}: ${safeText(body)}`);
    }
  }
});
await openLink.click();
await controlPage.waitForTimeout(1000);
console.error(`identity post-click URL ${safeUrl(controlPage.url())}`);
try {
  await controlPage.waitForURL(new RegExp(`^${erpBase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\/app`), { timeout: 60000 });
} catch {
  throw new Error(`control-to-erp callback did not land on ERP app: ${safeUrl(controlPage.url())}`);
}
evidence.control_to_erp = { final_url: new URL(controlPage.url()).pathname, no_second_password_prompt: true };
await controlPage.screenshot({ path: path.join(outputDir, "control-to-erp.png"), fullPage: true });

const directContext = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
await addIdentityCookie(directContext);
const directPage = await directContext.newPage();
await assertReady(directPage, `${erpBase}/app`);
if (!directPage.url().startsWith(`${erpBase}/app`)) throw new Error(`direct ERP visit did not land on ERP app: ${directPage.url()}`);
evidence.direct_erp = { final_url: new URL(directPage.url()).pathname, no_second_password_prompt: true };
await directPage.screenshot({ path: path.join(outputDir, "direct-erp.png"), fullPage: true });

await directPage.waitForTimeout(1500);
await assertReady(directPage, `${erpBase}/app/asset-maintenance`);
if (!directPage.url().includes("/app/asset-maintenance")) throw new Error(`direct ERP task path was not preserved: ${directPage.url()}`);
evidence.direct_erp.task_path = "/app/asset-maintenance";
let returnLink = directPage.locator("[data-lenerp-control-plane]");
if (await returnLink.count() === 0 || !(await returnLink.first().isVisible().catch(() => false))) {
  const toggles = directPage.locator(".dropdown-toggle, [data-toggle='dropdown'], [aria-haspopup='true']");
  for (let index = 0; index < Math.min(await toggles.count(), 8) && !(await returnLink.first().isVisible().catch(() => false)); index += 1) {
    await toggles.nth(index).click().catch(() => undefined);
  }
}
if (await returnLink.count() !== 1) throw new Error("ERP user navigation did not expose exactly one LenERP Control Plane link");
const returnHref = await returnLink.getAttribute("href");
if (!returnHref || !returnHref.startsWith(`${controlBase}/app/tenants/${manifest.tenant_id}`)) throw new Error("ERP return link was not bound to the synthetic tenant");
await Promise.all([
  directPage.waitForURL(new RegExp(`${controlBase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}/app/tenants/${manifest.tenant_id}`), { timeout: 60000 }),
  returnLink.evaluate((element) => element.click()),
]);
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
