import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

const live="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/elektrot-sinir-mesafesi/animasyon-2-elektrot-arama.html";
const explanation="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/elektrot-sinir-mesafesi/lateral-yerlesim.html";
const out="C:/Users/uugur/OneDrive/Desktop/animations_ncs_emg";
const browser=await chromium.launch({headless:true,executablePath:"C:/Program Files/Google/Chrome/Application/chrome.exe"});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const failures=[];page.on("pageerror",e=>failures.push(`pageerror:${e.message}`));page.on("console",m=>{if(m.type()==="error")failures.push(`console:${m.text()}`)});
await page.goto(pathToFileURL(live).href);await page.waitForTimeout(450);
async function setPosition(value,name){
  await page.locator("#position").evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event("input",{bubbles:true}))},value);await page.waitForTimeout(180);
  const result=await page.evaluate(()=>({state:window.__electrodeSearchState,output:document.querySelector("#positionOutput").textContent,position:document.querySelector("#positionText").textContent,amplitude:document.querySelector("#amplitudeText").textContent,onset:document.querySelector("#onsetText").textContent,best:document.querySelector("#bestText").textContent,verdict:document.querySelector("#verdictText").textContent,logic:document.querySelector("#logicText").innerText,mode:document.querySelector("#modeBadge").textContent}));
  await page.screenshot({path:`${out}/concept24_${name}.png`});return result;
}
const first=await setPosition(0,"first"),optimal=await setPosition(7,"optimal"),lateral=await setPosition(17,"lateral10"),far=await setPosition(-23,"far30");
if(first.state.distanceFromNerveMm!==7||first.state.amplitudeUv<20||first.state.amplitudeUv>30)failures.push("first placement calibration");
if(optimal.state.distanceFromNerveMm!==0||optimal.state.amplitudeUv!==38||optimal.state.onsetShiftMs!==0||optimal.state.interpretation!=="maximal_response_nerve_localized")failures.push("optimal calibration");
if(lateral.state.distanceFromNerveMm!==10||lateral.state.amplitudeUv!==12||lateral.state.onsetShiftMs!==-.18)failures.push("10 mm calibration");
if(far.state.distanceFromNerveMm!==30||far.state.amplitudeUv!==.8||far.state.onsetShiftMs!==-.54)failures.push("far calibration");
for(const s of [first.state,optimal.state,lateral.state,far.state]){
  if(s.variable!=="paired_recording_electrode_medial_lateral_position_mm"||!s.g1g2PairMovesTogether)failures.push("wrong variable");
  if(!s.stimulusSiteFixed||!s.stimulusCurrentFixed||!s.g1g2DistanceFixed||!s.conductionDistanceFixed||!s.displaySettingsFixed)failures.push("fixed condition changed");
  if(!s.teachingModel||s.normativeThreshold)failures.push("teaching scope");
}
await page.locator("#scanButton").click();await page.waitForTimeout(3300);await page.screenshot({path:`${out}/concept24_auto_mid.png`});await page.waitForTimeout(4100);
const autoFinal=await page.evaluate(()=>window.__electrodeSearchState);if(Math.abs(autoFinal.electrodePositionMm-7)>1||autoFinal.amplitudeUv<37)failures.push("auto search did not settle on maximum");
const metrics=await page.evaluate(()=>({overflowX:document.documentElement.scrollWidth>document.documentElement.clientWidth,overflowY:document.documentElement.scrollHeight>document.documentElement.clientHeight,appOverflowX:document.querySelector(".app").scrollWidth>document.querySelector(".app").clientWidth,appOverflowY:document.querySelector(".app").scrollHeight>document.querySelector(".app").clientHeight,navCount:document.querySelectorAll(".bottom-bar .fkey").length,navHrefs:[...document.querySelectorAll(".bottom-bar .fkey")].map(a=>a.getAttribute("href")),buttons:document.querySelectorAll("button").length,ranges:document.querySelectorAll('input[type="range"]').length,imageFailures:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length,imageAlt:document.querySelector("#bookFigure").alt,visibleText:document.body.innerText,canvas:{width:document.querySelector("canvas").clientWidth,height:document.querySelector("canvas").clientHeight}}));
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navHrefs.join("|")!=="lateral-yerlesim.html|../index.html|latans-hatasi.html")failures.push("navigation");
if(metrics.buttons!==1||metrics.ranges!==1)failures.push("controls");
if(metrics.imageFailures||!metrics.visibleText.includes("Şekil 8.29"))failures.push("source figure");
if(metrics.visibleText.includes("Sabit uyarım akımı")||metrics.visibleText.includes("5 mm lateral")||metrics.visibleText.includes("10 mm lateral"))failures.push("old overlapping controls");
const explanationHtml=fs.readFileSync(explanation,"utf8");
for(const phrase of ["anatomik işaretlere","medial, sonra lateral","en yüksek amplitüdü","Median/ulnar antidromik","Süperfisyal radial"])if(!explanationHtml.includes(phrase))failures.push(`explanation changed:${phrase}`);
if(!fs.readFileSync(live,"utf8").includes("fig_8_29_latency_clean.png"))failures.push("clean figure missing");
await browser.close();console.log(JSON.stringify({failures,first,optimal,lateral,far,autoFinal,metrics},null,2));if(failures.length)process.exit(1);
