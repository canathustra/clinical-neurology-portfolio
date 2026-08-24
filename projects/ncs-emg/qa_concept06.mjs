import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\stimulus-artefakti\\animasyon-2-artefakt-azaltma.html";
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
await page.screenshot({ path: path.join(out, "concept06_initial.png") });

const keys = ["ground", "impedance", "coax", "position", "intensity", "anode", "distance", "cables"];
const states = [];
for (const key of keys) {
  await page.locator(`.item[data-fix="${key}"] input`).check();
  await page.waitForTimeout(70);
  states.push(await page.evaluate(() => ({
    checked: document.querySelectorAll(".item input:checked").length,
    note: document.querySelector("#stepNote")?.textContent?.trim(),
    volume: document.querySelector("#volumeOut")?.textContent?.trim(),
    diff: document.querySelector("#diffOut")?.textContent?.trim(),
    induction: document.querySelector("#indOut")?.textContent?.trim(),
    margin: document.querySelector("#marginOut")?.textContent?.trim(),
    score: document.querySelector("#scoreOut")?.textContent?.trim(),
    readout: document.querySelector("#scopeReadout")?.textContent?.trim(),
  })));
}
await page.screenshot({ path: path.join(out, "concept06_all_applied.png") });
await page.click("#resetBtn");
const resetChecked = await page.locator(".item input:checked").count();
await page.click("#allBtn");
const allChecked = await page.locator(".item input:checked").count();

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
    items: document.querySelectorAll(".item").length,
    numberedItems: document.querySelectorAll(".item .num").length,
  };
});

const failures = [];
if (errors.length) failures.push(...errors);
if (states.length !== 8 || states.some((state, i) => state.checked !== i + 1)) failures.push("ordered checklist");
if (states[0].volume !== "62%" || states[0].diff !== "100%" || states[0].induction !== "100%") failures.push("ground specificity");
if (states[1].diff !== "35%") failures.push("impedance specificity");
if (states[2].induction !== "45%") failures.push("coax specificity");
if (!states[4].note.includes("supramaksimal") || !states[4].note.includes("submaksimal")) failures.push("intensity warning");
if (!states[5].note.includes("sonraki animasyondadır")) failures.push("anode preview boundary");
if (states[6].margin !== "geniş") failures.push("distance margin");
if (states[7].score !== "0/8 eksik" || states[7].readout !== "DSAP başlangıcı net") failures.push("completed result");
if (resetChecked !== 0 || allChecked !== 8) failures.push("bulk controls");
if (metrics.overflowX || metrics.overflowY || metrics.appOverflowX || metrics.appOverflowY) failures.push("overflow");
if (metrics.navCount !== 3 || metrics.navBottom === null || metrics.navBottom < 860) failures.push("navigation layout");
if (metrics.canvasWidth < 700 || metrics.canvasHeight < 400 || metrics.imageFailures || metrics.items !== 8 || metrics.numberedItems !== 8) failures.push("visual assets");

console.log(JSON.stringify({ failures, states, resetChecked, allChecked, metrics }, null, 2));
await browser.close();
if (failures.length) process.exitCode = 1;
