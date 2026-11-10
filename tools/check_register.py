#!/usr/bin/env python3
"""Check tools/perishable.json against the lessons.

Reports three things: phrases that no longer appear in the lesson text (the
lesson was edited and the register was not), figures past their trust period,
and figures that have never been confirmed against a source.

    python3 tools/check_register.py            # full report
    python3 tools/check_register.py --strict   # exit 1 if any phrase is missing
"""
import datetime, glob, json, os, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
text = "".join(open(p, encoding="utf-8").read()
               for p in sorted(glob.glob(os.path.join(root, "assets/js/content/*.js"))))
items = json.load(open(os.path.join(root, "tools/perishable.json"), encoding="utf-8"))["items"]
today = datetime.date.today()
missing, overdue, unconfirmed = [], [], []
for it in items:
    if it["text"] not in text:
        missing.append(it)
        continue
    if not it["checked"]:
        unconfirmed.append(it)
        continue
    d = datetime.date.fromisoformat(it["checked"])
    age = (today.year - d.year) * 12 + today.month - d.month
    if age >= it["months"]:
        overdue.append((age, it))

def show(title, rows):
    print("%s: %d" % (title, len(rows)))
    for r in rows:
        it = r[1] if isinstance(r, tuple) else r
        extra = " (%d months old)" % r[0] if isinstance(r, tuple) else ""
        print("  %-5s %s%s" % (it["lesson"], it["text"], extra))

print("%d figures registered" % len(items))
show("Phrase not found in the lessons", missing)
show("Past its trust period", overdue)
show("Never confirmed against a source", unconfirmed)
if "--strict" in sys.argv and missing:
    sys.exit(1)
