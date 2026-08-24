import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

const live="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/elektrot-sinir-mesafesi/animasyon-1-mesafe-amplitud-latans.html";
const explanation="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/elektrot-sinir-mesafesi/odem-etkisi.html";
const out="C:/Users/uugur/OneDrive/Desktop/animations_ncs_emg";
const browser=await chromium.launch({headless:true,executablePath:"C:/Program Files/Google/Chrome/Application/chrome.exe"});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const failures=[];
page.on("pageerror",e=>failures.push(`pageerror:${e.message}`));
page.on("console",m=>{if(m.type()==="error")failures.push(`console:${m.text()}`)});
await page.goto(pathToFileURL(live).href);await page.waitForTimeout(450);
async function setEdema(value,name){
  await page.locator("#edema").evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event("input",{bubbles:true}))},value);await page.waitForTimeout(180);
  const result=await page.evaluate(()=>({state:window.__edemaAttenuationState,output:document.querySelector("#edemaOutput").textContent,amplitude:document.querySelector("#amplitudeText").textContent,duration:document.querySelector("#durationText").textContent,onset:document.querySelector("#onsetText").textContent,peak:document.querySelector("#peakText").textContent,verdict:document.querySelector("#verdictText").textContent,logic:document.querySelector("#logicText").innerText,mode:document.querySelector("#modeBadge").textContent}));
  await page.screenshot({path:`${out}/concept23_${name}.png`});return result;
}
const normal=await setEdema(0,"normal"),moderate=await setEdema(10,"moderate"),marked=await setEdema(20,"marked");
if(normal.state.amplitudeUv!==20||normal.state.durationMs!==1.2||normal.state.onsetShiftMs!==0||normal.state.peakShiftMs!==0)failures.push("normal calibration");
if(moderate.state.amplitudeUv!==7.4||moderate.state.durationMs!==1.7||moderate.state.onsetShiftMs!==-.11||moderate.state.peakShiftMs!==.23)failures.push("moderate calibration");
if(marked.state.amplitudeUv!==2.7||marked.state.durationMs!==2.2||marked.state.onsetShiftMs!==-.22||marked.state.peakShiftMs!==.45)failures.push("marked calibration");
for(const s of [normal.state,moderate.state,marked.state]){
  if(s.variable!=="additional_edematous_tissue_depth_mm"||!s.electrodesCenteredOverNerve)failures.push("wrong variable");
  if(!s.stimulusFixed||!s.trueAxonResponseFixed||!s.g1g2DistanceFixed||!s.displaySettingsFixed)failures.push("fixed condition changed");
  if(!s.teachingModel||s.normativeThreshold)failures.push("teaching scope");
}
await page.locator("#scanButton").click();await page.waitForTimeout(1600);await page.screenshot({path:`${out}/concept23_auto_mid.png`});
const metrics=await page.evaluate(()=>({
  overflowX:document.documentElement.scrollWidth>document.documentElement.clientWidth,overflowY:document.documentElement.scrollHeight>document.documentElement.clientHeight,
  appOverflowX:document.querySelector(".app").scrollWidth>document.querySelector(".app").clientWidth,appOverflowY:document.querySelector(".app").scrollHeight>document.querySelector(".app").clientHeight,
  navCount:document.querySelectorAll(".bottom-bar .fkey").length,navHrefs:[...document.querySelectorAll(".bottom-bar .fkey")].map(a=>a.getAttribute("href")),
  buttons:document.querySelectorAll("button").length,ranges:document.querySelectorAll('input[type="range"]').length,
  imageFailures:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length,imageAlt:document.querySelector("#bookFigure").alt,
  visibleText:document.body.innerText,canvas:{width:document.querySelector("canvas").clientWidth,height:document.querySelector("canvas").clientHeight}
}));
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navHrefs.join("|")!=="odem-etkisi.html|../index.html|lateral-yerlesim.html")failures.push("navigation");
if(metrics.buttons!==1||metrics.ranges!==1)failures.push("controls");
if(metrics.imageFailures||!metrics.visibleText.includes("Şekil 8.28"))failures.push("source figure");
if(metrics.visibleText.includes("İmleç: 0 onset / 1 peak")||metrics.visibleText.includes("Klinik koşul"))failures.push("old overlapping controls");
const explanationHtml=fs.readFileSync(explanation,"utf8");
for(const phrase of ["sural, süperfisyal peroneal","amplitüdün <b>azalmasına","teknik bir faktör","Belirgin ödem"])if(!explanationHtml.includes(phrase))failures.push(`explanation changed:${phrase}`);
if(!fs.readFileSync(live,"utf8").includes("fig_8_28_depth_edema_clean.png"))failures.push("clean figure missing");
await browser.close();console.log(JSON.stringify({failures,normal,moderate,marked,metrics},null,2));if(failures.length)process.exit(1);
