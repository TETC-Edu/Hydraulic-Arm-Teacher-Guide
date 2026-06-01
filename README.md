# Hydraulic Rescue Arm · Teacher Guide

A self-contained, offline teacher guide for the **Hydraulic Rescue Arm** unit at TETC
(ExxonMobil Foundation · Teen Engineering + Tech Center). It is the coach-side companion to the
slide deck: for each phase of each day it lays out what's on screen, what to say, what to do, what
to watch for, what to say if students ask, and a pedagogical note.

**Live:** https://tetc-edu.github.io/Hydraulic-Arm-Teacher-Guide/

## Using it in class

- Open the live link on a laptop, or download `index.html` and open it directly — it works fully
  offline (all CSS, fonts, slide images, and logos are embedded).
- Navigate with the top tabs or keyboard shortcuts: `1` / `2` / `3` for days, `4` for Reference,
  `H` for home, `R` for the failure-mode drawer, arrow keys for previous/next phase, `Esc` to close.
- Each phase has a countdown timer. The prep checklist and your per-phase notes are saved in the
  browser (localStorage), so they persist between visits on the same machine.
- It prints cleanly: phases stay whole across page breaks and the footer logo is preserved.
- The **Reference** tab is the mid-class quick-lookup hub (force equation, syringe cheat-sheet,
  materials, relay rules, vocabulary) and includes a download link for the slide deck.

## Structure

Three 90-minute days, 17 phase cards:

- **Day 1 · From Syringes to Systems** — force vs. distance, the force-multiplier idea, design and
  first build.
- **Day 2 · Build the Machine** — the main build window, with a searchable failure-mode drawer.
- **Day 3 · Performance Under Pressure** — finish, practice, the multi-robot relay race, and debrief.

## Editing the content

**Do not hand-edit `index.html` — it is generated.** Edit `build.py` and re-run it:

```bash
python3 build.py        # writes index.html
```

All content (objectives, vocabulary, materials, per-phase text, callouts, relay rules) lives as
Python data structures near the top of `build.py`. Slide images, fonts, and logos in `assets/` are
base64-embedded at build time.

## Repo contents

| Path | Role |
|---|---|
| `index.html` | The deliverable. Generated, self-contained, ~4.9 MB. |
| `build.py` | The generator. Edit this, not `index.html`. |
| `assets/` | Slide images, fonts, and logos embedded at build time. |
| `Hydraulic Arm 2026_Final_web.pptx` | The editable slide deck the guide links to (~21 MB). |

## Deploying updates

This repo is served by GitHub Pages from `main` / root. After editing:

```bash
python3 build.py
git add -A && git commit -m "Update guide" && git push
```

GitHub Pages redeploys automatically in about a minute.
