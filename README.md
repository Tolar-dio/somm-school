# Vitis Mundi Academy

The school half of [Vitis Mundi](https://vitismundi.app), live at **https://vitismundi.app/academy/**. This repo is the source; `pipeline/frontend/sync_academy.py` in Tolar-dio/wine-world copies it into that site.

A free, self-paced online sommelier school modeled on the two major programs:

- **Floor track** (Court of Master Sommeliers model): Introductory → Certified → Advanced → Master Sommelier. Deductive blind tasting against the clock, service standards, salesmanship, wine-list math.
- **Analyst track** (WSET → Master of Wine model): Level 2 → Level 3 → Diploma → MW capstone. The Systematic Approach to Tasting, quality assessment, written answers and essays.

## What's inside

- **107 lessons** (about 81,000 words; roughly 20 hours of reading and quizzes) across 15 units: soils and geology, grape families and synonyms, rosé, classic pairings and cheese, cocktail families, a full vintage chart, history and wine law, viticulture and winemaking science (Diploma D1 depth), sparkling and fortified production (D4/D5 depth), the global wine business (D2), grapes, every major region (with deep dives on Bordeaux and the Right Bank, Burgundy, Chablis, Beaujolais, Champagne, Languedoc-Roussillon, Provence, Jura, Savoie, the South West, the Loire, Alsace, the Rhône, Piedmont, Tuscany, Northeast and Southern Italy, Italy's rulebook region by region, Spain's new pyramids, Portugal, Germany, Austria, Greece, Hungary and Tokaj (2026 rules), Switzerland, the Balkans, Georgia, California, Oregon, Washington, Canada, Australia, New Zealand, Argentina, Chile and South Africa), the CMS 2025 service standards, wine-list economics and 2026 market data, spirits law, beer, sake and cider, the real exam formats, and capstone exam craft. Each lesson has a CMS lens, a WSET lens, key terms and an exam (80% to pass).
- **About 1,200 exam questions** feeding timed mock exams at the real formats and pass marks, with prerequisites: each level's exam unlocks only after the seal before it. A paper left running keeps its clock and follows you as a bar; questions you miss collect in **Review your misses** until you answer them correctly.
- **14 short-answer questions and 20 essay prompts** (including the 2026 MW themes) for the written papers, self-marked against marking points and a rubric.
- **Tasting Lab**: virtual blind flights, CMS deductive grid and WSET SAT forms for real wines with benchmark comparison, profile drills, 75 classic wine profiles, a 20-week confusion-pair rotation, and a tasting journal.
- **Tasting Night**: pick a flight, enter a friend's number, and your Messages app opens with a prewritten text containing a shopping list and a private host card (setup steps and answer key). Nothing is sent or stored by the site.
- **Service Floor**: six service sequences to the 2025 Court standard, serving temperatures, business math generator, seven wine lists to correct.
- **Drills**: Label Lab (fictional producers, real label law) and CMS-style matching.
- **Flashcards** with spaced repetition, a **study planner**, and a **library**.

Progress is stored in the browser (localStorage), with backup and restore to a JSON file.

## Run it

No build step. Open `index.html`, or serve the folder with any static server. Deployed with GitHub Pages from the `main` branch root.

## Structure

```
index.html
assets/css/style.css
assets/js/content/   lessons and quizzes (one file per curriculum part)
assets/js/data/      wine profiles, drills, shopping guide, label lab, matching
assets/js/*.js       core, lab, floor, exam engine, learn views, tasting night, drills, app/router
tools/               build_atlas_index.py (atlas links for region lessons)
```

## Editing questions

Each quiz row is `[difficulty 1-3, question, correct answer, [three distractors], explanation]`. Two rules keep the exams honest:

- Keep the correct answer about the same length as the distractors. A test-wise student picks the longest option; before the November 2026 review that strategy scored 56%, enough to pass the WSET-style mocks. It now scores about 46%. Don't let it creep back up.
- `14-exam-bank.js` loads after every lesson file, and its first column is the lesson id that decides which unit and which mocks draw the question. An unknown id logs a console warning.

Append new questions to the end of a lesson's quiz array: the "Review your misses" record is keyed by lesson id and position. Every lesson lives whole in one content file; nothing patches a lesson from another file.

Independent and unaffiliated with the Court of Master Sommeliers, WSET, the Institute of Masters of Wine, the Society of Wine Educators or the Wine Scholar Guild. Exam formats follow their published guides; all lesson text and questions are original.
