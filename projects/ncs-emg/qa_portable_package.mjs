import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { fileURLToPath, pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const root = "C:\\Users\\uugur\\OneDrive\\Desktop\\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu";
const reportPath = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg\\portable-package-qa-report.json";
const manifest = JSON.parse(fs.readFileSync(path.join(root, "nonfizyolojik_69_sayfa_manifest.json"), "utf8"));

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
let runtimeErrors = [];
page.on("pageerror", error => runtimeErrors.push(`pageerror: ${error.message}`));
page.on("console", message => {
  if (message.type() === "error") runtimeErrors.push(`console: ${message.text()}`);
});

const failures = [];
const pages = [];

for (const item of manifest.sequence) {
  runtimeErrors = [];
  const absolute = path.join(root, item.file);
  const pageUrl = pathToFileURL(absolute).href;
  await page.goto(pageUrl, { waitUntil: "load", timeout: 20000 });
  await page.waitForTimeout(100);

  const initial = await page.evaluate(() => ({
    imageFailures: [...document.images]
      .filter(image => !image.complete || image.naturalWidth === 0)
      .map(image => image.getAttribute("src")),
    externalRefs: [...document.querySelectorAll("[src],[href]")]
      .map(element => element.getAttribute("src") || element.getAttribute("href"))
      .filter(Boolean)
      .filter(ref => /^https?:/i.test(ref)),
  }));

  if (item.type === "animation") {
    const sliders = page.locator('input[type="range"]');
    for (let index = 0; index < await sliders.count(); index++) {
      const slider = sliders.nth(index);
      const limits = await slider.evaluate(element => ({
        min: Number(element.min || 0),
        max: Number(element.max || 100),
      }));
      for (const value of [limits.min, (limits.min + limits.max) / 2, limits.max]) {
        await slider.evaluate((element, next) => {
          element.value = String(next);
          element.dispatchEvent(new Event("input", { bubbles: true }));
          element.dispatchEvent(new Event("change", { bubbles: true }));
        }, value);
        await page.waitForTimeout(15);
      }
    }

    const buttons = page.locator("button");
    for (let index = 0; index < await buttons.count(); index++) {
      const button = buttons.nth(index);
      if (await button.isVisible() && await button.isEnabled()) {
        await button.click({ timeout: 2000 });
        await page.waitForTimeout(25);
      }
    }
  }

  await page.waitForTimeout(80);
  const final = await page.evaluate(() => {
    const rootElement = document.documentElement;
    const shell = document.querySelector(".app,.slide");
    const shellRect = shell?.getBoundingClientRect();
    const nav = document.querySelector(".bottom-bar");
    const navRect = nav?.getBoundingClientRect();
    const refs = [...document.querySelectorAll("[src],[href]")]
      .map(element => element.getAttribute("src") || element.getAttribute("href"))
      .filter(Boolean);
    return {
      title: document.title,
      bodyOverflowX: rootElement.scrollWidth > rootElement.clientWidth + 1,
      bodyOverflowY: rootElement.scrollHeight > rootElement.clientHeight + 1,
      shellOverflowX: shell ? shell.scrollWidth > shell.clientWidth + 1 : false,
      shellOverflowY: shell ? shell.scrollHeight > shell.clientHeight + 1 : false,
      shellWithinViewport: shellRect
        ? shellRect.left >= -1 && shellRect.top >= -1
          && shellRect.right <= innerWidth + 1 && shellRect.bottom <= innerHeight + 1
        : false,
      navCount: document.querySelectorAll(".bottom-bar .fkey").length,
      navBottom: navRect ? Math.round(navRect.bottom) : null,
      imageFailures: [...document.images]
        .filter(image => !image.complete || image.naturalWidth === 0)
        .map(image => image.getAttribute("src")),
      externalRefs: refs.filter(ref => /^https?:/i.test(ref)),
      refs,
      visibleTextLength: (document.body.innerText || "").trim().length,
    };
  });

  const missingRefs = [];
  for (const ref of final.refs) {
    if (/^(?:https?:|data:|mailto:|javascript:|#)/i.test(ref)) continue;
    const resolved = new URL(ref, pageUrl);
    if (resolved.protocol === "file:") {
      const target = fileURLToPath(resolved);
      if (!fs.existsSync(target)) missingRefs.push(ref);
    }
  }

  const errors = [
    ...runtimeErrors,
    ...initial.imageFailures.map(ref => `initial missing image: ${ref}`),
    ...final.imageFailures.map(ref => `final missing image: ${ref}`),
    ...initial.externalRefs.map(ref => `initial external ref: ${ref}`),
    ...final.externalRefs.map(ref => `final external ref: ${ref}`),
    ...missingRefs.map(ref => `missing local ref: ${ref}`),
  ];
  if (final.bodyOverflowX || final.bodyOverflowY || final.shellOverflowX || final.shellOverflowY) {
    errors.push("layout overflow");
  }
  if (!final.shellWithinViewport) errors.push("presentation shell outside viewport");
  if (final.navCount !== 3 || final.navBottom === null || final.navBottom < 860) {
    errors.push("navigation bar mismatch");
  }
  if (item.type !== "topic_entry" && final.visibleTextLength < 80) {
    errors.push("unexpectedly sparse visible content");
  }
  const row = { ...item, errors, metrics: final };
  pages.push(row);
  if (errors.length) failures.push(row);
}

await page.goto(pathToFileURL(path.join(root, "SUNUMU_AC.html")).href, { waitUntil: "load" });
await page.waitForTimeout(150);
const starterReachedIndex = fileURLToPath(new URL(page.url())).toLowerCase()
  === path.join(root, "index.html").toLowerCase();
if (!starterReachedIndex) failures.push({ file: "SUNUMU_AC.html", errors: ["starter did not reach index.html"] });

await browser.close();

const rawHtml = manifest.sequence
  .map(item => fs.readFileSync(path.join(root, item.file), "utf8"))
  .join("\n");
const offlineChecks = {
  externalHttp: /https?:\/\//i.test(rawHtml),
  networkApi: /\b(?:fetch\s*\(|XMLHttpRequest|WebSocket\s*\()/i.test(rawHtml),
  absoluteWindowsPath: /[A-Za-z]:\\[^\s"'<>]+/.test(rawHtml),
};
for (const [name, failed] of Object.entries(offlineChecks)) {
  if (failed) failures.push({ file: "package", errors: [`offline check failed: ${name}`] });
}

const summary = {
  pages: manifest.sequence.length,
  explanations: pages.filter(row => row.type === "explanation").length,
  animations: pages.filter(row => row.type === "animation").length,
  topicEntries: pages.filter(row => row.type === "topic_entry").length,
  starterReachedIndex,
  offlineChecks,
  failures: failures.map(row => ({ number: row.number, file: row.file, errors: row.errors })),
};
fs.writeFileSync(reportPath, JSON.stringify({ summary, pages }, null, 2));
console.log(JSON.stringify(summary, null, 2));
if (failures.length) process.exit(1);
