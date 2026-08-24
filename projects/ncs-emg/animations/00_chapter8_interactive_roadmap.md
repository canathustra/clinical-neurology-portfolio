# Chapter 8 Interactive Animation Roadmap

Source: `materials/7 Uğurcan.pdf`, Chapter 8, "Artifacts and Technical Factors" (Preston & Shapiro).

Status: **all 26 modules built.** See `index.html` for the live table of contents. This file is now a build log, not a plan — it records what each module covers and maps back to the chapter so nothing gets lost if a module is edited later.

## Design standard (as built)

- Every file is standalone HTML in Turkish, no external dependencies, 16:9 slide-first layout with a mobile fallback.
- No embedded poll/QR screens. Questions are asked live in Mentimeter (separate browser tab, using its own Present mode which already shows question + QR + live results). Each HTML module opens directly to the mechanism/reveal content.
- Visual style: skin-toned hand/nerve illustrations instead of abstract shapes, dark oscilloscope-style device screens for waveform panels, short informal Turkish explanations, and a single bolded "Kural:" takeaway line at the end of each module.
- Each module's header has a nav cluster (‹ previous / module number linking to `index.html` / next ›) so the presenter can click straight through during the talk.
- Older rejected drafts and the original poll-embedded design live in `animations/_old/`.

## Module map

| # | Chapter section | File |
|---|---|---|
| 01 | Intro: correct collection + correct interpretation | `01_iki_kapi.html` |
| 02 | Intro: EDX signals are tiny and technically demanding | `02_kucuk_sinyal.html` |
| 03 | Intro: Type I and Type II errors | `03_tip1_tip2.html` |
| 04 | Temperature — ion channel mechanism | `04_sicaklik_mekanizma.html` |
| 05 | Temperature — waveform morph (Fig. 8.1) | `05_sicaklik_dalga_formu.html` |
| 06 | Temperature — phase cancellation | `06_sicaklik_faz_iptali.html` |
| 07 | Temperature — cooling paradox / clinical trap | `07_sicaklik_tuzak.html` |
| 08 | Temperature — warming delay (skin vs. nerve) | `08_sicaklik_isinma.html` |
| 09 | Age | `09_yas.html` |
| 10 | Height | `10_boy.html` |
| 11 | Proximal vs. distal nerve segments | `11_proksimal_distal.html` |
| 12 | Electrode impedance, 60-Hz noise, common-mode rejection | `12_impedans_60hz.html` |
| 13 | Filters and the passband | `13_filtreler.html` |
| 14 | Electronic averaging | `14_elektronik_ortalama.html` |
| 15 | Stimulus artifact & walking the anode | `15_stimulus_artefakti.html` |
| 16 | Cathode position: reversing stimulator polarity | `16_kutup_tersligi.html` |
| 17 | Supramaximal stimulation | `17_supramaksimal.html` |
| 18 | Co-stimulation of adjacent nerves | `18_kostimulasyon.html` |
| 19 | Electrode placement for motor studies (motor point) | `19_motor_elektrot.html` |
| 20 | Reference electrode (G2) & tendon potential | `20_referans_elektrot.html` |
| 21 | Antidromic vs. orthodromic recording | `21_antidromik_ortodromik.html` |
| 22 | Distance between recording electrodes and nerve (+ edema) | `22_elektrot_sinir_mesafesi.html` |
| 23 | Distance between active and reference electrodes | `23_g1_g2_mesafesi.html` |
| 24 | Limb position & distance measurement (ulnar at elbow) | `24_ekstremite_mesafe.html` |
| 25 | Limb position & waveform morphology | `25_ekstremite_morfoloji.html` |
| 26 | Sweep speed and sensitivity | `26_sweep_sensitivite.html` |

## If you revisit a module

Each module's explanation panel already contains the accurate chapter content and the "Kural" takeaway — that's the source of truth for what to ask about in Mentimeter, not a separate question bank (see `00_live_polling_workflow.md`).
