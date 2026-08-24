import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\motor-elektrot-yerlesimi\\animasyon-1-g1-konumu.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({
  headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]
});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",error=>errors.push(`pageerror: ${error.message}`));
page.on("console",message=>{if(message.type()==="error")errors.push(`console: ${message.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(350);
async function setOffset(value){
  await page.locator("#offset").evaluate((element,v)=>{element.value=String(v);element.dispatchEvent(new Event("input",{bubbles:true}))},value);
  await page.waitForTimeout(120);
}
async function snap(name){
  const data=await page.evaluate(()=>({
    state:window.__g1PositionState,
    position:document.querySelector("#positionText")?.textContent?.trim(),
    distance:document.querySelector("#distanceText")?.textContent?.trim(),
    amp:document.querySelector("#ampText")?.textContent?.trim(),
    positive:document.querySelector("#positiveText")?.textContent?.trim(),
    delay:document.querySelector("#delayText")?.textContent?.trim(),
    verdict:document.querySelector("#verdictText")?.textContent?.trim(),
    logic:document.querySelector("#logicText")?.textContent?.trim(),
    mode:document.querySelector("#modeBadge")?.textContent?.trim()
  }));
  await page.screenshot({path:path.join(out,`concept18_${name}.png`)});
  return data;
}
const center=await snap("center");
await setOffset(8);const partial=await snap("offset_8mm");
await setOffset(15);const distal=await snap("offset_plus15");
await setOffset(-15);const proximal=await snap("offset_minus15");
await page.click("#scanButton");await page.waitForTimeout(2100);await page.screenshot({path:path.join(out,"concept18_auto_scan_mid.png")});
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
function fixed(s){
  return s?.variable==="g1_offset_mm"&&s?.g2Location==="fixed_distal_tendon"&&s?.stimulation==="fixed_supramaximal"&&
    s?.underlyingNerveMuscle==="normal"&&s?.referenceAmp===7.8&&s?.trueOnset===3&&
    s?.bookCalibration?.onMotorPoint===7.8&&s?.bookCalibration?.offMotorPoint===5.6;
}
for(const sample of [center,partial,distal,proximal])if(!fixed(sample.state))failures.push("fixed model");
if(center.state.offset!==0||center.state.g1Location!=="motor_point"||center.state.amplitude!==7.8||center.state.initialPositiveAmp!==0||center.state.negativeMarkerDelay!==0||center.state.morphology!=="initial_negative_biphasic"||!center.verdict.includes("amplitüd maksimum"))failures.push("center");
if(partial.state.offset!==8||partial.state.g1Location!=="off_motor_point"||partial.state.initialPositiveAmp!==1.6||partial.state.negativeMarkerDelay!==.21||partial.state.amplitude!==6.63||!partial.logic.includes("ilk pozitif sapmayı"))failures.push("partial offset");
for(const sample of [distal,proximal]){
  if(Math.abs(sample.state.offset)!==15||sample.state.amplitude!==5.6||sample.state.initialPositiveAmp!==3||sample.state.negativeMarkerDelay!==.4||sample.state.negativeOnset!==3.4||sample.state.morphology!=="initial_positive_triphasic"||!sample.verdict.includes("yeniden konumlandır"))failures.push("maximum offset");
}
if(distal.state.direction!=="distal_side"||proximal.state.direction!=="proximal_side")failures.push("offset direction");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.buttons!==1||metrics.ranges!==1||metrics.imageFailures||!metrics.imageAlt.includes("Şekil 8.21")||metrics.canvas.width<900)failures.push("visual assets");
if(!metrics.visibleText.includes("Negatif ↑ · pozitif ↓")||!metrics.visibleText.includes("7,8 → 5,6 mV")||!metrics.visibleText.includes("ko-stimülasyon")||!metrics.visibleText.includes("eşleşen distal/proksimal"))failures.push("resident teaching");
console.log(JSON.stringify({failures,center,partial,distal,proximal,metrics},null,2));
await browser.close();if(failures.length)process.exitCode=1;
