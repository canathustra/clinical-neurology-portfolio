import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const root = path.resolve(process.env.QA_ROOT || "trace_realism_stage");
const out = path.resolve(process.env.QA_OUT || ".qa-trace-realism");
await mkdir(out, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
const results = [];
let current = "";
const errors = [];
page.on("pageerror", error => errors.push({ page: current, type: "pageerror", message: error.message }));
page.on("console", message => {
  if (message.type() === "error") errors.push({ page: current, type: "console", message: message.text() });
});

function assert(condition, message) {
  if (!condition) throw new Error(`${current}: ${message}`);
}
function close(a, b, tolerance = 0.001) {
  return Math.abs(a - b) <= tolerance;
}
async function open(relative, slug) {
  current = relative;
  await page.goto(pathToFileURL(path.join(root, relative)).href, { waitUntil: "load" });
  await page.waitForTimeout(180);
  const layout = await page.evaluate(() => ({
    title: document.title,
    widthOverflow: document.documentElement.scrollWidth - innerWidth,
    heightOverflow: document.documentElement.scrollHeight - innerHeight,
    navKeys: [...document.querySelectorAll(".bottom-bar .fkey")].length,
  }));
  assert(layout.widthOverflow <= 1, `horizontal overflow ${layout.widthOverflow}px`);
  assert(layout.heightOverflow <= 1, `vertical overflow ${layout.heightOverflow}px`);
  assert(layout.navKeys === 3, `expected 3 navigation keys, found ${layout.navKeys}`);
  await page.screenshot({ path: path.join(out, `${slug}-initial.png`) });
  return layout;
}
async function clickAndCapture(selector, slug, delay = 2200) {
  await page.locator(selector).click();
  await page.waitForTimeout(delay);
  await page.screenshot({ path: path.join(out, `${slug}.png`) });
}
async function state(name) {
  return await page.evaluate(key => window[key], name);
}

try {
  await open("stimulus-artefakti/animasyon-0-mekanizma.html", "01-stimulus");
  let s = await state("__stimulusArtifactMeasurementState");
  assert(s.traceVisible === false, "stimulus trace must start hidden");
  for (const [mode, amplitude, latency] of [["clean", 38, 2.0], ["negative", 29, 2.1], ["positive", 45, 1.9]]) {
    await page.locator(`.mbtn[data-mode="${mode}"]`).click();
    s = await state("__stimulusArtifactMeasurementState");
    assert(s.traceVisible === false, `${mode} trace appeared before stimulation`);
    assert(s.measuredAmplitudeUv === amplitude, `${mode} amplitude ${s.measuredAmplitudeUv}, expected ${amplitude}`);
    assert(close(s.measuredLatencyMs, latency), `${mode} latency ${s.measuredLatencyMs}, expected ${latency}`);
    await clickAndCapture("#shockBtn", `01-stimulus-${mode}`, 1300);
    s = await state("__stimulusArtifactMeasurementState");
    assert(s.traceVisible === true, `${mode} trace did not remain visible`);
  }
  results.push({ page: current, status: "pass" });

  await open("stimulus-artefakti/animasyon-1-anot-rotasyon.html", "02-anode");
  s = await state("__walkingAnodeState");
  assert(s.angle === 0, `default angle ${s.angle}, expected horizontal 0`);
  assert(s.traceVisible === false, "anode trace must start hidden");
  await clickAndCapture("#stimBtn", "02-anode-horizontal");
  s = await state("__walkingAnodeState");
  assert(s.traceVisible === true, "anode trace did not remain visible");
  await page.locator("#pos2Btn").click();
  assert((await state("__walkingAnodeState")).traceVisible === false, "anode preset did not hide old trace");
  await clickAndCapture("#stimBtn", "02-anode-book-position-1");
  await page.locator("#reverseBtn").click();
  await clickAndCapture("#stimBtn", "02-anode-book-position-2");
  results.push({ page: current, status: "pass" });

  await open("stimulus-artefakti/animasyon-3-kablo-induksiyonu.html", "03-cable");
  s = await state("__cableCouplingState");
  assert(s.traceVisible === false, "cable trace must start hidden");
  await clickAndCapture("#stimBtn", "03-cable-coax");
  const cleanCoupling = (await state("__cableCouplingState")).coupling;
  await page.locator("#worstBtn").click();
  s = await state("__cableCouplingState");
  assert(s.traceVisible === false, "cable preset did not hide old trace");
  await clickAndCapture("#stimBtn", "03-cable-free");
  s = await state("__cableCouplingState");
  assert(s.coupling > cleanCoupling, "free-wire coupling should exceed coaxial coupling");
  results.push({ page: current, status: "pass" });

  await open("kostimulasyon/animasyon-0-akim-yayilimi.html", "04-costim");
  s = await state("__costimCurrentState");
  assert(s.traceVisible === false, "costimulation traces must start hidden");
  assert(JSON.stringify(s.tracePair) === JSON.stringify(["ulnar_wrist_FDI", "ulnar_below_elbow_FDI"]), "wrong trace pair");
  assert(s.propagationDirection === "two_independent_stimulations_to_FDI", "wrist and below-elbow acquisitions must propagate independently toward the same FDI recording");
  await clickAndCapture("#stimBtn", "04-costim-low");
  await page.locator("#highBtn").click();
  assert((await state("__costimCurrentState")).traceVisible === false, "costim state change did not hide old traces");
  await clickAndCapture("#stimBtn", "04-costim-book");
  s = await state("__costimCurrentState");
  assert(s.wristCurrent === 87 && close(s.wristAmp, 10.4) && s.belowElbowCurrent === 37 && close(s.belowElbowAmp, 7.5), "Fig 8.19 values do not match");
  results.push({ page: current, status: "pass" });

  await open("kostimulasyon/animasyon-1-tanisal-hatalar.html", "04b-costim-diagnostic");
  s = await state("__costimDiagnosticState");
  assert(s.traceVisible === false, "diagnostic costimulation traces must start hidden");
  assert(s.propagationDirection === "both_stimuli_to_APB", "diagnostic propagation must run toward APB");
  await clickAndCapture("#playButton", "04b-costim-diagnostic-normal", 2800);
  s = await state("__costimDiagnosticState");
  assert(s.traceVisible === true, "diagnostic costimulation traces did not remain visible");
  await page.locator('.scenario[data-scenario="masked"]').click();
  assert((await state("__costimDiagnosticState")).traceVisible === false, "diagnostic scenario change did not hide old traces");
  await clickAndCapture("#playButton", "04b-costim-diagnostic-masked", 2800);
  results.push({ page: current, status: "pass" });

  await open("motor-elektrot-yerlesimi/animasyon-1-g1-konumu.html", "05-g1");
  await page.screenshot({ path: path.join(out, "05-g1-motor-point.png") });
  await page.locator("#offset").evaluate((el) => { el.value = "12"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.join(out, "05-g1-off-motor-point.png") });
  s = await state("__g1PositionState");
  assert(Math.abs(s.offset) >= 11, "G1 offset state did not update");
  results.push({ page: current, status: "pass" });

  await open("motor-elektrot-yerlesimi/animasyon-0-belly-tendon-montaj.html", "05b-belly-tendon");
  await page.locator("#time").evaluate(el => { el.value = "100"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  await page.waitForTimeout(220);
  await page.screenshot({ path: path.join(out, "05b-belly-tendon-complete.png") });
  s = await state("__bellyTendonBaselineState");
  assert(s && s.g1Location === "motor_point" && s.g2Location === "distal_tendon", "belly-tendon state missing or incorrect");
  results.push({ page: current, status: "pass" });

  await open("elektrot-sinir-mesafesi/animasyon-1-mesafe-amplitud-latans.html", "05c-edema");
  await page.locator("#edema").evaluate(el => { el.value = "20"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  await page.waitForTimeout(220);
  await page.screenshot({ path: path.join(out, "05c-edema-20mm.png") });
  s = await state("__edemaAttenuationState");
  assert(close(s.edemaMm, 20, 0.1), "edema state did not reach 20 mm");
  results.push({ page: current, status: "pass" });

  await open("elektrot-sinir-mesafesi/animasyon-2-elektrot-arama.html", "05d-electrode-search");
  await page.locator("#position").evaluate(el => { el.value = "30"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  await page.waitForTimeout(220);
  await page.screenshot({ path: path.join(out, "05d-electrode-search-30mm.png") });
  s = await state("__electrodeSearchState");
  assert(close(s.electrodePositionMm, 30, 0.1), "electrode-search state did not reach 30 mm");
  results.push({ page: current, status: "pass" });

  await open("elektrot-sinir-mesafesi/animasyon-3-yanlis-hiz.html", "05e-false-velocity");
  await page.locator("#offset").evaluate(el => { el.value = "30"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  await page.waitForTimeout(220);
  await page.screenshot({ path: path.join(out, "05e-false-velocity-30mm.png") });
  s = await state("__falseVelocityState");
  assert(close(s.lateralOffsetMm, 30, 0.1), "false-velocity state did not reach 30 mm");
  results.push({ page: current, status: "pass" });

  await open("ekstremite-mesafe/animasyon-1-dirsek-pozisyonu.html", "06-elbow");
  for (const angle of [0, 70, 90]) {
    await page.locator(`.preset[data-angle="${angle}"]`).click();
    await page.waitForTimeout(180);
    await page.screenshot({ path: path.join(out, `06-elbow-${angle}.png`) });
    s = await state("__ulnarElbowDistanceState");
    assert(close(s.angleDeg, angle, 0.5), `elbow angle ${s.angleDeg}, expected ${angle}`);
  }
  results.push({ page: current, status: "pass" });

  await open("sweep-sensitivite/animasyon-1-sensitivite.html", "07-sensitivity");
  for (const [scale, latency, slug, selectorValue] of [[5, 3.4, "5mv", "5"], [1, 3.1, "1mv", "1"], [0.1, 2.9, "100uv", ".1"]]) {
    await page.locator(`button[data-scale="${selectorValue}"]`).click();
    await page.waitForTimeout(180);
    await page.screenshot({ path: path.join(out, `07-sensitivity-${slug}.png`) });
    s = await state("__sensitivityLatencyState");
    assert(close(s.scaleMvPerDiv, scale, 0.01), `sensitivity scale ${s.scaleMvPerDiv}, expected ${scale}`);
    assert(close(s.measuredLatencyMs, latency, 0.01), `sensitivity latency ${s.measuredLatencyMs}, expected ${latency}`);
  }
  results.push({ page: current, status: "pass" });

  for (const test of [
    ["katot-polarite/animasyon-0-depolarizasyon-anodal-blok.html", "08-anodal", "__anodalBlockState", "#stimBtn", "#blockBtn"],
    ["katot-polarite/animasyon-1-polarite-tersligi.html", "09-polarity", "__reversedPolarityState", "#stimBtn", "#reverseBtn"],
    ["supramaksimal/animasyon-0-akson-rekrutmani.html", "10-supramax", "__supramaxRecruitmentState", "#stimBtn", "#step4"],
  ]) {
    const [relative, slug, stateName, stimSelector, alternateSelector] = test;
    await open(relative, slug);
    s = await state(stateName);
    assert(s.traceVisible === false, `${slug} trace must start hidden`);
    await clickAndCapture(stimSelector, `${slug}-first`);
    s = await state(stateName);
    assert(s.traceVisible === true, `${slug} trace did not remain visible`);
    await page.locator(alternateSelector).click();
    s = await state(stateName);
    assert(s.traceVisible === false, `${slug} state change did not hide old trace`);
    await clickAndCapture(stimSelector, `${slug}-alternate`);
    results.push({ page: current, status: "pass" });
  }
} catch (error) {
  results.push({ page: current, status: "fail", message: error.message, stack: error.stack });
} finally {
  await browser.close();
}

const report = { root, output: out, passed: results.filter(x => x.status === "pass").length, failed: results.filter(x => x.status === "fail").length, errors, results };
await writeFile(path.join(out, "report.json"), JSON.stringify(report, null, 2), "utf8");
console.log(JSON.stringify(report, null, 2));
if (report.failed || errors.length) process.exitCode = 1;
