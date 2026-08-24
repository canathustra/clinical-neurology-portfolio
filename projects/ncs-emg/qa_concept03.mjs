import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const liveRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations";
const outRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const files = [
  "filtreler\\animasyon-0-filtre-spektrumu.html",
  "filtreler\\animasyon-1-gecirgen-bant.html",
  "filtreler\\animasyon-2-filtre-odunlesimi.html",
];

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run", "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
const report = [];

for (let i = 0; i < files.length; i++) {
  const errors = [];
  const onPageError = error => errors.push(`pageerror: ${error.message}`);
  const onConsole = message => {
    if (message.type() === "error") errors.push(`console: ${message.text()}`);
  };
  page.on("pageerror", onPageError);
  page.on("console", onConsole);
  await page.goto(pathToFileURL(path.join(liveRoot, files[i])).href, { waitUntil: "load" });
  await page.waitForTimeout(250);
  const defaultScreenshot = `concept03_${i + 1}_default.png`;
  await page.screenshot({ path: path.join(outRoot, defaultScreenshot) });

  const buttons = page.locator(".mbtn");
  const buttonCount = await buttons.count();
  const states = [];
  for (let b = 0; b < buttonCount; b++) {
    await buttons.nth(b).click();
    await page.waitForTimeout(80);
    states.push(await page.evaluate(() => ({
      active: document.querySelector(".mbtn.active")?.textContent?.trim() || "",
      stats: [...document.querySelectorAll(".stat-row")].map(row => row.textContent.trim()),
      note: document.querySelector("#mechNote")?.textContent?.trim() || "",
    })));
  }

  const sliders = page.locator('input[type="range"]');
  const sliderCount = await sliders.count();
  for (let s = 0; s < sliderCount; s++) {
    const slider = sliders.nth(s);
    const min = Number(await slider.getAttribute("min") || 0);
    const max = Number(await slider.getAttribute("max") || 100);
    await slider.evaluate((element, value) => {
      element.value = String(value);
      element.dispatchEvent(new Event("input", { bubbles: true }));
      element.dispatchEvent(new Event("change", { bubbles: true }));
    }, min + 0.72 * (max - min));
  }
  await page.waitForTimeout(100);

  const metrics = await page.evaluate(() => {
    const root = document.documentElement;
    const shell = document.querySelector(".app,.slide");
    const nav = document.querySelector(".bottom-bar");
    const navRect = nav?.getBoundingClientRect();
    return {
      overflowX: root.scrollWidth > root.clientWidth + 1,
      overflowY: root.scrollHeight > root.clientHeight + 1,
      shellOverflowX: shell ? shell.scrollWidth > shell.clientWidth + 1 : false,
      shellOverflowY: shell ? shell.scrollHeight > shell.clientHeight + 1 : false,
      navCount: document.querySelectorAll(".bottom-bar .fkey").length,
      navBottom: navRect ? Math.round(navRect.bottom) : null,
      buttonCount: document.querySelectorAll(".mbtn").length,
      activeCount: document.querySelectorAll(".mbtn.active").length,
      sliderCount: document.querySelectorAll('input[type="range"]').length,
      canvasCount: document.querySelectorAll("canvas").length,
      imageFailures: [...document.images].filter(img => !img.complete || !img.naturalWidth).length,
      textLength: (document.body.innerText || "").trim().length,
    };
  });
  const screenshot = `concept03_${i + 1}_interacted.png`;
  await page.screenshot({ path: path.join(outRoot, screenshot) });
  report.push({ file: files[i], errors, states, metrics, defaultScreenshot, screenshot });
  page.off("pageerror", onPageError);
  page.off("console", onConsole);
}

await browser.close();
const failures = report.filter(row =>
  row.errors.length ||
  row.metrics.overflowX ||
  row.metrics.overflowY ||
  row.metrics.shellOverflowX ||
  row.metrics.shellOverflowY ||
  row.metrics.navCount !== 3 ||
  row.metrics.navBottom === null ||
  row.metrics.navBottom < 860 ||
  row.metrics.buttonCount < 3 ||
  row.metrics.activeCount > 1 ||
  row.metrics.canvasCount < 1 ||
  row.metrics.imageFailures ||
  row.metrics.textLength < 80
);
console.log(JSON.stringify({ pages: report.length, failures, report }, null, 2));
if (failures.length) process.exitCode = 1;
