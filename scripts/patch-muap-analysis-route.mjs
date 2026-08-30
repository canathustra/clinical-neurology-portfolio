import { readFile, writeFile } from "node:fs/promises";

const write=process.argv.includes("--write");
const file="projects/muap-analysis/assets/index-D6X6qUl7.js";
const source=await readFile(file,"utf8");
const before="function Rt(){let[e,t]=(0,f.useState)(0),n=(0,f.useCallback)(e=>{t(Math.max(0,Math.min($e.length-1,e)))},[]);return";
const after="function Rt(){let[e,t]=(0,f.useState)(()=>{let e=Number(location.hash.match(/^#\\/(\\d+)/)?.[1]);return Number.isFinite(e)?Math.max(0,Math.min($e.length-1,e-1)):0}),n=(0,f.useCallback)(e=>{let n=Math.max(0,Math.min($e.length-1,e));t(n),history.replaceState(null,``,`#/${n+1}`)},[]);return";
const beforeCount=source.split(before).length-1;
const afterCount=source.split(after).length-1;
if(beforeCount+afterCount!==1)throw new Error(`Expected one MUAP route patch location; found before=${beforeCount}, after=${afterCount}`);
const output=afterCount===1?source:source.replace(before,after);
if(write && output!==source)await writeFile(file,output,"utf8");
console.log(JSON.stringify({mode:write?"write":"check",beforeCount,afterCount,changed:output!==source},null,2));
