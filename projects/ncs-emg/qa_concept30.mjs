import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

const stage=path.resolve("qa_concept30_stage");
const dir=path.join(stage,"sweep-sensitivite");
const figures=path.join(stage,"figures","source-v3");
fs.mkdirSync(dir,{recursive:true});fs.mkdirSync(figures,{recursive:true});
fs.copyFileSync(path.resolve("concept30_sensitivity.html"),path.join(dir,"animasyon-1-sensitivite.html"));
fs.copyFileSync(path.resolve("concept30_sweep.html"),path.join(dir,"animasyon-2-sweep-hizi.html"));
fs.copyFileSync(path.resolve("concept30_fig_8_33_sensitivity.png"),path.join(figures,"fig_8_33_sensitivity.png"));
fs.copyFileSync(path.resolve("concept30_fig_8_34_sweep.png"),path.join(figures,"fig_8_34_sweep.png"));

const browser=await chromium.launch({headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const errors=[];page.on("console",m=>{if(m.type()==="error")errors.push(`console: ${m.text()}`)});page.on("pageerror",e=>errors.push(`pageerror: ${e.message}`));

async function commonChecks(label){
  const result=await page.evaluate(()=>({
    state:window.__sensitivityLatencyState||window.__sweepLatencyState,
    overflow:[document.documentElement.scrollWidth-document.documentElement.clientWidth,document.documentElement.scrollHeight-document.documentElement.clientHeight,document.querySelector(".app").scrollWidth-document.querySelector(".app").clientWidth,document.querySelector(".app").scrollHeight-document.querySelector(".app").clientHeight],
    image:[...document.images].every(i=>i.complete&&i.naturalWidth>0),
    nav:[...document.querySelectorAll(".bottom-bar .fkey")].map(a=>a.getAttribute("href"))
  }));
  if(!result.state)errors.push(`${label}: missing state`);
  if(result.overflow.some(v=>v>1))errors.push(`${label}: overflow ${JSON.stringify(result.overflow)}`);
  if(!result.image)errors.push(`${label}: image not loaded`);
  return result;
}
for(const level of [0,50,100]){
  await page.goto(`${pathToFileURL(path.join(dir,"animasyon-1-sensitivite.html")).href}?level=${level}`,{waitUntil:"load"});await page.waitForTimeout(180);
  const r=await commonChecks(`sensitivity/${level}`),s=r.state;
  if(Math.abs(s.levelPercent-level)>.01||!s.responseUnchanged)errors.push(`sensitivity/${level}: state mismatch`);
  if(level===0&&(Math.abs(s.scaleMvPerDiv-5)>.01||Math.abs(s.measuredLatencyMs-3.4)>.01))errors.push("sensitivity/0: book anchor mismatch");
  if(level===100&&(Math.abs(s.scaleMvPerDiv-.1)>.01||Math.abs(s.measuredLatencyMs-2.9)>.01))errors.push("sensitivity/100: book anchor mismatch");
  if(JSON.stringify(r.nav)!==JSON.stringify(["index.html","../index.html","animasyon-2-sweep-hizi.html"]))errors.push(`sensitivity nav: ${JSON.stringify(r.nav)}`);
  await page.screenshot({path:`concept30_sensitivity_${level}.png`,fullPage:true});
}
for(const level of [0,50,100]){
  await page.goto(`${pathToFileURL(path.join(dir,"animasyon-2-sweep-hizi.html")).href}?level=${level}`,{waitUntil:"load"});await page.waitForTimeout(180);
  const r=await commonChecks(`sweep/${level}`),s=r.state;
  if(Math.abs(s.levelPercent-level)>.01||!s.responseUnchanged)errors.push(`sweep/${level}: state mismatch`);
  if(level===0&&(Math.abs(s.sweepMsPerDiv-2)>.01||Math.abs(s.measuredLatencyMs-3.0)>.01))errors.push("sweep/0: book anchor mismatch");
  if(level===100&&(Math.abs(s.sweepMsPerDiv-.8)>.01||Math.abs(s.measuredLatencyMs-3.5)>.01))errors.push("sweep/100: book anchor mismatch");
  if(JSON.stringify(r.nav)!==JSON.stringify(["animasyon-1-sensitivite.html","../index.html","../index.html"]))errors.push(`sweep nav: ${JSON.stringify(r.nav)}`);
  await page.screenshot({path:`concept30_sweep_${level}.png`,fullPage:true});
}
console.log(JSON.stringify({checks:6,errors},null,2));await browser.close();process.exit(errors.length?1:0);
