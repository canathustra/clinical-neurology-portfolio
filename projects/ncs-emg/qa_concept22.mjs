import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

const live="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/elektrot-sinir-mesafesi/animasyon-0-derinlik-filtresi.html";
const explanation="C:/Users/uugur/OneDrive/Desktop/Second_Brain/10_Projects/presentations/artifacts_of_ncs_emg/animations/elektrot-sinir-mesafesi/index.html";
const out="C:/Users/uugur/OneDrive/Desktop/animations_ncs_emg";
const browser=await chromium.launch({headless:true,executablePath:"C:/Program Files/Google/Chrome/Application/chrome.exe"});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const failures=[];
page.on("pageerror",e=>failures.push(`pageerror:${e.message}`));
page.on("console",m=>{if(m.type()==="error")failures.push(`console:${m.text()}`)});
await page.goto(pathToFileURL(live).href);
await page.waitForTimeout(450);
async function setOffset(value,name){
  await page.locator("#offset").evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event("input",{bubbles:true}))},value);
  await page.waitForTimeout(180);
  const result=await page.evaluate(()=>({
    state:window.__electrodeDistanceState,
    output:document.querySelector("#offsetOutput").textContent,
    offset:document.querySelector("#offsetText").textContent,
    amplitude:document.querySelector("#amplitudeText").textContent,
    remaining:document.querySelector("#remainingText").textContent,
    loss:document.querySelector("#lossText").textContent,
    verdict:document.querySelector("#verdictText").textContent,
    logic:document.querySelector("#logicText").innerText,
    mode:document.querySelector("#modeBadge").textContent
  }));
  await page.screenshot({path:`${out}/concept22_${name}.png`});
  return result;
}
const centered=await setOffset(0,"centered");
const five=await setOffset(5,"5mm");
const ten=await setOffset(10,"10mm");
if(centered.state.amplitudeUv!==38||centered.state.lossPercent!==0)failures.push("0mm calibration");
if(five.state.amplitudeUv!==31||Math.abs(five.state.lossPercent-18.4)>.1)failures.push("5mm calibration");
if(ten.state.amplitudeUv!==12||Math.abs(ten.state.lossPercent-68.4)>.1)failures.push("10mm calibration");
for(const s of [centered.state,five.state,ten.state]){
  if(s.variable!=="recording_electrode_lateral_offset_mm")failures.push("wrong variable");
  if(!s.stimulusCurrentFixed||!s.g1g2DistanceFixed||!s.displaySettingsFixed||!s.underlyingAxonsFixed)failures.push("fixed condition changed");
  if(s.teachingScope!=="amplitude_effect_only"||!s.latencyEffectReservedForLaterConcept)failures.push("scope not isolated");
}
await page.locator("#scanButton").click();
await page.waitForTimeout(1450);
await page.screenshot({path:`${out}/concept22_auto_mid.png`});
const metrics=await page.evaluate(()=>({
  overflowX:document.documentElement.scrollWidth>document.documentElement.clientWidth,
  overflowY:document.documentElement.scrollHeight>document.documentElement.clientHeight,
  appOverflowX:document.querySelector(".app").scrollWidth>document.querySelector(".app").clientWidth,
  appOverflowY:document.querySelector(".app").scrollHeight>document.querySelector(".app").clientHeight,
  navCount:document.querySelectorAll(".bottom-bar .fkey").length,
  navHrefs:[...document.querySelectorAll(".bottom-bar .fkey")].map(a=>a.getAttribute("href")),
  buttons:document.querySelectorAll("button").length,
  ranges:document.querySelectorAll('input[type="range"]').length,
  imageFailures:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length,
  imageAlt:document.querySelector("#bookFigure").alt,
  visibleText:document.body.innerText,
  canvas:{width:document.querySelector("canvas").clientWidth,height:document.querySelector("canvas").clientHeight}
}));
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navHrefs.join("|")!=="index.html|../index.html|odem-etkisi.html")failures.push("navigation");
if(metrics.buttons!==1||metrics.ranges!==1)failures.push("controls");
if(metrics.imageFailures)failures.push("source image");
if(!metrics.visibleText.includes("Şekil 8.27")||metrics.visibleText.includes("Şekil 8.28"))failures.push("wrong figure concept");
const explanationHtml=fs.readFileSync(explanation,"utf8");
for(const phrase of ["38 µV","31 µV","12 µV","küçük bir artış bile"])if(!explanationHtml.includes(phrase))failures.push(`explanation changed:${phrase}`);
if(!fs.readFileSync(live,"utf8").includes("fig_8_27_electrode_search.png"))failures.push("figure 8.27 missing");
await browser.close();
console.log(JSON.stringify({failures,centered,five,ten,metrics},null,2));
if(failures.length)process.exit(1);
