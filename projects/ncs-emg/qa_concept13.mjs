import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\supramaksimal\\animasyon-2-amplitud-farki.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",e=>errors.push(`pageerror: ${e.message}`));page.on("console",m=>{if(m.type()==="error")errors.push(`console: ${m.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(300);
async function sample(name){const value=await page.evaluate(()=>({state:window.__submaxInterpretationState,ui:{badge:document.querySelector("#stateBadge")?.textContent?.trim(),ratio:document.querySelector("#ratioOut")?.textContent?.trim(),pattern:document.querySelector("#patternOut")?.textContent?.trim(),lesson:document.querySelector("#lesson")?.textContent?.trim()}}));await page.screenshot({path:path.join(out,`concept13_${name}.png`)});return value}
const normal=await sample("normal");await page.click("#distalBtn");await page.waitForTimeout(100);const distal=await sample("distal_submax");await page.click("#proxBtn");await page.waitForTimeout(100);const proximal=await sample("proximal_submax");await page.click("#stimBtn");await page.waitForTimeout(900);await page.screenshot({path:path.join(out,"concept13_proximal_travel.png")});
const metrics=await page.evaluate(()=>{const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),r=nav?.getBoundingClientRect();return{overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:r?Math.round(r.bottom):null,imageFailures:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,buttons:document.querySelectorAll(".controls button").length,nerve:{width:document.querySelector("#nerveCanvas")?.width,height:document.querySelector("#nerveCanvas")?.height},scope:{width:document.querySelector("#scopeCanvas")?.width,height:document.querySelector("#scopeCanvas")?.height},sourceAlt:document.querySelector(".source img")?.alt,caveat:document.querySelector(".caveat")?.textContent?.trim()}});
const failures=[...errors];
for(const s of [normal.state,distal.state,proximal.state])if(!s||s.trueNerve!=="normal"||s.trueMaxAmp!==10.7||s.recording!=="hypothenar"||s.nerve!=="ulnar")failures.push("fixed physiology");
if(normal.state.scenario!=="normal"||normal.state.distalAmp!==10.7||normal.state.proximalAmp!==10.7||normal.state.apparent!=="none")failures.push("normal state");
if(distal.state.scenario!=="distal_submax"||distal.state.distalAmp!==6.1||distal.state.proximalAmp!==10.7||distal.state.apparent!=="false_axonal_loss_distally"||distal.state.distalFibers!==14)failures.push("distal submax state");
if(proximal.state.scenario!=="proximal_submax"||proximal.state.distalAmp!==10.7||proximal.state.proximalAmp!==6.1||proximal.state.apparent!=="false_conduction_block"||proximal.state.proximalFibers!==14)failures.push("proximal submax state");
if(Math.abs(distal.state.ratio-175.41)>.01||Math.abs(proximal.state.ratio-57.009)>.01)failures.push("amplitude ratios");
if(!distal.ui.lesson.includes("aksonal kayıp")||!proximal.ui.lesson.includes("Yalancı iletim bloğu"))failures.push("teaching distinctions");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.imageFailures||metrics.buttons!==4||metrics.nerve.width<900||metrics.scope.width<900||!metrics.sourceAlt.includes("8.18"))failures.push("visual assets");
if(!metrics.caveat.includes("tek başına tanı değildir")||!metrics.caveat.includes("ko-stimülasyon"))failures.push("differential caveat");
console.log(JSON.stringify({failures,normal,distal,proximal,metrics},null,2));await browser.close();if(failures.length)process.exitCode=1;
