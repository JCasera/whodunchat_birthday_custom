#!/usr/bin/env python3
"""Generate guess-options.js decoy names from perindigo's Twitch chat logs.

Data source: tv.supa.sh -> https://logs.zonian.dev/ (a JustLog proxy, CORS-open).
There is no aggregate "all chatters" endpoint, so we enumerate the daily
message archives, de-duplicate by Twitch user-id, and emit a static
WHODUNCHAT_OPTIONS array (used as wrong-answer decoys in the game).

The 10 roster people from data.js are excluded so they remain roster-only
guess targets. Bots and the broadcaster are intentionally kept ("include
everyone").

Re-running is cheap: each day's raw JSON is cached under cache/ so only
missing/failed days are re-downloaded.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

CHANNEL = "perindigo"
BASE = "https://logs.zonian.dev"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
OUT = os.path.join(HERE, "guess-options.js")
DATA_JS = os.path.join(HERE, "data.js")
DELAY = 0.1


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "whodunchat-build/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def roster_exclude():
    excl = set()
    try:
        txt = open(DATA_JS, encoding="utf-8").read()
        for m in re.finditer(r'id:\s*"([^"]+)"', txt):
            excl.add(m.group(1).lower())
        for m in re.finditer(r'name:\s*"([^"]+)"', txt):
            excl.add(m.group(1).lower())
    except OSError:
        pass
    return excl


def main():
    os.makedirs(CACHE, exist_ok=True)
    exclude = roster_exclude()
    print(f"[build] excluding {len(exclude)} roster names/ids")

    listing = fetch_json(f"{BASE}/list?channel={CHANNEL}")
    days = listing.get("availableLogs", [])
    print(f"[build] {len(days)} days available")

    chatters = {}
    done = 0
    for d in days:
        y, m, day = d.get("year"), d.get("month"), d.get("day")
        if y is None or m is None or day is None:
            continue
        y, m, day = int(y), int(m), int(day)
        cname = f"{y}-{m:02d}-{day:02d}.json"
        path = os.path.join(CACHE, cname)
        msgs = None
        if os.path.exists(path):
            try:
                msgs = json.load(open(path, encoding="utf-8")).get("messages", [])
            except Exception:
                msgs = None
        if msgs is None:
            url = f"{BASE}/channel/{CHANNEL}/{y}/{m}/{day}?jsonBasic=1"
            try:
                data = fetch_json(url)
                msgs = data.get("messages", [])
                json.dump(data, open(path, "w", encoding="utf-8"))
            except Exception as e:
                print(f"[warn] {cname}: {e}")
                continue
        for msg in msgs:
            tags = msg.get("tags") or {}
            uid = tags.get("user-id")
            if not uid:
                continue
            name = msg.get("displayName") or tags.get("display-name") or ""
            if not name:
                continue
            if name.lower() in exclude:
                continue
            entry = chatters.get(uid)
            if entry is None:
                chatters[uid] = {"id": uid, "name": name, "count": 1}
            else:
                entry["count"] += 1
        done += 1
        if done % 25 == 0:
            print(f"[build] processed {done}/{len(days)} days, {len(chatters)} chatters so far")
        time.sleep(DELAY)

    result = list(chatters.values())
    result.sort(key=lambda e: e["count"], reverse=True)
    print(f"[build] {len(result)} unique chatters (after exclusions)")

    lines = []
    lines.append("// ============================================================================")
    lines.append("// GUESS POOL - decoy options auto-generated from perindigo's Twitch chat logs")
    lines.append("// (tv.supa.sh -> logs.zonian.dev) for the last ~12 months.")
    lines.append("// Regenerate with: python3 build_chatters.py")
    lines.append("// Roster people from data.js are excluded and added automatically at runtime,")
    lines.append("// so only community chatters (incl. bots and the broadcaster) are listed here.")
    lines.append("// ============================================================================")
    lines.append("")
    lines.append("window.WHODUNCHAT_OPTIONS = [")
    body = ",\n".join(
        "  { name: " + json.dumps(e["name"]) + ", id: " + json.dumps(e["id"]) +
        ", messages: " + str(e["count"]) + " }" for e in result
    )
    lines.append(body)
    lines.append("];")
    lines.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print(f"[build] wrote {OUT}")


if __name__ == "__main__":
    main()
