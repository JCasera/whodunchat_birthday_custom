// ============================================================================
// ROSTER DATA — these people can be the guessing target.
// Edit freely; keep the structure. See README.md for field-by-field notes.
// ============================================================================

window.WHODUNCHAT_DATA = {
  channel: "yourchannel",

  people: [
    {
      id: "chatterbox",
      name: "ChatterBox",
      followedAt: "2021-03-14", // hint: newer/older follower
      subMonths: 18, // hint: subbed longer/less (null = not a sub)
      messages: 1240, // hint: talks more/less (chat participation)
      statements: [
        "did someone clip that we gotta see it",
        "wait no i think it was yesterday actually",
        "LMAOOO that mod is on fire today",
        "first time catching this stream live btw",
        "can we get a hype train going chat",
        "alright who else is staying for the whole thing",
        "the vod will save this right? right?"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    },
    {
      id: "quiet-grace",
      name: "QuietGrace",
      followedAt: "2024-08-02",
      subMonths: null,
      messages: 87,
      statements: [
        "hello everyone :)",
        "that was really well explained, thanks",
        "this is so relaxing to watch",
        "goodnight all, see you next time",
        "congrats on the milestone!",
        "I mostly lurk but this is a nice community"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    },
    {
      id: "mod-mike",
      name: "ModMike",
      followedAt: "2019-11-20",
      subMonths: 41,
      messages: 3120,
      statements: [
        "keep it civil in here chat",
        "that's a timeout, no warnings",
        "answer's been said twice already in chat",
        "mute the mic if you're not talking please",
        "raid incoming, everyone say hi",
        "rules are on the left, read them"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    },
    {
      id: "night-owl",
      name: "NightOwl",
      followedAt: "2023-01-08",
      subMonths: 6,
      messages: 640,
      statements: [
        "i'm only here because the other stream ended lol",
        "3am gang where you at",
        "this is the calmest stream i've seen all night",
        "chat are we serious right now",
        "somebody's gotta stay awake to watch the raid",
        "ok i'm passing out after this one for real"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    },
    {
      id: "raidboss-k",
      name: "RaidBossK",
      followedAt: "2022-06-19",
      subMonths: 12,
      messages: 980,
      statements: [
        "everyone type LETS GO in 3, 2, 1",
        "we came from [REDACTED]'s stream, huge raid",
        "if you're new here the catch phrase is WAGMI",
        "that was a 120 person raid, new record chat",
        "give it up for the host you don't have to",
        "raiding out in 5, say your goodbyes"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    },
    {
      id: "sneaky-sam",
      name: "sneaky_sam",
      followedAt: "2025-02-27",
      subMonths: null,
      messages: 45,
      statements: [
        "first",
        "pepega",
        "yo",
        "pog",
        "nice",
        "LUL"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    },
    {
      id: "gramps",
      name: "GrampsPlays",
      followedAt: "2018-04-02",
      subMonths: 55,
      messages: 540,
      statements: [
        "back in my day we didn't have emotes, we had words",
        "son, that's not how you hold a controller",
        "i've been here since before the subscriber count had a comma",
        "kids these days with their 7tv emotes",
        "turn the music down, i can't hear the game",
        "i'll be in the garden if anyone needs me"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    },
    {
      id: "clip-kat",
      name: "ClipKat",
      followedAt: "2020-10-11",
      subMonths: 24,
      messages: 1580,
      statements: [
        "that moment is getting clipped immediately",
        "i already have the clip saved, title suggestions?",
        "mods get this man a highlight",
        "this is going on the comp for sure",
        "pov: you missed the clip because you blinked",
        "someone make that a soundbite"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    },
    {
      id: "new-kid",
      name: "NewKidEli",
      followedAt: "2026-07-30",
      subMonths: null,
      messages: 12,
      statements: [
        "hi i just found this stream",
        "what game is this?",
        "how do i follow",
        "can you say hi to my mom",
        "what does sub mean",
        "this is cool, i'll come back"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    },
    {
      id: "money-mutt",
      name: "MoneyMutt",
      followedAt: "2019-12-01",
      subMonths: 36,
      messages: 2210,
      statements: [
        "i subscribed again, we're at 40 months now",
        "gifted 5 subs to whoever's lurking",
        "take my bits, take them all",
        "this stream is my entire personality",
        "i will not be taking questions",
        "my wallet is crying but i'm not"
      ],
      videoWin: "https://drive.google.com/file/d/REPLACE_WIN/view?usp=sharing",
      videoLose: "https://drive.google.com/file/d/REPLACE_LOSE/view?usp=sharing"
    }
  ]
};