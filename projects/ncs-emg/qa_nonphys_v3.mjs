import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const liveRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations";
const qaRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg\\qa_nonphys_v4_69";
const manifest = JSON.parse(fs.readFileSync(path.join(liveRoot, "nonfizyolojik_69_sayfa_manifest.json"), "utf8"));
fs.mkdirSync(qaRoot, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run", "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
const report = [];
let pageErrors = [];
page.on("pageerror", err => pageErrors.push(`pageerror: ${err.message}`));
page.on("console", msg => { if (msg.type() === "error") pageErrors.push(`console: ${msg.text()}`); });

for (const item of manifest.sequence) {
  pageErrors = [];
  await page.goto(pathToFileURL(path.join(liveRoot, item.file)).href, { waitUntil: "load", timeout: 20000 });
  await page.waitForTimeout(220);
  if (item.type === "animation") {
    await page.evaluate(() => {
      const slider = document.querySelector('input[type="range"]');
      if (slider) {
        const lo = Number(slider.min || 0), hi = Number(slider.max || 100);
        slider.value = String(lo + (hi - lo) * .72);
        slider.dispatchEvent(new Event("input", { bubbles: true }));
        slider.dispatchEvent(new Event("change", { bubbles: true }));
      }
      const preset = document.querySelector(".preset");
      if (preset && !preset.disabled) preset.click();
    });
    await page.waitForTimeout(100);
  }
  const metrics = await page.evaluate(() => {
    const root = document.documentElement;
    const shell = document.querySelector(".app,.slide");
    const nav = document.querySelector(".bottom-bar");
    const navRect = nav?.getBoundingClientRect();
    const controls = [...document.querySelectorAll(".controls input,.controls button,.control-strip input,.control-strip button")];
    return {
      title: document.title,
      bodyOverflowX: root.scrollWidth > root.clientWidth + 1,
      bodyOverflowY: root.scrollHeight > root.clientHeight + 1,
      shellOverflowX: shell ? shell.scrollWidth > shell.clientWidth + 1 : false,
      shellOverflowY: shell ? shell.scrollHeight > shell.clientHeight + 1 : false,
      bodyBackground: getComputedStyle(document.body).backgroundColor,
      shellBackground: shell ? getComputedStyle(shell).backgroundColor : "",
      navCount: document.querySelectorAll(".bottom-bar .fkey").length,
      navTop: navRect ? Math.round(navRect.top) : null,
      navBottom: navRect ? Math.round(navRect.bottom) : null,
      guidedText: /Gösterimi başlat|Önce rehberli|Duraklat|Serbest laboratuvar modu/i.test(document.body.innerText),
      disabledLabControls: controls.filter(el => el.disabled || el.getAttribute("aria-disabled") === "true").length,
      canvases: [...document.querySelectorAll("canvas")].map(c => ({
        width: c.width, height: c.height,
        displayWidth: Math.round(c.getBoundingClientRect().width),
        displayHeight: Math.round(c.getBoundingClientRect().height),
      })),
      images: [...document.images].map(img => ({
        src: img.getAttribute("src"), complete: img.complete, naturalWidth: img.naturalWidth,
      })),
      visibleTextLength: (document.body.innerText || "").trim().length,
    };
  });
  const screenshot = `${String(item.number).padStart(2, "0")}-${item.type}-${item.file.replace(/[\\/]/g, "__")}.png`;
  await page.screenshot({ path: path.join(qaRoot, screenshot) });
  report.push({ ...item, screenshot, errors: [...pageErrors], metrics });
}

await browser.close();
const failures = report.filter(row =>
  row.errors.length ||
  row.metrics.bodyOverflowX ||
  row.metrics.bodyOverflowY ||
  row.metrics.shellOverflowX ||
  row.metrics.shellOverflowY ||
  row.metrics.navCount !== 3 ||
  row.metrics.navBottom === null ||
  row.metrics.navBottom < 860 ||
  row.metrics.guidedText ||
  row.metrics.images.some(img => !img.complete || img.naturalWidth === 0) ||
  row.metrics.canvases.some(c => c.width < 100 || c.height < 80) ||
  (row.type !== "topic_entry" && row.metrics.visibleTextLength < 80)
);
const summary = {
  pages: report.length,
  explanations: report.filter(r => r.type === "explanation").length,
  animations: report.filter(r => r.type === "animation").length,
  failures: failures.map(row => ({ file: row.file, errors: row.errors, metrics: row.metrics })),
};
fs.writeFileSync(path.join(qaRoot, "browser-qa-report.json"), JSON.stringify({ summary, pages: report }, null, 2), "utf8");
console.log(JSON.stringify(summary, null, 2));
if (failures.length) process.exitCode = 1;
