import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

const stage=path.resolve("qa_concept28_stage");
const file=path.join(stage,"ekstremite-mesafe","animasyon-2-kaliper.html");
const figureDir=path.join(stage,"figures","source-v3");
fs.mkdirSync(path.dirname(file),{recursive:true});fs.mkdirSync(figureDir,{recursive:true});
fs.copyFileSync(path.resolve("concept28_caliper.html"),file);
fs.copyFileSync(path.resolve("concept28_fig_10_17a_erb.png"),path.join(figureDir,"fig_10_17a_erb_proximal_clean.png"));
fs.copyFileSync(path.resolve("concept28_fig_10_13d_radial.png"),path.join(figureDir,"fig_10_13d_radial_above_spiral_clean.png"));

const browser=await chromium.launch({headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const errors=[];page.on("console",m=>{if(m.type()==="error")errors.push(`console: ${m.text()}`)});page.on("pageerror",e=>errors.push(`pageerror: ${e.message}`));
for(const caseName of ["erb","radial"]){
  for(const method of [0,100]){
    await page.goto(`${pathToFileURL(file).href}?case=${caseName}&method=${method}`,{waitUntil:"load"});await page.waitForTimeout(250);
    const s=await page.evaluate(()=>window.__caliperMeasurementState);
    if(s.case!==caseName)errors.push(`${caseName}/${method}: wrong case ${s.case}`);
    if(Math.abs(s.methodPercent-method)>.01)errors.push(`${caseName}/${method}: wrong method ${s.methodPercent}`);
    if(Math.abs(s.calculatedCvMps-s.measuredDistanceCm*10/s.deltaLatencyMs)>.001)errors.push(`${caseName}/${method}: formula mismatch`);
    await page.screenshot({path:`concept28_${caseName}_${method}.png`,fullPage:true});
  }
}
const hrefs=await page.locator(".bottom-bar .fkey").evaluateAll(as=>as.map(a=>a.getAttribute("href")));
if(JSON.stringify(hrefs)!==JSON.stringify(["diger-sinirler-caliper.html","../index.html","../ekstremite-morfoloji/index.html"]))errors.push(`navigation: ${JSON.stringify(hrefs)}`);
console.log(JSON.stringify({file,checks:4,errors},null,2));await browser.close();process.exit(errors.length?1:0);
