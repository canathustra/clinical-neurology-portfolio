import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const liveRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations";
const outRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg\\qa_book_audit_2026-07-30";
fs.mkdirSync(outRoot, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run", "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
const errors = [];
page.on("pageerror", e => errors.push(e.message));

async function open(rel) {
  await page.goto(pathToFileURL(path.join(liveRoot, rel)).href, { waitUntil: "load" });
  await page.waitForTimeout(250);
}
async function shot(name) {
  await page.screenshot({ path: path.join(outRoot, name) });
}

const report = {};

await open("elektronik-ortalama/animasyon-1-ortalama.html");
report.averaging = await page.evaluate(() => ({
  preOnset: dsap(2.99),
  atOnset: dsap(3.0),
  postOnset: dsap(3.12),
}));
await page.locator("#presetBtn").click();
await page.waitForTimeout(150);
await shot("01-averaging-causal-onset.png");

await open("kostimulasyon/animasyon-0-akim-yayilimi.html");
report.costimInitial = await page.evaluate(() => window.__costimCurrentState);
await page.locator("#highBtn").click();
await page.locator("#stimBtn").click();
await page.waitForTimeout(1800);
report.costimAfter = await page.evaluate(() => window.__costimCurrentState);
await shot("02-costim-two-independent-acquisitions.png");

await open("ekstremite-morfoloji/animasyon-1-pozisyon-tutarliligi.html");
await page.evaluate(() => {
  const slider = document.querySelector("#mismatch");
  slider.value = "100";
  slider.dispatchEvent(new Event("input", { bubbles: true }));
  slider.dispatchEvent(new Event("change", { bubbles: true }));
});
await page.waitForTimeout(150);
report.morphology = await page.evaluate(() => {
  const p = { lat: 3, amp: 1, shoulder: 0 };
  return {
    preOnset: cmap(2.99, p),
    atOnset: cmap(3.0, p),
    postOnset: cmap(3.18, p),
    state: window.__positionConsistencyState,
  };
});
await shot("03-position-morphology-causal-onset.png");

await open("sweep-sensitivite/animasyon-1-sensitivite.html");
await page.locator('button[data-scale=".1"]').click();
await page.waitForTimeout(150);
report.sensitivity = await page.evaluate(() => ({
  preOnset: signal(2.89),
  atOnset: signal(2.90),
  postOnset: signal(3.12),
  state: window.__sensitivityLatencyState,
}));
await shot("04-sensitivity-100uv.png");

await open("sweep-sensitivite/animasyon-2-sweep-hizi.html");
await page.locator('button[data-sweep=".8"]').click();
await page.waitForTimeout(150);
report.sweep = await page.evaluate(() => ({
  preOnset: signal(2.89),
  atOnset: signal(2.90),
  postOnset: signal(3.12),
  state: window.__sweepLatencyState,
}));
await shot("05-sweep-08ms.png");

await browser.close();

const checks = {
  noPageErrors: errors.length === 0,
  averagingCausal: report.averaging.preOnset === 0 && report.averaging.atOnset === 0 && Math.abs(report.averaging.postOnset) > 0,
  morphologyCausal: report.morphology.preOnset === 0 && report.morphology.atOnset === 0 && Math.abs(report.morphology.postOnset) > 0,
  costimHiddenBeforeClick: report.costimInitial?.traceVisible === false,
  costimSeparate: report.costimAfter?.propagationDirection === "two_independent_stimulations_to_FDI"
    && report.costimAfter?.tracePair?.[0] === "ulnar_wrist_FDI"
    && report.costimAfter?.tracePair?.[1] === "ulnar_below_elbow_FDI",
  sensitivityCausalFlag: report.sensitivity.state?.causalOnset === true,
  sweepCausalFlag: report.sweep.state?.causalOnset === true,
};
fs.writeFileSync(path.join(outRoot, "report.json"), JSON.stringify({ checks, errors, report }, null, 2));
if (Object.values(checks).some(v => !v)) {
  console.error(JSON.stringify({ checks, errors, report }, null, 2));
  process.exit(1);
}
console.log(JSON.stringify({ checks, screenshots: 5 }, null, 2));
