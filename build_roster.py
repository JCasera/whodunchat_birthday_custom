import json, glob, os, re

import filters

HANDLES = [
    ("raechuu", "Raechuu"),
    ("chrysaliacsilla", "ChrysaliaCsilla"),
    ("pocketchalk", "Pocketchalk"),
    ("laavispa", "LaAvispa"),
    ("yura", "Yura"),
    ("purrodie", "Purrodie"),
    ("eikkop", "EikkoP"),
    ("jackiemeyers", "JackieMeyers"),
    ("spellydoesart", "Spellydoesart"),
    ("dearninette", "dearNinette"),
]

NAME = {h: n for h, n in HANDLES}

VIDEO_WIN = "https://drive.google.com/file/d/1y-oYjVZRtKv3Q4Cb5f3-hUGXLLgp-kfY/view?usp=sharing"
VIDEO_LOSE = "https://drive.google.com/file/d/1aKbvIFGdoLgHOGThAfnZdy6sV6kUe4z9/view?usp=sharing"
VIDEO_ALT_WIN = "Victory video coming soon \u2014 great work closing this case!"
VIDEO_ALT_LOSE = "Farewell video coming soon \u2014 the suspect still walked!"

def keep(text):
    t = text.strip()
    if not t:
        return False
    if len(t) > 300:
        return False
    if filters.is_template(t):
        return False
    return True

# Pass 1: collect the set of user-ids that belong to each handle.
uid_sets = {h: set() for h, _ in HANDLES}
files = sorted(glob.glob("cache/*.json"))
for f in files:
    for m in json.load(open(f))["messages"]:
        dn = (m.get("displayName") or "").lower()
        uid = (m.get("tags") or {}).get("user-id")
        for h, _ in HANDLES:
            if dn == h and uid:
                uid_sets[h].add(uid)
                break

# Pass 2: gather each person's messages by user-id, filter + exact dedupe.
msgs = {h: [] for h, _ in HANDLES}
seen = {h: set() for h, _ in HANDLES}
for f in files:
    for m in json.load(open(f))["messages"]:
        uid = (m.get("tags") or {}).get("user-id")
        text = m.get("text") or ""
        for h, _ in HANDLES:
            if uid and uid in uid_sets[h]:
                if text not in seen[h] and keep(text):
                    seen[h].add(text)
                    msgs[h].append(text)
                break

# Pass 3: per-person near-duplicate (templated) removal, keep-one per cluster.
for h, _ in HANDLES:
    msgs[h], _short_dups = filters.near_dedupe(msgs[h])

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

lines = []
lines.append("// ============================================================================")
lines.append("// ROSTER DATA - these people can be the guessing target.")
lines.append("// Rebuilt from perindigo channel chat logs (cache/), full available history.")
lines.append("// See README.md for field-by-field notes.")
lines.append("// ============================================================================")
lines.append("")
lines.append("window.WHODUNCHAT_DATA = {")
lines.append('  channel: "happybirthday",')
lines.append("")
lines.append("  people: [")
for h, n in HANDLES:
    stmts = msgs[h]
    lines.append("    {")
    lines.append("      id: " + js_str(h) + ",")
    lines.append("      name: " + js_str(n) + ",")
    lines.append("      followedAt: null,")
    lines.append("      subMonths: null,")
    lines.append("      messages: " + str(len(stmts)) + ",")
    lines.append("      statements: [")
    for s in stmts:
        lines.append("        " + js_str(s) + ",")
    lines.append("      ],")
    lines.append("      videoWin: " + js_str(VIDEO_WIN) + ",")
    lines.append("      videoLose: " + js_str(VIDEO_LOSE) + ",")
    lines.append("      videoAltWin: " + js_str(VIDEO_ALT_WIN) + ",")
    lines.append("      videoAltLose: " + js_str(VIDEO_ALT_LOSE))
    lines.append("    },")
lines.append("  ]")
lines.append("};")
lines.append("")

with open("data.js", "w", encoding="utf-8") as out:
    out.write("\n".join(lines))

print("[build] wrote data.js")
for h, n in HANDLES:
    print("  %-18s %s -> %d statements" % (h, n, len(msgs[h])))
print("[build] total statements:", sum(len(v) for v in msgs.values()))
