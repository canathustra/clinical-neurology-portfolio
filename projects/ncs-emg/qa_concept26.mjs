import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

const live="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/aktif-referans-mesafesi/animasyon-1-g1-g2-mesafesi.html";
const explanation="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/aktif-referans-mesafesi/index.html";
const out="C:/Users/uugur/OneDrive/Desktop/animations_ncs_emg";
const browser=await chromium.launch({headless:true,executablePath:"C:/Program Files/Google/Chrome/Application/chrome.exe"});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});const failures=[];
page.on("pageerror",e=>failures.push(`pageerror:${e.message}`));page.on("console",m=>{if(m.type()==="error")failures.push(`console:${m.text()}`)});
await page.goto(pathToFileURL(live).href);await page.waitForTimeout(450);
const initialTrace=await page.evaluate(()=>window.__g1g2CancellationState);
if(initialTrace.traceInduced||initialTrace.g1RawSignalVisible||initialTrace.g2RawSignalVisible||initialTrace.differentialOutputVisible)failures.push("traces should wait for stimulation");
async function setDistance(value,name){
  await page.locator("#distance").evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event("input",{bubbles:true}))},value);await page.waitForTimeout(180);
  await page.locator("#stimulateButton").click();await page.waitForTimeout(50);
  const result=await page.evaluate(()=>({state:window.__g1g2CancellationState,output:document.querySelector("#distanceOutput").textContent,distance:document.querySelector("#distanceText").textContent,delay:document.querySelector("#delayText").textContent,amplitude:document.querySelector("#amplitudeText").textContent,cancel:document.querySelector("#cancelText").textContent,verdict:document.querySelector("#verdictText").textContent,logic:document.querySelector("#logicText").innerText,mode:document.querySelector("#modeBadge").textContent}));
  await page.screenshot({path:`${out}/concept26_${name}.png`});return result;
}
const close=await setDistance(1,"close1"),mid=await setDistance(2.5,"mid2_5"),recommended=await setDistance(4,"recommended4"),plateau=await setDistance(5,"plateau5");
if(close.state.recordedAmplitudeUv!==14||close.state.g2DelayMs!==.18||close.state.cancellationPct!==50||close.state.interpretation!=="marked_temporal_overlap_and_cancellation")failures.push("1 cm calibration");
if(mid.state.recordedAmplitudeUv!==25||mid.state.g2DelayMs!==.45||mid.state.cancellationPct!==10.7)failures.push("2.5 cm calibration");
if(recommended.state.recordedAmplitudeUv!==28||recommended.state.g2DelayMs!==.73||recommended.state.cancellationPct!==0||recommended.state.interpretation!=="recommended_3_to_4_cm_separation")failures.push("4 cm calibration");
if(plateau.state.recordedAmplitudeUv!==28||plateau.state.interpretation!=="amplitude_plateau_no_additional_gain")failures.push("plateau calibration");
for(const s of [close.state,mid.state,recommended.state,plateau.state]){
  if(s.variable!=="g1_g2_interelectrode_distance_cm"||s.sensoryConductionVelocityMs!==55||!s.conductionVelocityFixed)failures.push("wrong variable");
  if(!s.trueNerveResponseFixed||!s.stimulusFixed||!s.displaySettingsFixed)failures.push("fixed condition changed");
  if(!s.g1RawSignalVisible||!s.g2RawSignalVisible||!s.differentialOutputVisible||!s.traceInduced||!s.teachingModel||s.normativeThreshold)failures.push("teaching scope");
}
await page.locator("#compareButton").click();await page.waitForTimeout(1600);await page.screenshot({path:`${out}/concept26_auto_mid.png`});
const metrics=await page.evaluate(()=>({overflowX:document.documentElement.scrollWidth>document.documentElement.clientWidth,overflowY:document.documentElement.scrollHeight>document.documentElement.clientHeight,appOverflowX:document.querySelector(".app").scrollWidth>document.querySelector(".app").clientWidth,appOverflowY:document.querySelector(".app").scrollHeight>document.querySelector(".app").clientHeight,navCount:document.querySelectorAll(".bottom-bar .fkey").length,navHrefs:[...document.querySelectorAll(".bottom-bar .fkey")].map(a=>a.getAttribute("href")),buttons:document.querySelectorAll("button").length,ranges:document.querySelectorAll('input[type="range"]').length,imageFailures:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length,imageAlt:document.querySelector("#bookFigure").alt,visibleText:document.body.innerText,canvas:{width:document.querySelector("canvas").clientWidth,height:document.querySelector("canvas").clientHeight}}));
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navHrefs.join("|")!=="index.html|../index.html|../ekstremite-mesafe/konu-girisi.html")failures.push("navigation");
if(metrics.buttons!==2||metrics.ranges!==1)failures.push("controls");
if(metrics.imageFailures||!metrics.imageAlt.includes("14 mikrovolt"))failures.push("source figure");
if(metrics.visibleText.includes("Duyusal iletim hızı")||metrics.visibleText.includes("Yavaş iletim")||metrics.visibleText.includes("Çok yakın 1 cm"))failures.push("old overlapping controls");
const explanationHtml=fs.readFileSync(explanation,"utf8");
for(const phrase of ["aktif (<b>G1</b>)","referans (<b>G2</b>)","aynı anda","düşük amplitüdlü","3–4 cm"])if(!explanationHtml.includes(phrase))failures.push(`explanation changed:${phrase}`);
if(!fs.readFileSync(live,"utf8").includes("fig_8_31_g1_g2_distance_clean.png"))failures.push("clean figure missing");
await browser.close();console.log(JSON.stringify({failures,close,mid,recommended,plateau,metrics},null,2));if(failures.length)process.exit(1);
