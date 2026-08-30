import { access, readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";

const root=process.cwd();
const errors=[];
const summary={};

async function exists(file){try{await access(file);return true}catch{return false}}
async function walk(directory){
  const entries=await readdir(directory,{withFileTypes:true});
  const nested=await Promise.all(entries.filter((entry)=>entry.name!==".git").map((entry)=>{
    const target=path.join(directory,entry.name);
    return entry.isDirectory()?walk(target):target;
  }));
  return nested.flat();
}
function localRefs(html){
  return [...html.matchAll(/\b(?:href|src)=["']([^"']+)["']/gi)].map((match)=>match[1]).filter((value)=>
    value && !value.includes("`+") && !/^(?:[a-z]+:|\/\/|#|data:)/i.test(value)
  );
}
async function validateRefs(file,html){
  for(const ref of localRefs(html)){
    const clean=decodeURIComponent(ref.split(/[?#]/)[0]);
    if(!clean)continue;
    const target=path.resolve(path.dirname(file),clean);
    if(!await exists(target))errors.push(`Broken local reference: ${path.relative(root,file)} -> ${ref}`);
  }
}

const manifestFile=path.join(root,"projects","ncs-emg","animations","neuroedx-manifest.json");
const manifest=JSON.parse(await readFile(manifestFile,"utf8"));
summary.ncsEntries=manifest.entries.length;
if(manifest.entries.length!==117)errors.push(`Expected 117 NCS manifest entries, found ${manifest.entries.length}`);
for(const entry of manifest.entries){
  const file=path.join(root,entry.path);
  if(!await exists(file)){errors.push(`Missing NCS page: ${entry.path}`);continue}
  const html=await readFile(file,"utf8");
  if(!html.includes('data-neuroedx-adapter="signal-paper-03"'))errors.push(`Missing NCS adapter: ${entry.path}`);
  await validateRefs(file,html);
}

const gbsDir=path.join(root,"projects","gbs-aidp","gbs");
const deckNav=await readFile(path.join(gbsDir,"assets","deck-nav.js"),"utf8");
const slideSource=deckNav.match(/const slides=(\[[\s\S]*?\]);/)?.[1];
if(!slideSource)errors.push("GBS slide manifest not found");
const gbsSlides=slideSource?JSON.parse(slideSource):[];
summary.gbsEntries=gbsSlides.length;
if(gbsSlides.length!==44)errors.push(`Expected 44 GBS entries, found ${gbsSlides.length}`);
for(const [name] of gbsSlides){
  const file=path.join(gbsDir,name);
  if(!await exists(file)){errors.push(`Missing GBS page: ${name}`);continue}
  const html=await readFile(file,"utf8");
  if(!html.includes("deck-nav.js")&&!html.includes("static-slide.js"))errors.push(`GBS page has no shared navigation path: ${name}`);
  await validateRefs(file,html);
}
if(!await exists(path.join(gbsDir,"assets","neuroedx-deck.css")))errors.push("Missing GBS Signal & Paper stylesheet");

const publicTargets=[
  "projects/muap-ready-slides/index.html",
  "projects/muap-analysis/index.html",
  "projects/ach-animation/nmj-deplesyon.html",
  "projects/yeni-video/index.html",
];
for(const relative of publicTargets){
  const file=path.join(root,relative);
  const html=await readFile(file,"utf8");
  if(!html.includes('data-neuroedx-adapter="signal-paper-03"'))errors.push(`Missing public adapter: ${relative}`);
  await validateRefs(file,html);
}
summary.publicAdapters=publicTargets.length;

const muapBundle=await readFile(path.join(root,"projects","muap-analysis","assets","index-D6X6qUl7.js"),"utf8");
if(!muapBundle.includes('history.replaceState(null,``,`#/${n+1}`)'))errors.push("MUAP Analysis does not update its stable slide hash");
if(!muapBundle.includes('location.hash.match(/^#\\/(\\d+)/)'))errors.push("MUAP Analysis does not initialize from its stable slide hash");

const tracked=execFileSync("git",["ls-files"],{cwd:root,encoding:"utf8"}).split(/\r?\n/).filter(Boolean);
const forbidden=tracked.filter((relative)=>{
  return /\.pdf$/i.test(relative)||/(^|\/)(book_ch8_nonphys_extract\.txt|book_page\d+\.png|book_pages_montage\.png|book_pages\/page-\d+\.png|concept\d+_book_page[^/]*\.png|textbook_figures_v3_montage\.png)$/i.test(relative)||/\/textbook_figures_v3\/[^/]+$/i.test(relative)||/\/figures\/source-v3\/[^/]+$/i.test(relative);
});
summary.forbiddenPublicSources=forbidden.length;
for(const file of forbidden)errors.push(`Forbidden public source asset: ${file}`);

if(errors.length){
  console.error(JSON.stringify({ok:false,summary,errors:errors.slice(0,80),errorCount:errors.length},null,2));
  process.exitCode=1;
}else{
  console.log(JSON.stringify({ok:true,summary},null,2));
}
