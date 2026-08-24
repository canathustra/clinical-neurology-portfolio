import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\kostimulasyon\\animasyon-2-optimal-yerlesim.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({
  headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]
});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",error=>errors.push(`pageerror: ${error.message}`));
page.on("console",message=>{if(message.type()==="error")errors.push(`console: ${message.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(350);

async function setPosition(value){
  await page.locator("#offset").evaluate((element,v)=>{element.value=String(v);element.dispatchEvent(new Event("input",{bubbles:true}))},value);
  await page.waitForTimeout(120);
}
async function snap(name){
  const data=await page.evaluate(()=>({
    state:window.__optimalStimState,
    position:document.querySelector("#positionText")?.textContent?.trim(),
    current:document.querySelector("#currentText")?.textContent?.trim(),
    apb:document.querySelector("#apbText")?.textContent?.trim(),
    required:document.querySelector("#requiredText")?.textContent?.trim(),
    adm:document.querySelector("#admText")?.textContent?.trim(),
    verdict:document.querySelector("#verdictText")?.textContent?.trim(),
    mode:document.querySelector("#modeBadge")?.textContent?.trim()
  }));
  await page.screenshot({path:path.join(out,`concept16_${name}.png`)});
  return data;
}
const centerSearch=await snap("center_search");
await page.click("#finalButton");await page.waitForTimeout(1600);const centerFinal=await snap("center_final");
await setPosition(-16);const lateralSearch=await snap("lateral_search");
await page.click("#finalButton");await page.waitForTimeout(1600);const lateralFinal=await snap("lateral_final");
await setPosition(16);const medialSearch=await snap("medial_search");
await page.click("#finalButton");await page.waitForTimeout(1600);const medialFinal=await snap("medial_final");
await page.click("#scanButton");await page.waitForTimeout(1800);await page.screenshot({path:path.join(out,"concept16_auto_scan_mid.png")});

const metrics=await page.evaluate(()=>{
  const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),r=nav?.getBoundingClientRect();
  return{
    overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,
    appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,
    navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:r?Math.round(r.bottom):null,
    buttons:document.querySelectorAll(".controls button").length,ranges:document.querySelectorAll(".controls input[type=range]").length,
    imageFailures:[...document.images].filter(image=>!image.complete||!image.naturalWidth).length,
    imageAlt:document.querySelector(".book img")?.alt||"",
    canvas:{width:document.querySelector("#labCanvas")?.width,height:document.querySelector("#labCanvas")?.height},
    visibleText:document.body.innerText
  };
});
const failures=[...errors];
function fixed(s){return s?.variable==="stimulator_position"&&s?.scanCurrent===20&&s?.pulseDuration===.2}
for(const sample of [centerSearch,centerFinal,lateralSearch,lateralFinal,medialSearch,medialFinal])if(!fixed(sample.state))failures.push("fixed protocol");
if(centerSearch.state.mode!=="search"||!centerSearch.state.currentLockedDuringScan||centerSearch.state.offset!==0||centerSearch.state.targetSearchAmp!==4.1||centerSearch.state.requiredSupramax!==27)failures.push("center search");
if(centerFinal.state.mode!=="final"||!centerFinal.state.finalComplete||!centerFinal.state.optimal||centerFinal.state.costim||centerFinal.state.current!==27||!centerFinal.verdict.includes("Optimal"))failures.push("center final");
if(lateralSearch.state.offset!==-16||lateralSearch.state.direction!=="lateral"||lateralSearch.state.current!==20||lateralSearch.state.targetSearchAmp>=1||lateralSearch.state.requiredSupramax!==48)failures.push("lateral search");
if(lateralFinal.state.current!==48||lateralFinal.state.costim||lateralFinal.state.neighborAmp!==0||!lateralFinal.verdict.includes("Yüksek akım"))failures.push("lateral consequence");
if(medialSearch.state.offset!==16||medialSearch.state.direction!=="medial_toward_ulnar"||medialSearch.state.current!==20||medialSearch.state.adjacentThreshold!==45.2)failures.push("medial search");
if(medialFinal.state.current!==48||!medialFinal.state.costim||medialFinal.state.neighborAmp<=1||!medialFinal.verdict.includes("Ko-stimülasyon"))failures.push("medial costimulation");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.buttons!==2||metrics.ranges!==1||metrics.imageFailures||!metrics.imageAlt.includes("Box 8.5")||metrics.canvas.width<900)failures.push("visual assets");
if(!metrics.visibleText.includes("Akımı sabitle, konumu tara")||!metrics.visibleText.includes("eşikler evrensel değildir")||!metrics.visibleText.includes("morfoloji ve kas seğirmesi"))failures.push("clinical teaching");
console.log(JSON.stringify({failures,centerSearch,centerFinal,lateralSearch,lateralFinal,medialSearch,medialFinal,metrics},null,2));
await browser.close();if(failures.length)process.exitCode=1;
