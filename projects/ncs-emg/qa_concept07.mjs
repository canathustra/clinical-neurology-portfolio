import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\stimulus-artefakti\\animasyon-1-anot-rotasyon.html";
const out = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run", "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
const errors = [];
page.on("pageerror", error => errors.push(`pageerror: ${error.message}`));
page.on("console", message => { if (message.type() === "error") errors.push(`console: ${message.text()}`); });
await page.goto(pathToFileURL(live).href, { waitUntil: "load" });
await page.waitForTimeout(300);

async function sample(name) {
  const state = await page.evaluate(() => window.__walkingAnodeState);
  const ui = await page.evaluate(() => ({
    angle: document.querySelector("#angleOut")?.value,
    badge: document.querySelector("#stateBadge")?.textContent?.trim(),
    onset: document.querySelector("#onsetOut")?.textContent?.trim(),
    lesson: document.querySelector("#lesson")?.textContent?.trim(),
    cathode: document.querySelector("#cathodeOut")?.textContent?.trim(),
    trueOut: document.querySelector("#trueOut")?.textContent?.trim(),
  }));
  await page.screenshot({ path: path.join(out, `concept07_${name}.png`) });
  return { state, ui };
}

const optimum = await sample("position2");
await page.click("#pos1Btn");
await page.waitForTimeout(120);
const position1 = await sample("position1");
await page.click("#reverseBtn");
await page.waitForTimeout(120);
const reverse = await sample("reverse");
await page.click("#pos2Btn");
await page.click("#stimBtn");
await page.waitForTimeout(850);
await page.screenshot({ path: path.join(out, "concept07_conduction.png") });
const animated = await page.evaluate(() => window.__walkingAnodeState);

const metrics = await page.evaluate(() => {
  const root = document.documentElement, app = document.querySelector(".app"), nav = document.querySelector(".bottom-bar");
  const navRect = nav?.getBoundingClientRect();
  return {
    overflowX: root.scrollWidth > root.clientWidth + 1,
    overflowY: root.scrollHeight > root.clientHeight + 1,
    appOverflowX: app.scrollWidth > app.clientWidth + 1,
    appOverflowY: app.scrollHeight > app.clientHeight + 1,
    navCount: document.querySelectorAll(".bottom-bar .fkey").length,
    navBottom: navRect ? Math.round(navRect.bottom) : null,
    imageFailures: [...document.images].filter(img => !img.complete || !img.naturalWidth).length,
    geo: { width: document.querySelector("#geoCanvas")?.width, height: document.querySelector("#geoCanvas")?.height },
    scope: { width: document.querySelector("#scopeCanvas")?.width, height: document.querySelector("#scopeCanvas")?.height },
    controlCount: document.querySelectorAll(".controls button").length,
  };
});

const states = [optimum.state, position1.state, reverse.state, animated];
const failures = [...errors];
if (states.some(s => !s)) failures.push("missing exposed state");
if (states.some(s => s.cathodeX !== optimum.state.cathodeX || s.cathodeY !== optimum.state.cathodeY)) failures.push("cathode moved");
if (states.some(s => s.trueAmp !== 14 || s.trueLatency !== 2.4)) failures.push("true DSAP changed");
if (Math.abs(optimum.state.artifactTail) > 0.5) failures.push("optimum tail not minimized");
if (!(position1.state.artifactTail < -15 && reverse.state.artifactTail > 15)) failures.push("tail polarity response");
if (optimum.ui.onset !== "YÜKSEK" || position1.ui.onset !== "DÜŞÜK" || reverse.ui.onset !== "DÜŞÜK") failures.push("onset teaching states");
if (!position1.ui.lesson.includes("Değişen sinir yanıtı değil")) failures.push("mechanism wording");
if (!optimum.ui.badge.includes("Konum 2") || !position1.ui.badge.includes("Konum 1")) failures.push("book positions");
if (metrics.overflowX || metrics.overflowY || metrics.appOverflowX || metrics.appOverflowY) failures.push("overflow");
if (metrics.navCount !== 3 || metrics.navBottom === null || metrics.navBottom < 860) failures.push("navigation layout");
if (metrics.imageFailures || metrics.geo.width < 900 || metrics.scope.width < 900 || metrics.controlCount !== 4) failures.push("visual assets");

console.log(JSON.stringify({ failures, optimum, position1, reverse, animated, metrics }, null, 2));
await browser.close();
if (failures.length) process.exitCode = 1;
