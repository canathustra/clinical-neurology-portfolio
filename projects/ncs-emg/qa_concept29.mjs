import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

const stage=path.resolve("qa_concept29_stage");
const file=path.join(stage,"ekstremite-morfoloji","animasyon-1-pozisyon-tutarliligi.html");
const figureDir=path.join(stage,"figures","source-v3");
fs.mkdirSync(path.dirname(file),{recursive:true});
fs.mkdirSync(figureDir,{recursive:true});
fs.copyFileSync(path.resolve("concept29_position_consistency.html"),file);
fs.copyFileSync(path.resolve("concept19_fig_8_24_decomposition.png"),path.join(figureDir,"fig_8_24_g1_minus_g2.png"));

const browser=await chromium.launch({
  headless:true,
  executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]
});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const errors=[];
page.on("console",m=>{if(m.type()==="error")errors.push(`console: ${m.text()}`)});
page.on("pageerror",e=>errors.push(`pageerror: ${e.message}`));

for(const value of [0,50,100]){
  await page.goto(`${pathToFileURL(file).href}?mismatch=${value}`,{waitUntil:"load"});
  await page.waitForTimeout(250);
  const state=await page.evaluate(()=>window.__positionConsistencyState);
  if(!state)errors.push(`${value}: missing state`);
  else{
    if(Math.abs(state.mismatchPercent-value)>.01)errors.push(`${value}: mismatch ${state.mismatchPercent}`);
    if(state.trueNeuralConduction!=="fixed")errors.push(`${value}: neural conduction not fixed`);
    if(Math.abs(state.belowElbowAngleDeg-70)>.01||Math.abs(state.aboveElbowAngleDeg-70)>.01)errors.push(`${value}: proximal angles changed`);
    if(Math.abs(state.apparentElbowCvMps-100/(8.70+.22*value/100-(6.85+.12*value/100)))>.01)errors.push(`${value}: CV formula mismatch`);
  }
  const overflow=await page.evaluate(()=>({
    bodyX:document.documentElement.scrollWidth-document.documentElement.clientWidth,
    bodyY:document.documentElement.scrollHeight-document.documentElement.clientHeight,
    appX:document.querySelector(".app").scrollWidth-document.querySelector(".app").clientWidth,
    appY:document.querySelector(".app").scrollHeight-document.querySelector(".app").clientHeight
  }));
  if(Object.values(overflow).some(v=>v>1))errors.push(`${value}: overflow ${JSON.stringify(overflow)}`);
  const imageOk=await page.locator(".book-figure img").evaluate(img=>img.complete&&img.naturalWidth>0);
  if(!imageOk)errors.push(`${value}: textbook image not loaded`);
  await page.screenshot({path:`concept29_position_${value}.png`,fullPage:true});
}
const hrefs=await page.locator(".bottom-bar .fkey").evaluateAll(as=>as.map(a=>a.getAttribute("href")));
if(JSON.stringify(hrefs)!==JSON.stringify(["index.html","../index.html","../sweep-sensitivite/index.html"]))errors.push(`navigation: ${JSON.stringify(hrefs)}`);
console.log(JSON.stringify({file,checks:3,errors},null,2));
await browser.close();
process.exit(errors.length?1:0);
