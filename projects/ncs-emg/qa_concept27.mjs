import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

const stageRoot=path.resolve("qa_concept27_stage");
const file=path.join(stageRoot,"ekstremite-mesafe","animasyon-1-dirsek-pozisyonu.html");
fs.mkdirSync(path.dirname(file),{recursive:true});
fs.mkdirSync(path.join(stageRoot,"figures","source-v3"),{recursive:true});
fs.copyFileSync(path.resolve("concept27_ulnar_elbow_distance.html"),file);
fs.copyFileSync(
  path.resolve("concept27_fig_8_32_elbow_clean.png"),
  path.join(stageRoot,"figures","source-v3","fig_8_32_elbow_distance_clean.png")
);
const browser=await chromium.launch({
  headless:true,
  executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]
});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const errors=[];
page.on("console",m=>{if(m.type()==="error")errors.push(`console: ${m.text()}`)});
page.on("pageerror",e=>errors.push(`pageerror: ${e.message}`));

for(const angle of [0,70,90]){
  await page.goto(`${pathToFileURL(file).href}?angle=${angle}`,{waitUntil:"load"});
  await page.waitForTimeout(200);
  const state=await page.evaluate(()=>window.__ulnarElbowDistanceState);
  const expectedDistance=9+angle/90;
  const expectedCv=expectedDistance*5;
  if(Math.abs(state.angleDeg-angle)>.01)errors.push(`angle ${angle}: state angle ${state.angleDeg}`);
  if(Math.abs(state.measuredDistanceCm-expectedDistance)>.001)errors.push(`angle ${angle}: distance ${state.measuredDistanceCm}`);
  if(Math.abs(state.calculatedCvMps-expectedCv)>.001)errors.push(`angle ${angle}: cv ${state.calculatedCvMps}`);
  await page.screenshot({path:`concept27_${angle}.png`,fullPage:true});
}
const hrefs=await page.locator(".bottom-bar .fkey").evaluateAll(as=>as.map(a=>a.getAttribute("href")));
if(JSON.stringify(hrefs)!==JSON.stringify(["index.html","../index.html","diger-sinirler-caliper.html"]))errors.push(`navigation: ${JSON.stringify(hrefs)}`);
const alt=await page.locator(".figure-image").getAttribute("alt");
if(!alt?.includes("9 cm"))errors.push("missing figure alt");
console.log(JSON.stringify({file,checks:3,errors},null,2));
await browser.close();
process.exit(errors.length?1:0);
