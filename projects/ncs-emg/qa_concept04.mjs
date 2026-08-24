import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\elektronik-ortalama\\animasyon-1-ortalama.html";
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

async function state(label) {
  const values = await page.evaluate(() => ({
    n: document.querySelector("#nOut")?.textContent?.trim(),
    rms: document.querySelector("#rmsOut")?.textContent?.trim(),
    theory: document.querySelector("#theoryOut")?.textContent?.trim(),
    snr: document.querySelector("#snrOut")?.textContent?.trim(),
    note: document.querySelector("#mechNote")?.textContent?.trim(),
  }));
  await page.screenshot({ path: path.join(out, `concept04_${label}.png`) });
  return values;
}

const n1 = await state("n01");
await page.click("#addBtn");
await page.waitForTimeout(80);
const n2 = await page.locator("#nOut").textContent();
await page.click("#presetBtn");
await page.waitForTimeout(120);
const n10 = await state("n10");
await page.locator("#nSlider").evaluate(element => {
  element.value = "32";
  element.dispatchEvent(new Event("input", { bubbles: true }));
});
await page.waitForTimeout(120);
const n32 = await state("n32");
await page.click("#resetBtn");
const resetN = await page.locator("#nOut").textContent();
await page.click("#autoBtn");
await page.waitForTimeout(700);
await page.click("#autoBtn");
const autoN = Number(await page.locator("#nOut").textContent());

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
    buttonCount: document.querySelectorAll("button").length,
  };
});

const failures = [];
if (errors.length) failures.push(...errors);
if (n1.n !== "1" || n2.trim() !== "2" || n10.n !== "10" || n32.n !== "32" || resetN.trim() !== "1") failures.push("N controls");
if (n10.theory !== "3.8 µV" || n10.snr !== "3.16×") failures.push("N=10 theory");
if (!n10.note.includes("Şekil 8.10")) failures.push("N=10 explanation");
if (!n32.note.includes("1/√N")) failures.push("diminishing returns explanation");
if (autoN <= 1) failures.push("automatic averaging");
if (metrics.overflowX || metrics.overflowY || metrics.appOverflowX || metrics.appOverflowY) failures.push("overflow");
if (metrics.navCount !== 3 || metrics.navBottom === null || metrics.navBottom < 860) failures.push("navigation layout");
if (metrics.canvasWidth < 800 || metrics.canvasHeight < 400 || metrics.imageFailures || metrics.buttonCount !== 4) failures.push("visual assets");

console.log(JSON.stringify({ failures, states: { n1, n2: n2.trim(), n10, n32, resetN: resetN.trim(), autoN }, metrics }, null, 2));
await browser.close();
if (failures.length) process.exitCode = 1;
