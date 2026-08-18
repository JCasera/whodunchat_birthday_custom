// ============================================================================
// GUESS POOL — every name the player can pick from.
// Roster people from data.js are added automatically and de-duplicated, so
// you only need to list names here that ARE NOT already in the roster.
// Duplicates are matched by id, else by name (case-insensitive).
// ============================================================================

window.WHODUNCHAT_OPTIONS = [
  { id: "mod-mike", name: "ModMike" }, // already in roster -> de-duplicated
  { name: "QuietGrace" }, // already in roster -> de-duplicated
  { name: "chatternum" }, // decoy
  { id: "boomer-bob", name: "BoomerBob" }, // decoy
  { name: "WhisperWendy" }, // decoy
  { name: "DefinitelyNotAClip" }, // decoy
  { name: "ZzZ_Lurker" } // decoy
];