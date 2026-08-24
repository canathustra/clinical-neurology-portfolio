# Presentation Template & Style Guide

Exported from the Chapter 8 "Artifacts and Technical Factors" NCS/EMG teaching deck. This
document describes every reusable convention so a new topic (e.g. GBS/AIDP) can be built
in the same visual and structural style. Read this before writing any HTML for the new deck.

## 1. Concept and delivery workflow

Two browser tabs during live delivery:
- **Tab 1: Mentimeter.** One question per module, shown in Mentimeter's own Present mode
  (already bundles question + QR + live results). Keep a companion Markdown file (e.g.
  `01_mentimeter_soru_bankasi.md`) listing every question + 5 options + correct answer, in
  deck order, so it can be pasted straight into Mentimeter as Quiz questions.
- **Tab 2: the HTML deck.** No embedded poll/QR screens inside the HTML — each module opens
  directly to the mechanism/reveal content. Keep a short `00_live_polling_workflow.md`
  documenting this two-tab pattern for whoever runs the talk.

## 2. Folder / file structure

```
<deck-root>/
  index.html                 top-level table of contents (tree + filter, see template below)
  kurallar.html              "how this session works" rules page (Mentimeter scoring rules etc.)
  <topic-slug>/
    index.html               topic's first slide (overview: 3 cards + rule-bar)
    <named-slide>.html       subsequent explanation slides, same card+rule-bar structure
    animasyon-N-<name>.html  interactive canvas animation(s), numbered in play order
```

- Topic folder names and slide file names are content-derived, lowercase, hyphenated,
  ASCII-safe (avoid raw ğ/ş/ı in filenames even though the page content uses proper Turkish
  — Windows/some tools mishandle decomposed Unicode in filenames).
- `index.html` inside a topic folder is itself a real content slide (not just a stub) —
  it's the topic's overview/first card set.
- Animation files are numbered `animasyon-1-`, `animasyon-2-`, … in the order they're
  reached during navigation, NOT necessarily the order the files were built.

## 3. Navigation rules (critical — verify after every edit)

Every page's bottom bar has exactly three buttons:

```html
<div class="bottom-bar">
<a class="fkey" href="PREV.html">F1<b>Önceki: X</b></a>
<a class="fkey" href="../index.html">F2<b>İçindekiler</b></a>
<a class="fkey" href="NEXT.html">F3<b>Sıradaki: Y</b></a>
</div>
```

- F2 always points to the top-level table of contents (`../index.html` from inside a topic
  folder).
- F1/F3 must form ONE unbroken, bidirectional chain across the ENTIRE deck: if page A's F3
  points to B, then B's F1 must point back to A. There is no branching — it's a single
  linear path a presenter clicks straight through.
- **Animations get their own toolbar counter**, separate from the F1/F3 nav:
  `<div class="tf"><label>Animasyon</label><strong>N / M — Title</strong></div>`
  where M = total animations in that topic, N = this one's position. If animations are
  ever reordered relative to each other, renumber these too.
- **Placement rule**: put each animation immediately after the specific slide it
  illustrates — not bundled at the end of a topic. If one slide has multiple cards, and
  each card gets its own animation, order the animations to match the card order. If a
  single animation genuinely needs material from two slides, place it after the *later*
  slide and add one short forward-reference sentence to the earlier slide's rule-bar or a
  card bullet, rather than leaving the reader without any pointer.
- After any reorder, verify with `grep -n 'class="fkey"' *.html` in every touched folder
  and manually trace forward/backward consistency. For a full-deck check, walk the chain
  programmatically starting from the first topic's `index.html`, following each F3 link,
  and confirm it terminates without loops or missing files.

## 4. Shared CSS shell — do not redesign

Every page uses the **exact same** `<style>` block (`.app / .titlebar / .toolbar /
.workspace / .bottom-bar / .panel / .card / .rule-bar`, plus animation-specific additions
like `.stage-wrap / .badge / .stat-row / .note-box / footer / .modetoggle`). Copy it
verbatim from `templates/topic-index-template.html` or `templates/animation-template.html`
— never hand-roll a new layout. Structure:

- `.app`: 16:9 aspect-ratio card, centered, max-width 1500px, `display:grid` with rows
  `auto auto 1fr auto` (titlebar / toolbar / workspace / bottom-bar).
- `.titlebar`: session branding (left: session name; right: product initials).
- `.toolbar`: topic name + group/animation-counter labels.
- `.workspace`: either `grid-template-rows:1fr auto` (slide: cards + rule-bar) or
  `grid-template-columns:1fr 300px` (animation: canvas stage + side readout panel).
- Color tokens (`--cyan/--blue/--amber/--green/--red/--ink/--muted/--dim`) are reused as
  per-card accent colors (`.card.c1/.c2/.c3`) — rotate through blue → amber → red (or
  blue → amber → green depending on topic) consistently within one topic.

## 5. Slide content structure

Every explanation slide (topic `index.html` and named slides) has:
1. A `.panel-head` with the slide's specific title + a short italic-style subtitle
   (`.panel-head-sub`) that poses the question the slide answers.
2. 2–3 `.card`s, each with an `<h2>` label (e.g. "Kural", "Mekanizma", "Örnek",
   "Sayısal Kural") and a bulleted `<ul>` of short, punchy claims. Bold (`<b>`) the key
   terms/numbers in each bullet. Wrap numeric values in `<span class="num">` for
   consistent tabular-figure rendering.
3. One `.rule-bar` at the very bottom of the panel: `<b>Kural:</b> <the one-sentence
   takeaway>`. Every slide ends with exactly one of these.

Don't skip content from the source material to fit this shape — fold short paragraphs into
an existing card's bullets, or merge two short adjacent points into one slide, rather than
dropping them.

## 6. Tone and terminology

- Short, informal, spoken-register Turkish — as if explaining to a colleague, not reading
  a textbook aloud. But stay clinically precise; don't oversimplify to the point of being
  wrong.
- Use the field's own established abbreviations consistently once introduced (in the NCS
  deck: DSAP/BKAP/İH/DL/G1/G2). For a GBS/AIDP deck, establish the equivalent standard
  abbreviations early (e.g. whatever the source material uses for conduction block,
  temporal dispersion, F-wave, etc.) and never re-expand them once established.
- Numeric convention: **period decimals** ("1.5–2.5 m/s", not "1,5–2,5"), and use "m/s"
  (not the Turkish "m/sn") — pick ONE convention for the whole deck and never mix, since
  dynamically-computed values from `.toFixed()` in JS always render with periods anyway.
- Every worked numeric example (mV/µV/ms/cm values) should be internally consistent
  between a slide's card, its rule-bar, and any animation's default/preset values that
  claim to reproduce it.

## 7. Canvas animation conventions

See `templates/animation-template.html` for the full boilerplate. Key rules:

- **Wave engine**: build any biphasic/triphasic waveform from two exponential "lobes"
  layered together:
  ```js
  function shape(dt,riseTau,decayTau){ if(dt<0) return 0; return Math.exp(-dt/decayTau)-Math.exp(-dt/riseTau); }
  function shapePeak(riseTau,decayTau){ let m=0; for(let dt=0;dt<=decayTau*8;dt+=decayTau/60){const v=shape(dt,riseTau,decayTau); if(v>m)m=v;} return m||1; }
  ```
  Then a main (negative) lobe + a smaller "after" (positive) lobe, each normalized by its
  own `shapePeak()`, summed to form the full waveform function.
- **Polarity convention**: the physiologically negative/main deflection is drawn UPWARD.
  Canvas y-mapping must be `py = midY + (v/scale)*halfH` — **PLUS sign**. (A minus sign
  here was a real, systemic bug discovered late in the NCS deck's development — get this
  right from the start.)
- **Canvas resize pattern**: use a `ResizeObserver` on a wrapping `.stage-wrap` div, redraw
  on resize, and scale for `devicePixelRatio`. Never hardcode canvas pixel dimensions.
- **Panel styling**: waveform-trace panels get a dark oscilloscope look (`#071a12`
  background, `#5eea8d` trace line, faint grid). Mechanism/diagram panels (non-waveform,
  e.g. electrode geometry) use the light panel background instead — don't force every
  animation into the dark oscilloscope style if it isn't actually plotting a trace.
- **Controls**: sliders (`input[type=range]`) and mode toggles (`.modetoggle` with `.mbtn`
  buttons) live in a `<footer>` below the canvas. A side `.panel.side` shows `.stat-row`
  readouts and one `.note-box` (`id="mechNote"`) that updates its text explaining *why*
  the current state looks the way it does — never just restate the numbers.
- After any JS edit, sanity-check brace `{}` and paren `()` counts still match (quick
  `grep -o` count comparison) before considering the file done.
- One animation = one concept. If a mechanism genuinely has two independent parameters
  (e.g. two different figures in the source material), build two small focused animations
  rather than one combined toggle, unless the source material itself treats them as one
  inseparable point.

## 8. Accuracy workflow

- Prefer a small, pre-isolated PDF/text extract of just the relevant source chapter over
  reading a full textbook — extract via a PDF text-extraction library (e.g. PyMuPDF/fitz)
  rather than rendering pages as images, it's far cheaper in tokens and just as accurate
  for text (only misses pure-photograph figures, which this deck reproduces as canvas
  animations rather than image copies anyway).
- Cross-check every numbered figure/box the source material cites against what's been
  built, so nothing gets silently dropped.
- When something in a slide can be verified against a live-computed value in its paired
  animation (e.g. a stated "~X m/s" figure vs. what the animation's own math produces),
  actually compute it rather than trusting the two were written consistently.

## 9. What NOT to change between decks

Everything in sections 3, 4, 6 (numeric convention), 7, and 8 should carry over unchanged
to the GBS/AIDP deck. What changes per deck: the topic list, the specific terminology/
abbreviations, the card content, the figure numbers referenced, and the accent-color
rotation if you want a different palette feel per major section.
