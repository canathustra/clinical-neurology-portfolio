import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const write = process.argv.includes("--write");
const root = process.cwd();
const animationsArg = process.argv.find((value) => value.startsWith("--animations-root="));
const animationsRoot = animationsArg
  ? path.resolve(animationsArg.slice("--animations-root=".length))
  : path.join(root, "projects", "ncs-emg", "animations");
const isPublicArchive = !animationsArg;
const startMarker = "<!-- neuroedx:signal-paper:start -->";
const endMarker = "<!-- neuroedx:signal-paper:end -->";

const canonicalSlugs = {
  "": "technical-factors",
  "giris": "technical-factors",
  "sicaklik": "temperature",
  "yas": "age",
  "boy": "height",
  "proksimal-distal": "proximal-distal",
  "impedans-gurultu": "impedance-noise",
  "filtreler": "filters",
  "elektronik-ortalama": "electronic-averaging",
  "stimulus-artefakti": "stimulus-artifact",
  "katot-polarite": "cathode-polarity",
  "supramaksimal": "supramaximal",
  "kostimulasyon": "costimulation",
  "motor-elektrot-yerlesimi": "motor-electrode-placement",
  "antidromik-ortodromik": "antidromic-orthodromic",
  "elektrot-sinir-mesafesi": "electrode-nerve-distance",
  "aktif-referans-mesafesi": "active-reference-distance",
  "ekstremite-mesafe": "limb-distance",
  "ekstremite-morfoloji": "limb-morphology",
  "sweep-sensitivite": "sweep-sensitivity",
};

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(entries.map((entry) => {
    const target = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(target) : target;
  }));
  return nested.flat();
}

function titleOf(html, fallback) {
  const title = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]
    ?.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  return title || fallback;
}

function escapeAttribute(value) {
  return value.replaceAll("&", "&amp;").replaceAll('"', "&quot;").replaceAll("<", "&lt;");
}

function navLinks(html) {
  return [...html.matchAll(/<a\b(?=[^>]*\bclass=["'][^"']*\bfkey\b[^"']*["'])(?=[^>]*\bhref=["']([^"']+)["'])[^>]*>/gi)]
    .map((match) => match[1]);
}

function orderedGroup(records) {
  const byName = new Map(records.map((record) => [path.basename(record.file).toLowerCase(), record]));
  const ordered = [];
  const seen = new Set();
  let current = byName.get("index.html") ?? [...records].sort((a, b) => a.file.localeCompare(b.file))[0];
  while (current && !seen.has(current.file)) {
    ordered.push(current);
    seen.add(current.file);
    const links = navLinks(current.html);
    const nextHref = links.at(-1)?.split(/[?#]/)[0];
    if (!nextHref) break;
    const nextPath = path.resolve(path.dirname(current.file), decodeURIComponent(nextHref));
    current = records.find((record) => path.resolve(record.file) === nextPath);
  }
  for (const record of [...records].sort((a, b) => a.file.localeCompare(b.file))) {
    if (!seen.has(record.file)) ordered.push(record);
  }
  return ordered;
}

const files = (await walk(animationsRoot)).filter((file) => file.toLowerCase().endsWith(".html"));
const records = await Promise.all(files.map(async (file) => {
  const html = await readFile(file, "utf8");
  return { file, html, title: titleOf(html, path.basename(file, ".html")) };
}));

const groups = Map.groupBy(records, (record) => path.relative(animationsRoot, path.dirname(record.file)).replaceAll("\\", "/"));
const manifest = [];
let changed = 0;
let skipped = 0;

for (const [folder, group] of groups) {
  const ordered = orderedGroup(group);
  const slug = canonicalSlugs[folder];
  const canonicalHref = slug ? `/library/ncs/technical-factors/${slug === "technical-factors" ? "" : slug}`.replace(/\/$/, "") : "/library/ncs/technical-factors";

  for (const [offset, record] of ordered.entries()) {
    const relativeAsset = path.relative(path.dirname(record.file), animationsRoot).replaceAll("\\", "/") || ".";
    const block = `${startMarker}\n<link rel="stylesheet" href="${relativeAsset}/neuroedx-system.css" data-neuroedx-system="signal-paper-03">\n<script defer src="${relativeAsset}/neuroedx-nav.js" data-neuroedx-adapter="signal-paper-03" data-index="${offset + 1}" data-total="${ordered.length}" data-label="${escapeAttribute(record.title)}" data-canonical="https://edx.ucugur.chatgpt.site${canonicalHref}"></script>\n${endMarker}`;
    const markerPattern = new RegExp(`${startMarker}[\\s\\S]*?${endMarker}`, "i");
    let updated = markerPattern.test(record.html) ? record.html.replace(markerPattern, block) : record.html.replace(/<\/head>/i, `${block}\n</head>`);
    if (updated === record.html && !markerPattern.test(record.html)) {
      skipped += 1;
    } else if (updated !== record.html) {
      changed += 1;
      if (write) await writeFile(record.file, updated, "utf8");
    }
    manifest.push({
      path: path.relative(isPublicArchive ? root : animationsRoot, record.file).replaceAll("\\", "/"),
      title: record.title,
      domain: "ncs",
      collection: folder || "course-index",
      index: offset + 1,
      total: ordered.length,
      canonicalHref,
      legacyHref: isPublicArchive
        ? `https://canathustra.github.io/clinical-neurology-portfolio/${path.relative(root, record.file).replaceAll("\\", "/")}`
        : path.relative(animationsRoot, record.file).replaceAll("\\", "/"),
    });
  }
}

manifest.sort((a, b) => a.path.localeCompare(b.path));
if (write) await writeFile(path.join(animationsRoot, "neuroedx-manifest.json"), `${JSON.stringify({ version: "2026-08-30", entries: manifest }, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ mode: write ? "write" : "check", files: records.length, changed, skipped, manifestEntries: manifest.length }, null, 2));
