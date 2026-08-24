import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\kostimulasyon\\animasyon-0-akim-yayilimi.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",e=>errors.push(`pageerror: ${e.message}`));page.on("console",m=>{if(m.type()==="error")errors.push(`console: ${m.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(300);
async function sample(name){const v=await page.evaluate(()=>({state:window.__costimCurrentState,ui:{badge:document.querySelector("#stateBadge")?.textContent?.trim(),median:document.querySelector("#medianOut")?.textContent?.trim(),fdi:document.querySelector("#fdiOut")?.textContent?.trim(),morph:document.querySelector("#morphOut")?.textContent?.trim(),twitch:document.querySelector("#twitchOut")?.textContent?.trim(),lesson:document.querySelector("#lesson")?.textContent?.trim()}}));await page.screenshot({path:path.join(out,`concept14_${name}.png`)});return v}
const low=await sample("37mA");await page.click("#riskBtn");await page.waitForTimeout(100);const risk=await sample("50mA");await page.click("#highBtn");await page.waitForTimeout(100);const high=await sample("87mA");await page.click("#stimBtn");await page.waitForTimeout(720);await page.screenshot({path:path.join(out,"concept14_87mA_travel.png")});
const metrics=await page.evaluate(()=>{const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),r=nav?.getBoundingClientRect();return{overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:r?Math.round(r.bottom):null,imageFailures:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,buttons:document.querySelectorAll(".controls button").length,anatomy:{width:document.querySelector("#anatomyCanvas")?.width,height:document.querySelector("#anatomyCanvas")?.height},scope:{width:document.querySelector("#scopeCanvas")?.width,height:document.querySelector("#scopeCanvas")?.height},sourceAlt:document.querySelector(".source img")?.alt,caveat:document.querySelector(".caveat")?.textContent?.trim()}});
const failures=[...errors];
for(const s of [low.state,risk.state,high.state])if(!s||s.pulseDuration!==0.2||s.stimulatorPosition!=="fixed"||s.ulnarRecruitment!==100||s.targetRecording!=="FDI"||s.neighborControl!=="APB")failures.push("fixed mechanism");
if(low.state.level!=="selective"||low.state.current!==37||low.state.medianActivation!==0||low.state.fdiAmp!==7.5||low.state.morphology!=="stable")failures.push("low state");
if(risk.state.level!=="risk_boundary"||risk.state.current!==50||risk.state.medianActivation!==12||risk.state.morphology!=="watch")failures.push("risk state");
if(high.state.level!=="costimulation"||high.state.current!==87||high.state.medianActivation!==100||high.state.fdiAmp!==10.4||high.state.morphology!=="changed"||high.state.twitch!=="ulnar_plus_median")failures.push("high state");
if(high.state.bookReference.wristCurrent!==87||high.state.bookReference.wristAmp!==10.4||high.state.bookReference.belowElbowCurrent!==37||high.state.bookReference.belowElbowAmp!==7.5)failures.push("figure 8.19 values");
if(!high.ui.lesson.includes("hacim iletilmiş")||!high.ui.lesson.includes("7,5'ten 10,4"))failures.push("teaching mechanism");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.imageFailures||metrics.buttons!==4||metrics.anatomy.width<900||metrics.scope.width<900||!metrics.sourceAlt.includes("8.19"))failures.push("visual assets");
if(!metrics.caveat.includes("evrensel eşik değildir")||!metrics.caveat.includes("morfoloji"))failures.push("clinical caveat");
console.log(JSON.stringify({failures,low,risk,high,metrics},null,2));await browser.close();if(failures.length)process.exitCode=1;
