import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const liveRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations";
const qaRoot = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg\\qa_nonphys_69";
const manifest = JSON.parse(fs.readFileSync(path.join(liveRoot, "nonfizyolojik_69_sayfa_manifest.json"), "utf8"));
const animations = manifest.sequence.filter(item => item.type === "animation");
const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run", "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
await page.addInitScript(() => {
  const nativeSetTimeout = window.setTimeout.bind(window);
  window.setTimeout = (fn, delay = 0, ...args) => nativeSetTimeout(fn, Math.min(Number(delay) || 0, 70), ...args);
});
const results = [];

for (const item of animations) {
  const errors = [];
  const listener = err => errors.push(err.message);
  page.on("pageerror", listener);
  await page.goto(pathToFileURL(path.join(liveRoot, item.file)).href, { waitUntil: "load" });
  let family = "unknown";
  if (await page.locator("#gtStart").count()) {
    family = "guided-existing";
    await page.locator("#gtStart").click();
    await page.waitForTimeout(450);
  } else if (await page.locator("#play").count()) {
    family = "new-simulator";
    await page.locator("#play").click();
    await page.waitForTimeout(450);
  } else if (await page.locator("#playBtn").count()) {
    family = "stimulus-prototype";
    await page.locator("#playBtn").click();
    await page.waitForTimeout(900);
  }
  const state = await page.evaluate(familyName => {
    const controls = familyName === "guided-existing"
      ? [...document.querySelectorAll("input,select,textarea,button")]
          .filter(el => !el.closest("#guidedTourV2"))
      : [...document.querySelectorAll(".controls input,.controls select,.controls textarea,.controls .preset")];
    const stillLocked = controls.filter(el =>
      el.disabled ||
      el.getAttribute("aria-disabled") === "true" ||
      getComputedStyle(el).pointerEvents === "none"
    ).length;
    const replayText =
      document.querySelector("#gtStart,#play,#playBtn")?.textContent?.trim() || "";
    return {
      family: familyName,
      stillLocked,
      replayText,
      labLockHidden: document.querySelector("#labLock")?.classList.contains("hidden") ?? null,
    };
  }, family);
  page.off("pageerror", listener);
  const passed =
    !errors.length &&
    family !== "unknown" &&
    state.stillLocked === 0 &&
    (family !== "stimulus-prototype" || state.labLockHidden === true) &&
    /yinele/i.test(state.replayText);
  results.push({ file: item.file, passed, errors, ...state });
}

await browser.close();
const failures = results.filter(row => !row.passed);
const summary = { animations: results.length, passed: results.length - failures.length, failures };
fs.writeFileSync(path.join(qaRoot, "guided-completion-report.json"), JSON.stringify({ summary, results }, null, 2), "utf8");
console.log(JSON.stringify(summary, null, 2));
if (failures.length) process.exitCode = 1;
