#!/usr/bin/env python3
"""Check that facts stated in several lessons agree.

Reads tools/shared_facts.json, finds every statement of each fact in the
lesson text and quiz rows, and reports any whose number differs from the
agreed value.

    python3 tools/check_consistency.py        # mismatches only
    python3 tools/check_consistency.py -v     # also list where each fact lives
"""
import glob, json, os, re, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lessons = []  # (id, text)
for p in sorted(glob.glob(os.path.join(root, "assets/js/content/*.js"))):
    src = open(p, encoding="utf-8").read()
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'L\.push\(\{id:"([a-z0-9]+)"', src)]
    for i, (pos, lid) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(src)
        lessons.append((lid, re.sub(r"<[^>]+>", "", src[pos:end])))
facts = json.load(open(os.path.join(root, "tools/shared_facts.json"), encoding="utf-8"))["facts"]
bad = unused = 0
for f in facts:
    rx, where, wrong = re.compile(f["pattern"]), {}, []
    for lid, text in lessons:
        for m in rx.finditer(text):
            v = next(g for g in m.groups() if g)
            where.setdefault(lid, set()).add(v)
            if v not in f["expect"]:
                wrong.append((lid, v, text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")))
    if not where:
        unused += 1
        print("NOT FOUND  %s" % f["fact"])
    for lid, v, ctx in wrong:
        bad += 1
        print("MISMATCH   %s: %s says %s, expected %s\n           ...%s..." % (f["fact"], lid, v, " or ".join(f["expect"]), ctx))
    if "-v" in sys.argv and where:
        print("ok  %-44s %s" % (f["fact"], ", ".join(sorted(where))))
print("%d facts checked, %d mismatches, %d patterns matched nothing" % (len(facts), bad, unused))
sys.exit(1 if bad else 0)
