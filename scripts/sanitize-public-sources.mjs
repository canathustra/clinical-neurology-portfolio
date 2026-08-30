import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const write=process.argv.includes("--write");
const root=path.join(process.cwd(),"projects","ncs-emg","animations");
async function walk(directory){
  const entries=await readdir(directory,{withFileTypes:true});
  const nested=await Promise.all(entries.map((entry)=>{
    const target=path.join(directory,entry.name);
    return entry.isDirectory()?walk(target):target;
  }));
  return nested.flat();
}

const files=(await walk(root)).filter((file)=>file.toLowerCase().endsWith(".html"));
let changed=0;
let replacements=0;
for(const file of files){
  const source=await readFile(file,"utf8");
  const matches=source.match(/\.\.\/figures\/source-v3\/[^"'`\s)]+/g)??[];
  if(!matches.length)continue;
  const output=source.replace(/\.\.\/figures\/source-v3\/[^"'`\s)]+/g,"../figures/source-omitted.svg");
  changed+=1;
  replacements+=matches.length;
  if(write)await writeFile(file,output,"utf8");
}
console.log(JSON.stringify({mode:write?"write":"check",files:files.length,changed,replacements},null,2));
