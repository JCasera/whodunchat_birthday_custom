# whodunchat (local)

A local guessing game that mimics [whodunchat](https://whodunchat.ducksaint.com), using a **fixed** set of people and chat messages instead of live Twitch logs.

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
  videoLose: "https://drive.google.com/file/d/FILE_ID/view?usp=sharing"  // optional (Phase 3)
}
```

- Every roster person needs at least **4 statements**; extra ones are never shown to the player.
- `videoWin` / `videoLose` are for Phase 3 (outcome videos). Share the file as **Anyone with the link → Viewer**, then paste the share link. `REPLACE_WIN` / `REPLACE_LOSE` are placeholders.
- On load, the app validates the data and prints warnings to the browser console (F12) if anything is off.

### `guess-options.js` — guess pool

```js
window.WHODUNCHAT_OPTIONS = [
  { id: "mod-mike", name: "ModMike" },  // already in roster -> de-duplicated
  { name: "chatternum" }                // decoy
];
```

Roster people are added automatically. Duplicates are matched by `id` first, else by name (case-insensitive). List here anything you want as a guessable decoy that isn't in the roster.

## How the game works

- A random roster person becomes the target (each person is a target at most **once per launch**).
- Their first random statement is shown; pick who you think said it.
- Correct → move to the next person.
- Wrong → another statement is revealed plus three hints comparing the target to your guess (follower date, sub tenure, chat participation).
- Three wrong guesses → the suspect walks and you return to the front page.

## Progress & reset

- Used targets are stored in `sessionStorage` — they survive a page refresh but are cleared when you close the tab (that's a new launch).
- Use **"start a fresh run"** on the home page to reset immediately.

## Phases

- **Phase 1 (current):** home page, app shell, data loading/validation, guess-pool merge, progress tracking, screen navigation.
- **Phase 2:** the guessing game screen (statements, choices, hints, win/lose flow).
- **Phase 3:** per-person win/lose videos (Google Drive embeds) and the results screen.
