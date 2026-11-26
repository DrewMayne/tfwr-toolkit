# Changelog

## 1.0.0 (2026-11-26)

First release. Requires BepInEx 5 (5.4.23.x, Windows x64, Mono).

- Plugin `FasterSimulations.dll` (BepInEx 5) adds four functions to the game, with code tooltips, docs pages and entries
  in `builtins.py`:
  - `simulate_many(filename, sim_unlocks, sim_items, sim_globals, seeds, speedup[, options])` -> list of times
  - `compare(filename_a, filename_b, sim_unlocks, sim_items, sim_globals, seeds, speedup[, options])` -> seqtest dict
    and one printed line
  - `leaderboard_simulate(leaderboard, file_name, seeds, speedup[, options])` -> list of times (nothing submitted)
  - `sim_options([options])` -> all options (set and saved to `BepInEx/config/FasterSimulations.cfg`)
- Options: `workers`, `shared_trees`, `gc_every_mb`, `hot_spots`, `vm`, `stages`, `stage_prefix`, `until`, `detail`, `bound`, `looks`,
  `min_effect`, `max_pairs`, `from`, `to`, `max_game_seconds`, `max_real_seconds`, `in_game_functions`; the first three
  functions take a dict of options as an optional last argument for one call.
- Stage times: every successful `unlock()` and every printed line starting with `@stage ` (0 ticks for unlocks).
- Speed for the mod's own simulations (each behind an option, all on by default, results identical to `simulate()`):
  shared syntax trees for `spawn_drone` (`shared_trees`), garbage collection every N MB (`gc_every_mb`), hot-spot
  paths (`hot_spots`: scheduler copy, dinosaur flood fill, unlock-check cache, token reuse), a bytecode interpreter
  (`vm`, with immutable-tuple sharing for drones). `hot_spots` and `vm` take effect after a restart.
- Safety: `workers` defaults to 0 (simulations run inside the game; no other process is started). Background copies
  (`workers` >= 1) are experimental: started one at a time, killed if not ready in their own folder within 20 s, at
  most one retry, the call fails with an error instead of falling back, and all copies are killed when a call is
  stopped or fails and when the game exits (Windows job object, also on a crash). A `workers` value saved by a
  pre-release build is reset to 0 once. At most 4 copies while BepInEx's disk log is on (BepInEx keeps 5 log files
  per game folder; a 6th BepInEx process started without its mods in our tests). Per-session counts of safety kills and
  retries in `sim_options()`.
- `report_time` option (off by default): one line per call with the real time it took.
- Background copies: a limit from CPU threads and free memory (`workers_recommended`, shown by `sim_options()`), the
  per-dict override `workers_force` (never saved, at most 64), a once-per-session reminder line, and no new copies when
  free memory is under 1 GB.
- Command line switches (used by the background copies and the tests): `-fsdata`, `-fssave`, `-fsautoplay`,
  `-fsnooutput`, `-fsworker`, `-fsparent`, `-fsrun`, `-fsquit`, `-fsnospeed`, `-fsnoshare`, `-fsnohot`, `-fsnovm`, `-fsgcmb`, `-fsnostages`,
  `-fsmaxreal`, `-fsmaxgame`, `-fstesthook`, `-fstestlimits`.
- Tested on The Farmer Was Replaced build b4b1470b15874582b4a2375fb29b0002 (`Core.dll` SHA-256 da7373f9...; Steam,
  Windows): 62 single-process and 15 two-process test cases and the 9-run identical-results check pass with the default options.
