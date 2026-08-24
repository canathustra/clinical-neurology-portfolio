import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "node:url";
import fs from "node:fs";
import path from "node:path";

const root=process.env.SCALE_FILTER_ROOT||path.resolve("scale_filter_stage");
const out=path.resolve("qa_scale_filter_fix");
fs.mkdirSync(out,{recursive:true});
const targets=[
  ["sicaklik/animasyon-2-ncs.html",["snap","cmap"]],
  ["sicaklik/animasyon-3-faz-iptali.html",["snap","cmap"]],
  ["sicaklik/animasyon-4-muap.html",[]],
  ["sicaklik/animasyon-6-kts-vs-soguk.html",[]],
  ["sicaklik/animasyon-7-soguk-vs-aksonal.html",[]],
  ["filtreler/animasyon-1-gecirgen-bant.html",["sensory","motor"]],
];
const browser=await chromium.launch({
  headless:true,
  executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"],
});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const report=[];
for(const [file,modes] of targets){
  const errors=[];
  const onConsole=m=>{if(m.type()==="error")errors.push(`console:${m.text()}`)};
  const onError=e=>errors.push(`pageerror:${e.message}`);
  page.on("console",onConsole);page.on("pageerror",onError);
  await page.goto(pathToFileURL(path.join(root,file)).href,{waitUntil:"load",timeout:20000});
  await page.waitForTimeout(250);
  const states=modes.length?modes:["default"];
  for(const state of states){
    if(state!=="default"){
      await page.locator(`[data-mode="${state}"]`).click();
      await page.waitForTimeout(120);
    }
    const metrics=await page.evaluate(()=>({
      calibration:document.querySelector(".scope-calibration")?.textContent?.trim()||"",
      state:window.__filterPresetState||null,
      overflowX:document.documentElement.scrollWidth-document.documentElement.clientWidth,
      overflowY:document.documentElement.scrollHeight-document.documentElement.clientHeight,
      nav:[...document.querySelectorAll(".bottom-bar .fkey")].map(x=>x.textContent.trim()),
      title:document.querySelector(".panel-head span")?.textContent?.trim()||"",
    }));
    const safe=file.replace(/[\\/]/g,"__").replace(".html","");
    const shot=`${safe}__${state}.png`;
    await page.screenshot({path:path.join(out,shot),fullPage:true});
    report.push({file,state,metrics,errors:[...errors],shot});
  }
  page.off("console",onConsole);page.off("pageerror",onError);
}
await browser.close();
const expected={
  "sicaklik/animasyon-2-ncs.html":{snap:"25 µV/div · Sweep 1 ms/div",cmap:"3 mV/div · Sweep 1 ms/div"},
  "sicaklik/animasyon-3-faz-iptali.html":{snap:"25 µV/div · Sweep 0.4 ms/div",cmap:"3 mV/div · Sweep 0.4 ms/div"},
  "sicaklik/animasyon-4-muap.html":{default:"200 µV/div · Sweep 2 ms/div"},
  "sicaklik/animasyon-6-kts-vs-soguk.html":{default:"10 µV/div · Sweep 1 ms/div"},
  "sicaklik/animasyon-7-soguk-vs-aksonal.html":{default:"2 mV/div · Sweep 2 ms/div"},
  "filtreler/animasyon-1-gecirgen-bant.html":{sensory:"10 µV/div · Sweep 1 ms/div",motor:"2 mV/div · Sweep 2 ms/div"},
};
const failures=[];
for(const row of report){
  const want=expected[row.file]?.[row.state];
  if(want&&!row.metrics.calibration.includes(want))failures.push(`${row.file} ${row.state}: calibration "${row.metrics.calibration}"`);
  if(row.errors.length)failures.push(`${row.file} ${row.state}: ${row.errors.join(" | ")}`);
  if(row.metrics.overflowX>2||row.metrics.overflowY>2)failures.push(`${row.file} ${row.state}: overflow ${row.metrics.overflowX},${row.metrics.overflowY}`);
  if(row.metrics.nav.length!==3)failures.push(`${row.file} ${row.state}: nav ${row.metrics.nav.length}`);
}
const sensory=report.find(x=>x.file.includes("gecirgen")&&x.state==="sensory")?.metrics.state;
const motor=report.find(x=>x.file.includes("gecirgen")&&x.state==="motor")?.metrics.state;
if(sensory?.response!=="SNAP"||sensory?.unit!=="µV")failures.push(`sensory semantics ${JSON.stringify(sensory)}`);
if(motor?.response!=="BKAP"||motor?.unit!=="mV")failures.push(`motor semantics ${JSON.stringify(motor)}`);
fs.writeFileSync(path.join(out,"report.json"),JSON.stringify({report,failures},null,2));
console.log(JSON.stringify({screenshots:report.length,failures,out},null,2));
if(failures.length)process.exitCode=1;
