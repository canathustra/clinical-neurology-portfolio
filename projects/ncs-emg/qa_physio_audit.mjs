import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "node:url";
import fs from "node:fs";
import path from "node:path";

const root="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations";
const groups=["sicaklik","yas","boy","proksimal-distal"];
const out=path.resolve("qa_physio_audit");
fs.mkdirSync(out,{recursive:true});
const files=groups.flatMap(group=>fs.readdirSync(path.join(root,group)).filter(n=>/^animasyon-.*\.html$/i.test(n)).sort().map(name=>({group,name,file:path.join(root,group,name)})));
const browser=await chromium.launch({headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]});
const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const report=[];
for(const [i,item] of files.entries()){
  const errors=[];
  const onConsole=m=>{if(m.type()==="error")errors.push(`console:${m.text()}`)};
  const onError=e=>errors.push(`pageerror:${e.message}`);
  page.on("console",onConsole);page.on("pageerror",onError);
  await page.goto(pathToFileURL(item.file).href,{waitUntil:"load",timeout:20000});
  await page.waitForTimeout(220);
  const metrics=await page.evaluate(()=>({
    title:document.title,
    bodyText:(document.body.innerText||"").slice(0,1200),
    canvasCount:document.querySelectorAll("canvas").length,
    svgCount:document.querySelectorAll("svg").length,
    calibrationText:(document.body.innerText.match(/(?:\d+(?:[.,]\d+)?\s*(?:mV|µV|uV)\s*\/\s*(?:div|kutu)|\d+(?:[.,]\d+)?\s*ms\s*\/\s*(?:div|kutu))/gi)||[]),
    overflow:[document.documentElement.scrollWidth-document.documentElement.clientWidth,document.documentElement.scrollHeight-document.documentElement.clientHeight]
  }));
  const screenshot=`${String(i+1).padStart(2,"0")}-${item.group}__${item.name}.png`;
  await page.screenshot({path:path.join(out,screenshot),fullPage:true});
  report.push({...item,screenshot,errors,metrics});
  page.off("console",onConsole);page.off("pageerror",onError);
}
await browser.close();
fs.writeFileSync(path.join(out,"report.json"),JSON.stringify(report,null,2));
console.log(JSON.stringify({pages:report.length,errors:report.flatMap(r=>r.errors),out},null,2));
