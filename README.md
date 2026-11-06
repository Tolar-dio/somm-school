# Tastevin Academy

A free, self-paced online sommelier school modeled on the two major programs:

- **Floor track** (Court of Master Sommeliers model): Introductory → Certified → Advanced → Master Sommelier. Deductive blind tasting against the clock, service standards, salesmanship, wine-list math.
- **Analyst track** (WSET → Master of Wine model): Level 2 → Level 3 → Diploma → MW capstone. The Systematic Approach to Tasting, quality assessment, written answers and essays.

## What's inside

- **101 lessons** across 15 units: history and wine law, viticulture and winemaking science (Diploma D1 depth), sparkling and fortified production (D4/D5 depth), the global wine business (D2), grapes, every major region (with deep dives on Bordeaux and the Right Bank, Burgundy, Chablis, Beaujolais, Champagne, Languedoc-Roussillon, Provence, Jura, Savoie, the South West, the Loire, Alsace, the Rhône, Piedmont, Tuscany, Northeast and Southern Italy, Italy's rulebook region by region, Spain's new pyramids, Portugal, Germany, Austria, Greece, Hungary and Tokaj (2026 rules), Switzerland, the Balkans, Georgia, California, Oregon, Washington, Canada, Australia, New Zealand, Argentina, Chile and South Africa), the CMS 2025 service standards, wine-list economics and 2026 market data, spirits law, beer, sake and cider, the real exam formats, and capstone exam craft. Each lesson has a CMS lens, a WSET lens, key terms and an exam (80% to pass).
- **825 exam questions** feeding timed mock exams at the real formats and pass marks, with prerequisites: each level's exam unlocks only after the seal before it.
- **Tasting Lab**: virtual blind flights, CMS deductive grid and WSET SAT forms for real wines with benchmark comparison, profile drills, 60 classic wine profiles, a 20-week confusion-pair rotation, and a tasting journal.
- **Tasting Night**: pick a flight, enter a friend's number, and your Messages app opens with a prewritten text containing a shopping list and a private host card (setup steps and answer key). Nothing is sent or stored by the site.
- **Service Floor**: service sequences, serving temperatures, business math generator, wine-list correction.
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
```

Independent and unaffiliated with the Court of Master Sommeliers, WSET, the Institute of Masters of Wine, the Society of Wine Educators or the Wine Scholar Guild. Exam formats follow their published guides; all lesson text and questions are original.
