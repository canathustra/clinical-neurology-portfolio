# Project Brief: NCS/EMG "Artifacts and Technical Factors" Teaching Deck

## What This Is

Turkish-language interactive HTML teaching deck for neurology residents, covering Chapter 8, "Artifacts and Technical Factors," from Preston & Shapiro, *Electromyography and Neuromuscular Disorders*.

Source PDF: `materials/07_source_chapter8.pdf`  
Original source filename may contain Turkish/Unicode characters; prefer the ASCII-safe copy above when scripting.

## Presentation Workflow

Use two browser tabs during the talk:

1. **Mentimeter:** questions, QR, voting, and live results.
2. **HTML deck:** mechanism, real recordings, models, clinical interpretation, and source summaries.

Do not add poll or QR screens back into the HTML deck. Mentimeter already handles that better.

## Current Structure

The live deck is in `animations/`.

- `index.html` is the table of contents.
- 26 chapter topics are covered.
- 67 deck pages are wired in sequence.
- 68 HTML files exist including `index.html`.
- 25 generated source-summary pages exist.
- 14 real-source figure pages exist.
- Extracted source images live in `animations/figures/source/`.
- The generator/polish script is `tools/polish_deck.py`.

Current page types:

- **Concept/model pages:** interactive or explanatory HTML pages.
- **Figure pages:** real textbook figures, shown before the related summary when available.
- **Summary pages:** direct Turkish clinical summaries from the chapter topic.

## Content Scope

Do not skip chapter sections. The deck covers:

- **Giriş:** EDX data collection vs interpretation, low-amplitude signals/noise, Type I/II errors.
- **Fizyolojik faktörler:** temperature mechanisms, waveform changes, phase cancellation, cooling trap, warming delay, age, height, proximal/distal segment differences.
- **Nonfizyolojik faktörler:** electrode impedance/60 Hz noise, filters, electronic averaging, stimulus artifact/anode position, cathode-anode reversal, supramaximal stimulation, co-stimulation, motor electrode placement, reference electrode/tendon potential, antidromic vs orthodromic recordings, electrode-nerve distance/edema, G1-G2 distance, limb position, sweep speed/sensitivity.

## Language Rules

- Use correct Turkish clinical terminology: DL, CV, amplitüd, latans, inaktivasyon, depolarizasyon, nod, miyelin, stimulus artefaktı, ko-stimülasyon, supramaksimal uyarım.
- Keep sentences short and direct.
- Avoid invented slang, jokes, courtroom metaphors, and childish visual metaphors.
- Avoid invented metaphors, courtroom analogies, joke phrasing, and casual imperatives.
- Prefer clinical phrasing: "değerlendirilmelidir," "kontrol edilmelidir," "yorumundan önce doğrulanmalıdır."
- Each module should end with a clear **Kural:** line.

## Visual Rules

- Real textbook figures are preferred whenever available.
- Do not hand-draw anatomy from primitive shapes.
- Technical simulations should look like instrument displays: dark scope background, grid, clinical labels, realistic asymmetric traces.
- Keep figure pages professional: real source image first, concise clinical interpretation beside it.
- Avoid childish iconography, decorative blobs, cartoon anatomy, or overly playful metaphors.
- Keep slide headers, explanation panels, and rule boxes visually distinct.

## Figure Integration

Figure pages are currently wired for these topics:

- 08: warming delay
- 13: filters
- 14: electronic averaging
- 15: stimulus artifact
- 16: cathode-anode reversal
- 17: supramaximal stimulation
- 18: co-stimulation
- 19: motor electrode placement
- 20: reference electrode/tendon potential
- 21: antidromic vs orthodromic
- 22: electrode-nerve distance/edema
- 23: G1-G2 distance
- 24: limb position/distance
- 26: sweep speed/sensitivity

## Validation

After regenerating the deck, run:

```powershell
$env:PYTHONIOENCODING='utf-8'; python tools\polish_deck.py
```

Then verify links and images. The expected current result is:

```text
missing_links 0
missing_images 0
html_count 68
figure_pages 14
```

## Recent Polish Notes

- Module 01 was reframed from "two gates" to **EDX doğruluğunun iki aşaması**.
- Module 02 was reframed as **Düşük amplitüdlü sinyal ve gürültü**.
- Module 03 now uses direct **yalancı pozitif / yalancı negatif** wording.
- Module 04 was rebuilt as a trace-based model rather than a hand-drawn ion-channel illustration.
- Modules 10-18 and 19-26 were tightened to remove casual phrasing and make headers/rules more clinical.
- `animations/00_live_polling_workflow.md` was updated to match the current slide names.
