# whodunchat — happy birthday fan copy

A **happy birthday fan copy** of [whodunchat](https://whodunchat.ducksaint.com), the original guessing game by **DuckSaint**. It uses a **fixed** set of people and chat messages instead of live Twitch logs.

This was copied on purpose to make a one-off birthday game — it is **not** the full whodunchat experience. Go play the real thing at **[whodunchat.ducksaint.com](https://whodunchat.ducksaint.com)**.

## Credits

- **whodunchat** is the original creation of **[DuckSaint](https://whodunchat.ducksaint.com)** — all credit for the idea and design goes to them. Play the real site at https://whodunchat.ducksaint.com.
- This repository is an unofficial birthday fan copy built from that game's design; it is not affiliated with or endorsed by DuckSaint.

## Running it

Just double-click `index.html` (open it in a browser). No build step, no server required.

Optional: if you prefer, serve it over HTTP:

```
python3 -m http.server 8000
```

then open `http://localhost:8000`.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole app: styles + logic. Open this. |
| `data.js` | **Roster** — the people who can be the guessing target. |
| `guess-options.js` | **Guess pool** — extra names shown as guesses (decoys). |

## Editing the data

### `data.js` — roster

```js
{
  id: "chatterbox",                 // unique key; used for "once per run" exclusion
  name: "ChatterBox",               // displayed name
  followedAt: "2021-03-14",         // date followed -> hint: newer/older follower
  subMonths: 18,                    // months subbed -> hint: subbed longer/less (null = not a sub)
  messages: 1240,                   // chat participation -> hint: talks more/less
  statements: [ "...", "...", ... ], // chat lines; at least 4
  videoWin:  "https://drive.google.com/file/d/FILE_ID/view?usp=sharing", // optional (Phase 3)
  videoLose: "https://drive.google.com/file/d/FILE_ID/view?usp=sharing",  // optional (Phase 3)
  videoAltWin:  "Victory video coming soon!",  // optional fallback text (win)
  videoAltLose: "Farewell video coming soon!"  // optional fallback text (lose)
}
```

- Every roster person needs at least **4 statements**; extra ones are never shown to the player.
- `videoWin` / `videoLose` are for Phase 3 (outcome videos). Share the file as **Anyone with the link → Viewer**, then paste the share link. `REPLACE_WIN` / `REPLACE_LOSE` are placeholders — any URL containing `REPLACE_` is treated as "no video" and the embed is skipped.
- `videoAltWin` / `videoAltLose` are the fallback texts shown in place of the player when no video link is set (`null`, blank, `REPLACE_`, or unparseable) — win and lose versions respectively. Edit them per person in `data.js` (they are also emitted by `build_roster.py` / `build_perindigo.py`, so rebuilds keep them). Omit one to fall back to "Video unavailable."
- On load, the app validates the data and prints warnings to the browser console (F12) if anything is off.

### `guess-options.js` — guess pool

```js
window.WHODUNCHAT_OPTIONS = [
  { id: "mod-mike", name: "ModMike" },  // already in roster -> de-duplicated
  { name: "chatternum" }                // decoy
];
```

Roster people are added automatically. Duplicates are matched by `id` first, else by name (case-insensitive). List here anything you want as a guessable decoy that isn't in the roster.

Decoys may carry the same hint stats as roster people (`followedAt`, `subMonths`, `messages`) if you want their "nothing to compare" guesses to show real hints instead; the app validates these if present.

## How the game works

- A random roster person becomes the target (each person is a target at most **once per run**; **drop case** puts the current person back in the pool and the next open randomizes a new target).
- Their first random statement is shown; type a name to guess who said it (autocomplete + the 3 closest-name quick picks help avoid typos).
- Correct → move to the next person.
- Wrong → another statement is revealed plus hints comparing the target to your guess:
  - `followedAt` — earlier / later / about the same time (within ±7 days)
  - `subMonths` — longer / shorter / about as long (within ±1 month)
  - `messages` — more / less / about as much (within ±25%)
  - if the guess has no comparable stats → "nothing to compare"
- **Four misses** → the suspect walks and the answer is revealed. After any round you are taken to the **outcome page**: the win/lose video (Drive `/preview` embed, if a real link is set), who the answer was with their profile stats, guesses used, run progress and streak, plus **continue** (next case) and **back to the front page** buttons.
- A win streak (consecutive wins) and per-person records (guesses + identified/walked) are tracked and shown on the front page and the **case statistics** screen.

## Progress & reset

- Targets are stored in `sessionStorage` — they survive a page refresh but are cleared when you close the tab.
- **Stats (streak, longest streak, records, totals) persist for the whole session** and only reset when you close the tab.
- **"start a fresh run"** on the home page reopens the target pool but keeps your stats.

## Phases

- **Phase 1:** home page, app shell, data loading/validation, guess-pool merge, progress tracking, screen navigation.
- **Phase 2:** the guessing game screen — progressive statements, typed guessing with autocomplete + closest-name quick picks, comparison hints, win/lose flow, statement pips, win streak, and per-person records.
- **Phase 3:** per-person win/lose videos (Google Drive `/preview` embeds) on the outcome page, and the case statistics screen. Videos need the file shared as **Anyone with the link → Viewer** to play; `REPLACE_` placeholder links are skipped.
