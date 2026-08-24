import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\supramaksimal\\animasyon-0-akson-rekrutmani.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",e=>errors.push(`pageerror: ${e.message}`));page.on("console",m=>{if(m.type()==="error")errors.push(`console: ${m.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(300);
const samples=[];
for(let i=0;i<5;i++){
  if(i)await page.click(`#step${i}`);
  await page.waitForTimeout(80);
  samples.push(await page.evaluate(()=>({state:window.__supramaxRecruitmentState,ui:{badge:document.querySelector("#stateBadge")?.textContent?.trim(),amp:document.querySelector("#ampOut")?.textContent?.trim(),lat:document.querySelector("#latOut")?.textContent?.trim(),lesson:document.querySelector("#lesson")?.textContent?.trim()}})));
  await page.screenshot({path:path.join(out,`concept11_step${i}.png`)});
}
await page.click("#step2");await page.click("#stimBtn");await page.waitForTimeout(850);await page.screenshot({path:path.join(out,"concept11_recruitment_travel.png")});
const metrics=await page.evaluate(()=>{
  const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),r=nav?.getBoundingClientRect();
  return{overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:r?Math.round(r.bottom):null,imageFailures:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,buttons:document.querySelectorAll(".controls button").length,axon:{width:document.querySelector("#axonCanvas")?.width,height:document.querySelector("#axonCanvas")?.height},scope:{width:document.querySelector("#scopeCanvas")?.width,height:document.querySelector("#scopeCanvas")?.height},sourceAlt:document.querySelector(".source img")?.alt};
});
const exp=[{current:6,amplitude:4.5,latency:3.6,activeFibers:10,stage:"recruiting"},{current:7.2,amplitude:6.8,latency:3.5,activeFibers:16,stage:"recruiting"},{current:9,amplitude:9.3,latency:3.5,activeFibers:21,stage:"recruiting"},{current:11,amplitude:10.5,latency:3.2,activeFibers:24,stage:"plateau"},{current:14,amplitude:10.5,latency:3.1,activeFibers:24,stage:"confirmed"}];
const failures=[...errors];
samples.forEach((s,i)=>{const e=exp[i],v=s.state;if(!v)failures.push(`missing state ${i}`);else{for(const k of Object.keys(e))if(v[k]!==e[k])failures.push(`step ${i} ${k}`);if(v.totalFibers!==24||v.stimulusSite!=="wrist"||v.recording!=="APB")failures.push(`fixed context ${i}`)}});
if(!(samples[3].state.amplitude===samples[4].state.amplitude&&samples[4].state.latency<samples[3].state.latency))failures.push("plateau/latency distinction");
if(!samples[3].ui.lesson.includes("henüz")||!samples[4].ui.lesson.includes("yaklaşık %25"))failures.push("protocol language");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.imageFailures||metrics.buttons!==6||metrics.axon.width<900||metrics.scope.width<900||!metrics.sourceAlt.includes("8.17"))failures.push("visual assets");
console.log(JSON.stringify({failures,samples,metrics},null,2));await browser.close();if(failures.length)process.exitCode=1;
