import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\supramaksimal\\animasyon-1-uyari-egrisi.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",e=>errors.push(`pageerror: ${e.message}`));page.on("console",m=>{if(m.type()==="error")errors.push(`console: ${m.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(300);
const samples=[];
async function sample(i){
  await page.waitForTimeout(720);
  const value=await page.evaluate(()=>({
    state:window.__supramaxProtocolState,
    ui:{
      badge:document.querySelector("#stateBadge")?.textContent?.trim(),
      change:document.querySelector("#changeOut")?.textContent?.trim(),
      plateau:document.querySelector("#plateauOut")?.textContent?.trim(),
      margin:document.querySelector("#marginOut")?.textContent?.trim(),
      decision:document.querySelector("#decision")?.textContent?.trim(),
      nextDisabled:document.querySelector("#nextBtn")?.disabled
    }
  }));
  samples.push(value);
  await page.screenshot({path:path.join(out,`concept12_stage${i}.png`)});
}
await sample(0);for(let i=1;i<5;i++){await page.click("#nextBtn");await sample(i)}
const metrics=await page.evaluate(()=>{const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),r=nav?.getBoundingClientRect();return{overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:r?Math.round(r.bottom):null,imageFailures:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,buttons:document.querySelectorAll(".controls button").length,curve:{width:document.querySelector("#curveCanvas")?.width,height:document.querySelector("#curveCanvas")?.height},scope:{width:document.querySelector("#scopeCanvas")?.width,height:document.querySelector("#scopeCanvas")?.height},sourceAlt:document.querySelector(".source img")?.alt,caveat:document.querySelector(".caveat")?.textContent?.trim()}});
const exp=[{current:6,amplitude:4.5,latency:3.6,verdict:"increase_current"},{current:7.2,amplitude:6.8,latency:3.5,verdict:"increase_current"},{current:9,amplitude:9.3,latency:3.5,verdict:"increase_current"},{current:11,amplitude:10.5,latency:3.2,verdict:"needs_margin"},{current:14,amplitude:10.5,latency:3.1,verdict:"supramaximal_confirmed"}];
const failures=[...errors];
samples.forEach((s,i)=>{const e=exp[i],v=s.state;if(!v)failures.push(`missing state ${i}`);else{for(const k of Object.keys(e))if(v[k]!==e[k])failures.push(`stage ${i} ${k}`);if(v.bookTargetPct!==25)failures.push(`book target ${i}`)}});
if(samples[3]?.state?.plateau!=="candidate"||samples[3]?.state?.marginPct!==0||!samples[3]?.ui?.badge?.includes("durma"))failures.push("candidate decision");
if(samples[4]?.state?.plateau!=="confirmed"||Math.abs(samples[4]?.state?.marginPct-27.273)>.001||samples[4]?.state?.amplitudeChanged!==false||!samples[4]?.ui?.nextDisabled)failures.push("confirmation decision");
if(!samples[4]?.ui?.margin?.includes("%27")||!samples[4]?.ui?.decision?.includes("doğrulandı"))failures.push("final teaching output");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.imageFailures||metrics.buttons!==2||metrics.curve.width<900||metrics.scope.width<900||!metrics.sourceAlt.includes("8.17"))failures.push("visual assets");
if(!metrics.caveat.includes("AANEM")||!metrics.caveat.includes("%20–33"))failures.push("clinical range caveat");
console.log(JSON.stringify({failures,samples,metrics},null,2));await browser.close();if(failures.length)process.exitCode=1;
