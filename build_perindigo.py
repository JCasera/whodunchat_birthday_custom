#!/usr/bin/env python3
"""Build the perindigo person entry for the whodunchat game.

perindigo (the broadcaster) is added as a guessable person. Statements are
sourced from perindigo's OWN chat messages in the cached daily logs
(cache/*.json, fetched earlier from logs.zonian.dev for channel perindigo,
spanning ~2025-08-21 -> 2026-08-19).

Pipeline:
  1. Keep only messages where the speaker is perindigo (displayName /
     tags["display-name"] == "perindigo", case-insensitive). Bots such as
     StreamElements are separate displayNames and are excluded automatically.
  2. Drop bot/template lines: empty/whitespace, URLs, commands (start with !),
     and automated patterns (summon/gacha/ad-break/raid-host boilerplate).
  3. Dedupe exact repeats.
  4. Balanced selection to TARGET statements: score each line as "obvious"
     (contains a perin* emote or streamer-context keywords) vs "hard"
     (generic reactions / short / emote-spam), then stratified-sample a mix
     of both so the guess isn't trivially easy or hard.
  5. Emit ONLY the perindigo person object as JS to stdout (insert into data.js).
     Progress/summary lines go to stderr so they don't pollute the output.

Run: python3 build_perindigo.py > perindigo_block.txt
"""

import json
import glob
import os
import re
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
TARGET = 1500
SEED = 42

# emote tokens in emotes.js for perindigo all start with "perin"
PERIN_EMOTE = re.compile(r"\bperin[A-Za-z0-9]+\b")
URL_RE = re.compile(r"https?://|www\.", re.I)

# Automated / template patterns posted under perindigo's name (chat bot game,
# gacha, ad-breaks, raid/host welcomes). These are not genuine chatter.
TEMPLATE_RE = re.compile(
    r"(has been summoned into"
    r"|is currently a level"
    r"|you have rolled:"
    r"|rarity"
    r"|perishin indmpact"
    r"|congrats .*! you have"
    r"|ad warriors"
    r"|pause the fight"
    r"|back after ad"
    r"|thank u so much for raid"
    r"|welcome in"
    r"|send some love over to)",
    re.I,
)

OBVIOUS_KEYWORDS = re.compile(
    r"(adge|raid|fusion|peri|refill|welcome|break|stream|"
    r"\bim \b|\bwe will\b|\bi am\b|\blet's\b|\blets\b|\bmy \b)",
    re.I,
)


def is_perindigo(msg):
    dn = str(msg.get("displayName", "")).lower()
    if dn == "perindigo":
        return True
    tags = msg.get("tags") or {}
    return str(tags.get("display-name", "")).lower() == "perindigo"


def is_template(text):
    if not text or not text.strip():
        return True
    if URL_RE.search(text):
        return True
    if text.lstrip().startswith("!"):
        return True
    if TEMPLATE_RE.search(text):
        return True
    return False


def is_obvious(text):
    if PERIN_EMOTE.search(text):
        return True
    if OBVIOUS_KEYWORDS.search(text):
        return True
    return False


def log(msg):
    print(msg, file=sys.stderr)


def main():
    files = sorted(glob.glob(os.path.join(CACHE, "*.json")))
    raw = []
    for f in files:
        try:
            data = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for m in data.get("messages", []):
            if is_perindigo(m):
                raw.append(m.get("text", ""))

    log("[build] perindigo raw messages: %d" % len(raw))

    seen = set()
    clean = []
    for t in raw:
        if is_template(t):
            continue
        key = t.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        clean.append(t.strip())

    log("[build] after template-filter + dedupe: %d" % len(clean))

    obvious = [t for t in clean if is_obvious(t)]
    hard = [t for t in clean if not is_obvious(t)]
    log("[build] obvious: %d | hard: %d" % (len(obvious), len(hard)))

    rng = random.Random(SEED)
    # ~60% obvious / ~40% hard, filling from the other bucket on shortfall.
    want_obvious = min(len(obvious), int(TARGET * 0.6))
    want_hard = min(len(hard), TARGET - want_obvious)
    if want_obvious < int(TARGET * 0.6):
        want_obvious = min(len(obvious), want_obvious + (TARGET - want_obvious - want_hard))
    if want_hard < TARGET - int(TARGET * 0.6):
        want_hard = min(len(hard), want_hard + (TARGET - want_obvious - want_hard))

    sel = rng.sample(obvious, want_obvious) + rng.sample(hard, want_hard)
    rng.shuffle(sel)
    sel = sel[:TARGET]
    log("[build] selected: %d (obvious %d, hard %d)" % (len(sel), want_obvious, want_hard))

    lines = []
    lines.append("    {")
    lines.append('      id: "perindigo",')
    lines.append('      name: "perindigo",')
    lines.append("      followedAt: null, // broadcaster; backfill later")
    lines.append("      subMonths: null, // broadcaster; backfill later")
    lines.append("      messages: " + str(len(sel)) + ", // selected statement count")
    lines.append("      statements: [")
    for t in sel:
        esc = t.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").replace("\r", " ")
        lines.append('        "' + esc + '",')
    lines.append("      ],")
    lines.append('      videoWin: "https://drive.google.com/file/d/1y-oYjVZRtKv3Q4Cb5f3-hUGXLLgp-kfY/view?usp=sharing",')
    lines.append('      videoLose: "https://drive.google.com/file/d/1aKbvIFGdoLgHOGThAfnZdy6sV6kUe4z9/view?usp=sharing"')
    lines.append("    },")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
