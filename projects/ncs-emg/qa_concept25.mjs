import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

const live="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/elektrot-sinir-mesafesi/animasyon-3-yanlis-hiz.html";
const explanation="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/elektrot-sinir-mesafesi/latans-hatasi.html";
const out="C:/Users/uugur/OneDrive/Desktop/animations_ncs_emg";
const browser=await chromium.launch({headless:true,executablePath:"C:/Program Files/Google/Chrome/Application/chrome.exe"});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});const failures=[];
page.on("pageerror",e=>failures.push(`pageerror:${e.message}`));page.on("console",m=>{if(m.type()==="error")failures.push(`console:${m.text()}`)});
await page.goto(pathToFileURL(live).href);await page.waitForTimeout(450);
async function setOffset(value,name){
  await page.locator("#offset").evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event("input",{bubbles:true}))},value);await page.waitForTimeout(180);
  const result=await page.evaluate(()=>({state:window.__falseVelocityState,output:document.querySelector("#offsetOutput").textContent,onset:document.querySelector("#onsetText").textContent,velocity:document.querySelector("#velocityText").textContent,error:document.querySelector("#errorText").textContent,verdict:document.querySelector("#verdictText").textContent,logic:document.querySelector("#logicText").innerText,mode:document.querySelector("#modeBadge").textContent}));
  await page.screenshot({path:`${out}/concept25_${name}.png`});return result;
}
const direct=await setOffset(0,"direct"),lateral10=await setOffset(10,"lateral10"),lateral30=await setOffset(30,"lateral30");
if(direct.state.amplitudeUv!==38||direct.state.onsetLatencyMs!==7.6||direct.state.calculatedVelocityMs!==52.63||direct.state.falseVelocityIncreasePct!==0)failures.push("direct calibration");
if(lateral10.state.amplitudeUv!==12||lateral10.state.onsetShiftMs!==-.2||lateral10.state.onsetLatencyMs!==7.4||lateral10.state.calculatedVelocityMs!==54.05)failures.push("10 mm calibration");
if(lateral30.state.onsetShiftMs!==-.54||lateral30.state.onsetLatencyMs!==7.06||lateral30.state.calculatedVelocityMs!==56.66||lateral30.state.falseVelocityIncreasePct!==7.6)failures.push("30 mm calibration");
for(const s of [direct.state,lateral10.state,lateral30.state]){
  if(s.variable!=="recording_electrode_lateral_offset_mm"||s.recordingDistanceM!==.4||!s.recordingDistanceFixed||!s.trueAxonVelocityFixed)failures.push("wrong variable");
  if(!s.stimulusSiteFixed||!s.stimulusCurrentFixed||!s.g1g2DistanceFixed||!s.displaySettingsFixed)failures.push("fixed condition changed");
  if(s.peakLatencyMs!==8.4||!s.volumeConductionEffect||!s.teachingModel||s.normativeThreshold)failures.push("teaching scope");
}
await page.locator("#compareButton").click();await page.waitForTimeout(1600);await page.screenshot({path:`${out}/concept25_auto_mid.png`});
const metrics=await page.evaluate(()=>({overflowX:document.documentElement.scrollWidth>document.documentElement.clientWidth,overflowY:document.documentElement.scrollHeight>document.documentElement.clientHeight,appOverflowX:document.querySelector(".app").scrollWidth>document.querySelector(".app").clientWidth,appOverflowY:document.querySelector(".app").scrollHeight>document.querySelector(".app").clientHeight,navCount:document.querySelectorAll(".bottom-bar .fkey").length,navHrefs:[...document.querySelectorAll(".bottom-bar .fkey")].map(a=>a.getAttribute("href")),buttons:document.querySelectorAll("button").length,ranges:document.querySelectorAll('input[type="range"]').length,imageFailures:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length,imageAlt:document.querySelector("#bookFigure").alt,visibleText:document.body.innerText,canvas:{width:document.querySelector("canvas").clientWidth,height:document.querySelector("canvas").clientHeight}}));
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navHrefs.join("|")!=="latans-hatasi.html|../index.html|../aktif-referans-mesafesi/konu-girisi.html")failures.push("navigation");
if(metrics.buttons!==1||metrics.ranges!==1)failures.push("controls");
if(metrics.imageFailures||!metrics.imageAlt.includes("onsetin sola kayması"))failures.push("source figure");
if(metrics.visibleText.includes("Uyarı-kayıt mesafesi")||metrics.visibleText.includes("5 mm sapma")||metrics.visibleText.includes("10 mm sapma"))failures.push("old overlapping controls");
const explanationHtml=fs.readFileSync(explanation,"utf8");
for(const phrase of ["onset latansı kısalır","tepe latansı","hacim iletim","yapay olarak hızlı İH","Yakın = Doğru"])if(!explanationHtml.includes(phrase))failures.push(`explanation changed:${phrase}`);
if(!fs.readFileSync(live,"utf8").includes("fig_8_29_latency_clean.png"))failures.push("clean figure missing");
await browser.close();console.log(JSON.stringify({failures,direct,lateral10,lateral30,metrics},null,2));if(failures.length)process.exit(1);
