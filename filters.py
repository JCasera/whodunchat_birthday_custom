"""Shared template/command filtering for the whodunchat build scripts.

A "template" message is an automated/bot/system line (sub notices, raid/host
welcomes, gacha/quiz bot output, ad-game spam, etc.) rather than a genuine
chat statement. These are matched by clear system/bot phrasing so that normal
conversation is not accidentally dropped.
"""

import re

# Each fragment is matched case-insensitively anywhere in the line.
TEMPLATE_PATTERNS = [
    # StreamElements quiz/gacha bot output
    r"your type is",
    r"streamelements",
    r"you have rolled",
    r"has been summoned",
    r"is currently a level",
    r"rarity",
    r"perishin",
    # Subscription / gift / resub notices
    r"subscribed",            # "subscribed at Tier 1", "has subscribed for N", "just subscribed"
    r"resubbed",
    r"re-subbed",
    r"has gifted",
    r"is gifting",
    r"gifted a sub",
    # Raid / host notices
    r"raided",
    r"now hosting",
    r"hosted by",
    r"is hosting",
    # Ad-game spam
    r"ad warriors",
    r"pause the fight",
    r"back after ad",
    # Raid welcome
    r"welcome in",
    r"send some love over to",
    r"thank u so much for raid",
    # Misc system
    r"yapped into",
    r"congrats .*? you have",
    r"prime sub",
    r"hype train",
    r"new follower",
    r"has followed",          # "X has followed! :)" follow-notification bot
    r"followed the channel",
    r"radio queue cleared",   # song-request bot notice
    r"queue cleared",         # song-request bot notice (variants)
    # Duel game bot output
    r"has accepted the duel against",
    r"has declined the duel",
    r"for winning the duel",
    r"the duel has ended",
    # Other game / poll / slots / lobby bot output
    r"battleroyale",                                             # win/loss battleroyale stats
    r"\d+\) [A-Za-z0-9_]+: \d+(?:, \d+\) [A-Za-z0-9_]+: \d+)+",  # ranked leaderboards
    r"TTS redeem to answer the question",                        # TTS question bot
    r"the slots",                                                # slots jackpot / win-from-slots
    r"out of \d+ vote",                                          # poll result bot
    r"shoot your avatar",                                        # basketball game bot
    r"lobby id",                                                 # game lobby bot
    r"community challenge",
    # Cheer/bits (guarded so "cheer me up" is kept)
    r"cheer(ed)? \d",
    r"\d+ bits",
]

TEMPLATE_RE = re.compile("|".join("(?:" + p + ")" for p in TEMPLATE_PATTERNS), re.I)


def is_template(text):
    """Return True if `text` is empty, a URL, a command, or a bot/system line."""
    if not text or not text.strip():
        return True
    if re.search(r"https?://|www\.", text, re.I):
        return True
    if text.lstrip().startswith("!"):
        return True
    if TEMPLATE_RE.search(text):
        return True
    return False


import difflib


def _tokens(text):
    return [w.lower() for w in re.split(r"[^A-Za-z0-9]+", text) if w]


def _seq_ratio(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def _greedy_dedupe(statements, threshold):
    """Keep the first of any pair with token-sequence similarity > threshold."""
    kept = []  # list of (token_tuple, text)
    for s in statements:
        t = _tokens(s)
        is_dup = False
        for kt, _ in kept:
            if kt:
                inter = len(set(t) & set(kt))
                union = len(set(t) | set(kt))
                jac = inter / union if union else 0
                # cheap pre-filter: sequence-ratio > threshold implies Jaccard > 0.5
                if jac > 0.5 and _seq_ratio(t, list(kt)) > threshold:
                    is_dup = True
                    break
        if not is_dup:
            kept.append((tuple(t), s))
    return [text for _, text in kept]


def _find_near_dups(items, threshold):
    """Return the short statements that are near-duplicates of another (for review)."""
    toks = [_tokens(s) for s in items]
    out = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if toks[i] and toks[j]:
                inter = len(set(toks[i]) & set(toks[j]))
                union = len(set(toks[i]) | set(toks[j]))
                jac = inter / union if union else 0
                if jac > 0.5 and _seq_ratio(toks[i], toks[j]) > threshold:
                    out.append(items[i]); out.append(items[j]); break
    seen = set(); uniq = []
    for d in out:
        if d not in seen:
            seen.add(d); uniq.append(d)
    return uniq


def near_dedupe(statements, threshold=0.80, min_tokens=4):
    """Remove near-duplicate (templated) statements, keeping one per cluster.

    Only statements with at least `min_tokens` tokens are eligible for removal
    (token-sequence similarity > `threshold` vs an already-kept statement).
    Shorter statements are always kept but reported in the returned
    `short_dups` list for human review.

    Returns (kept, short_dups).
    """
    longs = []
    shorts = []
    for s in statements:
        (longs if len(_tokens(s)) >= min_tokens else shorts).append(s)
    kept_longs = _greedy_dedupe(longs, threshold)
    short_dups = _find_near_dups(shorts, threshold)
    return kept_longs + shorts, short_dups
