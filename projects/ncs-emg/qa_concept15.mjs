import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\kostimulasyon\\animasyon-1-tanisal-hatalar.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({
  headless:true,
  executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]
});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",error=>errors.push(`pageerror: ${error.message}`));
page.on("console",message=>{if(message.type()==="error")errors.push(`console: ${message.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});
await page.waitForTimeout(350);

async function capture(key){
  await page.click(`[data-scenario="${key}"]`);
  await page.waitForTimeout(120);
  const snapshot=await page.evaluate(()=>({
    state:window.__costimDiagnosticState,
    truth:document.querySelector("#truthText")?.textContent?.trim(),
    ratio:document.querySelector("#ratioText")?.textContent?.trim(),
    neighbor:document.querySelector("#neighborText")?.textContent?.trim(),
    verdict:document.querySelector("#verdictText")?.textContent?.trim(),
    logic:document.querySelector("#logicText")?.textContent?.trim()
  }));
  await page.screenshot({path:path.join(out,`concept15_${key}.png`)});
  return snapshot;
}
const normal=await capture("normal");
const falseBlock=await capture("false_block");
const trueBlock=await capture("true_block");
const masked=await capture("masked");
await page.click("#playButton");
await page.waitForTimeout(1420);
await page.screenshot({path:path.join(out,"concept15_masked_animation.png")});

const metrics=await page.evaluate(()=>{
  const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".nav"),r=nav?.getBoundingClientRect();
  const warning=document.querySelector(".warning")?.textContent?.trim()||"";
  return{
    overflowX:root.scrollWidth>root.clientWidth+1,
    overflowY:root.scrollHeight>root.clientHeight+1,
    appOverflowX:app.scrollWidth>app.clientWidth+1,
    appOverflowY:app.scrollHeight>app.clientHeight+1,
    navCount:document.querySelectorAll(".nav .fkey").length,
    navBottom:r?Math.round(r.bottom):null,
    buttons:document.querySelectorAll(".controls button").length,
    imageFailures:[...document.images].filter(image=>!image.complete||!image.naturalWidth).length,
    imageAlt:document.querySelector(".figure img")?.alt||"",
    canvas:{width:document.querySelector("#labCanvas")?.width,height:document.querySelector("#labCanvas")?.height},
    warning,
    title:document.querySelector("h1")?.textContent?.trim()
  };
});

const failures=[...errors];
function fixed(state){
  return state?.targetRecording==="APB"&&state?.neighborControl==="ADM"&&
    ["normal","conduction_block"].includes(state?.truePathology);
}
for(const sample of [normal,falseBlock,trueBlock,masked])if(!fixed(sample.state))failures.push("fixed recording model");
if(normal.state.scenario!=="normal"||normal.state.ratio!==96||normal.state.distalCostim||normal.state.proximalCostim||normal.state.neighborDistal||normal.state.neighborProximal)failures.push("normal comparison");
if(falseBlock.state.scenario!=="false_block"||falseBlock.state.truePathology!=="normal"||falseBlock.state.ratio!==53||!falseBlock.state.distalCostim||falseBlock.state.proximalCostim||falseBlock.state.neighborDistal<=0||!falseBlock.verdict.includes("Yalancı"))failures.push("false block direction");
if(trueBlock.state.scenario!=="true_block"||trueBlock.state.truePathology!=="conduction_block"||trueBlock.state.ratio!==44||trueBlock.state.distalCostim||trueBlock.state.proximalCostim||!trueBlock.verdict.includes("Gerçek blok görünür"))failures.push("visible true block");
if(masked.state.scenario!=="masked"||masked.state.truePathology!=="conduction_block"||masked.state.ratio!==96||masked.state.distalCostim||!masked.state.proximalCostim||masked.state.neighborProximal<=0||!masked.verdict.includes("gizlendi"))failures.push("masked block direction");
if(!falseBlock.logic.includes("distal BKAP")||!masked.logic.includes("blok gözden kaçar"))failures.push("teaching logic");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.buttons!==5||metrics.imageFailures||!metrics.imageAlt.includes("8.20")||metrics.canvas.width<900)failures.push("visual assets");
if(!metrics.warning.includes("Supramaksimal")||!metrics.warning.includes("morfoloji/alan/süre")||!metrics.warning.includes("anatomik varyant"))failures.push("clinical safety");
console.log(JSON.stringify({failures,normal,falseBlock,trueBlock,masked,metrics},null,2));
await browser.close();
if(failures.length)process.exitCode=1;
