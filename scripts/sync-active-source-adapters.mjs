import { copyFile, readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";

const write=process.argv.includes("--write");
const rootArg=process.argv.find((value)=>value.startsWith("--presentations-root="));
if(!rootArg)throw new Error("Pass --presentations-root=<04_Presentations path>");
const archiveRoot=process.cwd();
const presentationsRoot=path.resolve(rootArg.slice("--presentations-root=".length));

const gbsAssets=path.join(presentationsRoot,"01_Active_Projects","02_GBS_AIDP","GBS and AIDP Presentation","gbs","assets");
const ncsAnimations=path.join(presentationsRoot,"01_Active_Projects","01_EMG_NCS","artifacts_of_ncs_emg","animations");
const muapRoot=path.join(presentationsRoot,"01_Active_Projects","03_Basic_Electromyography_Analysis_of_MUAPs","MUAP_Hazir_Sunum_Hastane_121_2026-08-29");
const copies=[
  [path.join(archiveRoot,"projects","gbs-aidp","gbs","assets","deck-nav.js"),path.join(gbsAssets,"deck-nav.js")],
  [path.join(archiveRoot,"projects","gbs-aidp","gbs","assets","neuroedx-deck.css"),path.join(gbsAssets,"neuroedx-deck.css")],
  [path.join(archiveRoot,"projects","ncs-emg","animations","neuroedx-system.css"),path.join(ncsAnimations,"neuroedx-system.css")],
  [path.join(archiveRoot,"projects","ncs-emg","animations","neuroedx-nav.js"),path.join(ncsAnimations,"neuroedx-nav.js")],
];

const publicCss=await readFile(path.join(archiveRoot,"assets","neuroedx-public.css"),"utf8");
const publicJs=await readFile(path.join(archiveRoot,"assets","neuroedx-public.js"),"utf8");
const muapHtmlFile=path.join(muapRoot,"MUAP_Hazir_Sunum.html");
const muapSource=await readFile(muapHtmlFile,"utf8");
const styleStart="<!-- neuroedx:offline-style:start -->";
const styleEnd="<!-- neuroedx:offline-style:end -->";
const scriptStart="<!-- neuroedx:offline-script:start -->";
const scriptEnd="<!-- neuroedx:offline-script:end -->";
const styleBlock=`${styleStart}\n<style data-neuroedx-system="signal-paper-03">\n${publicCss}\n</style>\n${styleEnd}`;
const scriptBlock=`${scriptStart}\n<script data-neuroedx-adapter="signal-paper-03" data-kind="muap-atlas" data-domain="EMG" data-title="MUAP Visual Atlas" data-canonical="https://edx.ucugur.chatgpt.site/library/emg/muap-atlas" data-total="121">\n${publicJs}\n</script>\n${scriptEnd}`;
const stylePattern=new RegExp(`${styleStart}[\\s\\S]*?${styleEnd}`,"i");
const scriptPattern=new RegExp(`${scriptStart}[\\s\\S]*?${scriptEnd}`,"i");
let muapUpdated=stylePattern.test(muapSource)?muapSource.replace(stylePattern,styleBlock):muapSource.replace(/<\/head>/i,`${styleBlock}\n</head>`);
muapUpdated=scriptPattern.test(muapUpdated)?muapUpdated.replace(scriptPattern,scriptBlock):muapUpdated.replace(/<\/body>/i,`${scriptBlock}\n</body>`);

if(write){
  for(const [source,target] of copies)await copyFile(source,target);
  if(muapUpdated!==muapSource)await writeFile(muapHtmlFile,muapUpdated,"utf8");
  const htmlHash=createHash("sha256").update(muapUpdated).digest("hex");
  const versionFile=path.join(muapRoot,"VERSION.json");
  const version=JSON.parse(await readFile(versionFile,"utf8"));
  version.design_system="Signal & Paper 03";
  version.design_locked_at="2026-08-30";
  version.html_bytes=Buffer.byteLength(muapUpdated);
  version.html_sha256=htmlHash;
  const versionText=`${JSON.stringify(version,null,2)}\n`;
  await writeFile(versionFile,versionText,"utf8");
  const versionHash=createHash("sha256").update(versionText).digest("hex");
  const sumsFile=path.join(muapRoot,"SHA256SUMS.txt");
  let sums=await readFile(sumsFile,"utf8");
  sums=sums.replace(/^[a-f0-9]{64}\s+MUAP_Hazir_Sunum\.html$/m,`${htmlHash}  MUAP_Hazir_Sunum.html`);
  sums=sums.replace(/^[a-f0-9]{64}\s+VERSION\.json$/m,`${versionHash}  VERSION.json`);
  await writeFile(sumsFile,sums,"utf8");
}

console.log(JSON.stringify({mode:write?"write":"check",copiedAssets:copies.length,muapHtmlChanged:muapUpdated!==muapSource,ncsAnimations},null,2));
