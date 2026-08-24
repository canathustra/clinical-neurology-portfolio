import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\stimulus-artefakti\\animasyon-0-mekanizma.html";
const out = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run", "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
const errors = [];
page.on("pageerror", error => errors.push(`pageerror: ${error.message}`));
page.on("console", message => {
  if (message.type() === "error") errors.push(`console: ${message.text()}`);
});
await page.goto(pathToFileURL(live).href, { waitUntil: "load" });
await page.waitForTimeout(250);

async function capture(mode) {
  if (mode !== "clean") await page.click(`.mbtn[data-mode="${mode}"]`);
  await page.waitForTimeout(130);
  const state = await page.evaluate(() => ({
    active: document.querySelector(".mbtn.active")?.dataset.mode,
    distance: document.querySelector("#distanceOut")?.textContent?.trim(),
    amp: document.querySelector("#ampOut")?.textContent?.trim(),
    latency: document.querySelector("#latOut")?.textContent?.trim(),
    trueLatency: document.querySelector("#trueLatOut")?.textContent?.trim(),
    note: document.querySelector("#mechNote")?.textContent?.trim(),
    claim: document.querySelector("#scopeClaim")?.textContent?.trim(),
  }));
  await page.screenshot({ path: path.join(out, `concept05_${mode}.png`) });
  return state;
}

const clean = await capture("clean");
const negative = await capture("negative");
const positive = await capture("positive");
const short = await capture("short");
await page.click("#shockBtn");
await page.waitForTimeout(90);
const earlyField = await page.locator(".field-path.live").count();
await page.waitForTimeout(620);
const volleyX = Number(await page.locator("#volley").getAttribute("cx"));

await page.locator("#distanceSlider").evaluate(element => {
  element.value = "10";
  element.dispatchEvent(new Event("input", { bubbles: true }));
});
await page.waitForTimeout(100);
const custom = await page.evaluate(() => ({
  active: document.querySelector(".mbtn.active")?.dataset.mode,
  distance: document.querySelector("#distanceOut")?.textContent?.trim(),
  trueLatency: document.querySelector("#trueLatOut")?.textContent?.trim(),
  amp: document.querySelector("#ampOut")?.textContent?.trim(),
}));

const metrics = await page.evaluate(() => {
  const root = document.documentElement;
  const app = document.querySelector(".app");
  const nav = document.querySelector(".bottom-bar");
  const rect = nav?.getBoundingClientRect();
  const canvas = document.querySelector("canvas");
  return {
    overflowX: root.scrollWidth > root.clientWidth + 1,
    overflowY: root.scrollHeight > root.clientHeight + 1,
    appOverflowX: app.scrollWidth > app.clientWidth + 1,
    appOverflowY: app.scrollHeight > app.clientHeight + 1,
    navCount: document.querySelectorAll(".bottom-bar .fkey").length,
    navBottom: rect ? Math.round(rect.bottom) : null,
    canvasWidth: canvas?.width || 0,
    canvasHeight: canvas?.height || 0,
    imageFailures: [...document.images].filter(img => !img.complete || !img.naturalWidth).length,
    modeButtons: document.querySelectorAll(".mbtn").length,
    activeButtons: document.querySelectorAll(".mbtn.active").length,
  };
});

const failures = [];
if (errors.length) failures.push(...errors);
if (clean.amp !== "38 µV" || clean.latency !== "2.0 ms") failures.push("clean values");
if (negative.amp !== "29 µV" || negative.latency !== "2.1 ms") failures.push("negative Figure 8.11 values");
if (positive.amp !== "45 µV" || positive.latency !== "1.9 ms") failures.push("positive Figure 8.11 values");
if (short.distance !== "7 cm" || short.active !== "short" || !short.note.includes("Kısa mesafe")) failures.push("short distance");
if (earlyField !== 2 || volleyX <= 620 || volleyX >= 1465) failures.push("arrival animation");
if (custom.distance !== "10 cm" || custom.active !== "negative" || custom.trueLatency !== "1.4 ms") failures.push("distance slider");
if (metrics.overflowX || metrics.overflowY || metrics.appOverflowX || metrics.appOverflowY) failures.push("overflow");
if (metrics.navCount !== 3 || metrics.navBottom === null || metrics.navBottom < 860) failures.push("navigation layout");
if (metrics.canvasWidth < 700 || metrics.canvasHeight < 180 || metrics.imageFailures || metrics.modeButtons !== 4 || metrics.activeButtons !== 1) failures.push("visual assets");

console.log(JSON.stringify({ failures, states: { clean, negative, positive, short, custom, earlyField, volleyX }, metrics }, null, 2));
await browser.close();
if (failures.length) process.exitCode = 1;
