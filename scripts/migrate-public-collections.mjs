import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const write = process.argv.includes("--write");
const root = process.cwd();
const start = "<!-- neuroedx:public:start -->";
const end = "<!-- neuroedx:public:end -->";
const targets = [
  { file: "projects/muap-ready-slides/index.html", kind: "muap-atlas", domain: "EMG", title: "MUAP Visual Atlas", canonical: "/library/emg/muap-atlas", total: 121 },
  { file: "projects/muap-analysis/index.html", kind: "muap-analysis", domain: "EMG", title: "MUAP Analysis", canonical: "/library/emg/muap-analysis", total: 75 },
  { file: "projects/ach-animation/nmj-deplesyon.html", kind: "quantal", domain: "Cross-domain", title: "Quantal Depletion", canonical: "/library/cross-domain/quantal-depletion", total: 10 },
  { file: "projects/yeni-video/index.html", kind: "video", domain: "Cross-domain", title: "Blink Reflex Mechanism", canonical: "/library/cross-domain/blink-reflex", total: 1 },
];

function escape(value){return value.replaceAll("&","&amp;").replaceAll('"',"&quot;").replaceAll("<","&lt;");}
let changed=0;
for(const target of targets){
  const absolute=path.join(root,target.file);
  const html=await readFile(absolute,"utf8");
  const relative=path.relative(path.dirname(absolute),path.join(root,"assets")).replaceAll("\\","/")||".";
  const block=`${start}\n<link rel="stylesheet" href="${relative}/neuroedx-public.css" data-neuroedx-system="signal-paper-03">\n<script defer src="${relative}/neuroedx-public.js" data-neuroedx-adapter="signal-paper-03" data-kind="${target.kind}" data-domain="${escape(target.domain)}" data-title="${escape(target.title)}" data-canonical="https://edx.ucugur.chatgpt.site${target.canonical}" data-total="${target.total}"></script>\n${end}`;
  const pattern=new RegExp(`${start}[\\s\\S]*?${end}`,"i");
  let updated=pattern.test(html)?html.replace(pattern,block):html.replace(/<\/head>/i,`${block}\n</head>`);
  if(updated===html && !pattern.test(html))updated=`${block}\n${html}`;
  if(updated!==html){changed+=1;if(write)await writeFile(absolute,updated,"utf8");}
}
console.log(JSON.stringify({mode:write?"write":"check",targets:targets.length,changed},null,2));
