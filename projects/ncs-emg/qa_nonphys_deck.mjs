import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const liveRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations";
const qaRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg\\qa_nonphys_69";
const manifest = JSON.parse(fs.readFileSync(path.join(liveRoot, "nonfizyolojik_69_sayfa_manifest.json"), "utf8"));
fs.mkdirSync(qaRoot, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run", "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
const report = [];
let current = "";
let pageErrors = [];
page.on("pageerror", err => pageErrors.push(`pageerror: ${err.message}`));
page.on("console", msg => {
  if (msg.type() === "error") pageErrors.push(`console: ${msg.text()}`);
});

for (const item of manifest.sequence) {
  current = item.file;
  pageErrors = [];
  const url = pathToFileURL(path.join(liveRoot, item.file)).href;
  await page.goto(url, { waitUntil: "load", timeout: 20000 });
  await page.waitForTimeout(180);

  if (item.type === "animation") {
    if (await page.locator("#gtStart").count()) {
      await page.locator("#gtStart").click();
      await page.waitForTimeout(180);
      await page.locator("#gtFree").click();
    } else if (await page.locator("#play").count()) {
      await page.locator("#play").click();
      await page.waitForTimeout(180);
      await page.locator("#free").click();
    } else if (await page.locator("#playBtn").count()) {
      await page.locator("#playBtn").click();
      await page.waitForTimeout(180);
      await page.evaluate(() => {
        if (typeof window.applyStep === "function") window.applyStep(7);
      });
    }
    await page.evaluate(() => {
      const slider = document.querySelector('input[type="range"]');
      if (!slider) return;
      const lo = Number(slider.min || 0), hi = Number(slider.max || 100);
      slider.value = String(lo + (hi - lo) * 0.63);
      slider.dispatchEvent(new Event("input", { bubbles: true }));
      slider.dispatchEvent(new Event("change", { bubbles: true }));
    });
    await page.waitForTimeout(120);
  }

  const metrics = await page.evaluate(() => {
    const root = document.documentElement;
    const shell = document.querySelector(".slide,.app");
    const canvases = [...document.querySelectorAll("canvas")].map(c => ({
      width: c.width,
      height: c.height,
      displayWidth: Math.round(c.getBoundingClientRect().width),
      displayHeight: Math.round(c.getBoundingClientRect().height),
    }));
    const images = [...document.images].map(img => ({
      src: img.getAttribute("src"),
      complete: img.complete,
      naturalWidth: img.naturalWidth,
    }));
    return {
      title: document.title,
      bodyOverflowX: root.scrollWidth > root.clientWidth + 1,
      bodyOverflowY: root.scrollHeight > root.clientHeight + 1,
      shellOverflowX: shell ? shell.scrollWidth > shell.clientWidth + 1 : false,
      shellOverflowY: shell ? shell.scrollHeight > shell.clientHeight + 1 : false,
      visibleTextLength: (document.body.innerText || "").trim().length,
      canvases,
      images,
      guidedTour: Boolean(document.querySelector("#guidedTourV2")),
      lockedControls: [...document.querySelectorAll("input,select,textarea,button")]
        .filter(el => !el.closest("#guidedTourV2"))
        .filter(el => el.getAttribute("aria-disabled") === "true").length,
    };
  });
  const screenshotName = `${String(item.number).padStart(2, "0")}-${item.type}-${item.file.replace(/[\\/]/g, "__")}.png`;
  await page.screenshot({ path: path.join(qaRoot, screenshotName), fullPage: false });
  report.push({ ...item, screenshot: screenshotName, errors: [...pageErrors], metrics });
}

await browser.close();
const failures = report.filter(row =>
  row.errors.length ||
  row.metrics.bodyOverflowX ||
  row.metrics.bodyOverflowY ||
  row.metrics.shellOverflowX ||
  row.metrics.shellOverflowY ||
  row.metrics.visibleTextLength < 80 ||
  row.metrics.images.some(img => !img.complete || img.naturalWidth === 0) ||
  row.metrics.canvases.some(c => c.width < 100 || c.height < 80)
);
const summary = {
  pages: report.length,
  explanationPages: report.filter(r => r.type === "explanation").length,
  animationPages: report.filter(r => r.type === "animation").length,
  guidedExistingAnimations: report.filter(r => r.metrics.guidedTour).length,
  failures: failures.map(f => ({
    file: f.file,
    errors: f.errors,
    metrics: f.metrics,
  })),
};
fs.writeFileSync(path.join(qaRoot, "browser-qa-report.json"), JSON.stringify({ summary, pages: report }, null, 2), "utf8");
console.log(JSON.stringify(summary, null, 2));
if (failures.length) process.exitCode = 1;
