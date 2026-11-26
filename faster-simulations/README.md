# Faster Simulations

A BepInEx 5 mod for The Farmer Was Replaced: `simulate()` for many seeds in one call, faster than calling `simulate()` in a loop, and a paired comparison of two scripts (`compare`) that tells you which one is faster and how sure that is.

## Safety first: your save

**Back up your save folder before you try any mod** (`%USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves`; copy the whole folder somewhere else).

By default (`workers = 0`) the mod runs every simulation **inside the game you are playing**, one after another. It starts no other programs and writes nothing to your saves.

The option `workers` (1 or more) is **EXPERIMENTAL** and off by default. It starts that many hidden copies of the game in the background to run simulations in parallel. The risk, stated plainly: if BepInEx fails to load in one of those copies, that copy is the plain game, and the plain game opens **your real save folder** and autosaves your active save about 38 s after it starts. We saw BepInEx fail in a 5th copy started from the same game folder (it found no free log file), which is why the mod never starts more than 4. The mod also guards against any other cause: it starts copies one at a time, kills any copy that has not reported ready from its own private folder within 20 s (before that first autosave), retries at most once, then stops the call with an error; and it kills all copies when a call is stopped or fails and when the game exits (also if the game crashes). In our tests the guard caught that 5th copy and nothing was written to any save, but the mode is new: only turn `workers` on with a backed-up save.

## Install

1. Find the game folder: in Steam, right-click The Farmer Was Replaced > Manage > Browse local files (the folder with `TheFarmerWasReplaced.exe`).
2. Download BepInEx **5.4.23.x for Windows x64** (for example `BepInEx_win_x64_5.4.23.4.zip` from https://github.com/BepInEx/BepInEx/releases; not BepInEx 6, not the x86 or IL2CPP builds) and unzip it into the game folder, so that `BepInEx\`, `winhttp.dll`, `doorstop_config.ini`, `.doorstop_version` and `changelog.txt` sit next to `TheFarmerWasReplaced.exe`.
3. Create the folder `BepInEx\plugins\` (the BepInEx zip does not contain it; BepInEx would also create it the first time the game starts).
4. Copy `FasterSimulations.dll` into `<game folder>\BepInEx\plugins\`. In this zip it is inside the `FasterSimulations` folder; copying that whole folder into `plugins` works too.
5. Start the game. The functions appear once `simulate` is unlocked (`leaderboard_simulate` once `leaderboard_run` is). If they do not, check `BepInEx\LogOutput.log` for the line `Faster Simulations 1.0.0 loaded`.

To uninstall, delete the DLL (or, to remove BepInEx too, the `BepInEx` folder, `winhttp.dll`, `doorstop_config.ini`, `.doorstop_version` and `changelog.txt`). Scripts that call these functions only run with the mod installed.

## First call

Put your farm code in a file, say `farm`, and in another file run:

```python
times = simulate_many("farm", Unlocks, {}, {}, 10, 1)   # seeds 1..10, same as 10 simulate() calls
print(times)

result = compare("farm", "farm_new", Unlocks, {}, {}, 40, 1)    # which one is faster, and how sure (up to 40 seed pairs)
print(result["verdict"], result["diff"], result["pairs"])
```

The drone waits until the call is done (as with `simulate()`); press stop to cancel. To see how long a call really took, turn on `sim_options({"report_time": True})`: each call then prints one line such as `simulate_many: 10 runs in 49.2 s real time (4.9 s each), 1 process`.

## Make your tests shorter

- **Stop each run where your change stops mattering.** `{"until": "Expand.5"}` as the last argument ends every run at that stage and returns the stage time, e.g. `simulate_many("farm", Unlocks, {}, {}, 20, 1, {"until": "Expand.5"})`. Stages are every `unlock()` (`Expand.5` = Expand reaching level 5) and every printed line starting with `@stage name`.
- **Let `compare` stop early.** Give it a large seed pool (`200`); it checks every 20 pairs and stops as soon as the answer is clear, or as soon as the difference is surely smaller than `min_effect` (0.5 s). A big change usually ends after 20 pairs.
- **Start small.** 10 seeds tell you whether something works at all; 40 pairs is enough for a 1 s change on most farms.

## What this does NOT do

- It does not change the game's own `simulate()`, `leaderboard_run()` or your normal runs: those use the game's code as before.
- It refuses to run inside `leaderboard_run` (and inside simulations), so it cannot be used during a leaderboard attempt.
- It does not change game-clock results: a run takes exactly as many in-game seconds as with `simulate()`; only real time is shorter.
- The mod itself does not submit anything, use the network or call Steam (background copies, if you turn them on, are ordinary copies of the game and start the game's Steam connection as the game does).
- By default it starts no other programs and writes nothing to your saves (the game's own `builtins.py`, which the game rewrites itself, lists the four new functions).

## Using several CPU cores (experimental)

By default every simulation runs inside your game, one after another, on one CPU core. With `sim_options({"workers": N})` the mod instead starts N hidden copies of the game in the background (no window, lower priority) and spreads the runs over them, so N runs go at once.

- **Turn it on:** `sim_options({"workers": 4})` (saved), or for one call only: `simulate_many("farm", Unlocks, {}, {}, 40, 1, {"workers": 4})`. The first time in a game session the mod prints one line reminding you that this is experimental.
- **At most 4 copies.** BepInEx keeps 5 log files per game folder (`LogOutput.log` and `.1` to `.4`); a 6th BepInEx process of the same folder (your game + a 5th copy) finds no free log file and starts without its mods. So with BepInEx's disk log on (the default) the mod never starts more than 4 copies, not even with `workers_force`. (BepInEx can be told not to write the log file, `Enabled = false` under `[Logging.Disk]` in `BepInEx\config\BepInEx.cfg`; the mod then allows more, but that setup was not measured for this release.)
- **How many:** the mod allows at most `workers_recommended` = the smallest of 4, (CPU threads - 2) and (free memory - 2 GB) / 1 GB per copy, counting copies already running as available; `sim_options()` shows `workers_max_cpu`, `workers_max_memory` and `workers_recommended` for your PC. Asking for more is an error that names the numbers. To do it anyway, put `WFORCE` in the same dict as `workers` (`sim_options({"workers": 12, "workers_force": True})` or the same per-call dict); it is never saved, so a saved value above the limit is checked again in the next session. More copies than CPU cores does not make it faster. If free memory falls under 1 GB, the mod starts no further copies and finishes with the ones it has (it says so).
- **What to expect:** the first call starts the copies, one at a time (a few seconds each); later calls reuse them, so they start at once. Results are exactly the same as with `workers = 0`.
- **Memory:** each copy is a whole game (about 0.6 GB each in our measurements, see the table; the limit assumes 1 GB); make sure you have the RAM for N copies plus your game.
- **Turn it off:** `sim_options({"workers": 0})`. The copies close when your game closes, when a call is stopped or fails, and also if the game crashes.

**Back up your Saves folder first.** This mode is experimental. If BepInEx ever fails to load in one of the copies, that copy is the plain game, and the plain game opens your real save and autosaves it about 38 s after it starts. The mod watches for that: a copy that has not reported from its own private folder within 20 s is killed before it can save, the call is retried once and then stops with an error. That guard is new, so keep a backup.

Measured with a full-game program (about 1,600 game seconds per run), 40 seeds, an 8-core / 16-thread desktop CPU, quiet machine, BepInEx disk log on; every result identical to `workers = 0`:

| `workers` | first call (incl. start-up) | later calls (copies already running) | s per run | memory per copy |
|---|---|---|---|---|
| 0 (in the game) | 196 s | 196 s | 4.9 | - |
| 2 | 128 s | 118 s | 2.95 | 0.6 GB |
| 4 | 85 s | 65 s | 1.63 | 0.6 GB |

Start-up is about 5 s per copy (they start one after another). The copies run at lower priority than your game, so the gain is less than N times.

## Functions

```python
simulate_many(filename, sim_unlocks, sim_items, sim_globals, seeds, speedup)
# simulate() once per seed -> list of times (None for a failed run); same times as simulate()
# seeds: a list / range, or N for seeds 1..N

compare(filename_a, filename_b, sim_unlocks, sim_items, sim_globals, seeds, speedup)
# seqtest on the same seeds -> dict, and prints one line, e.g.
# farm_new faster by 2.24 s (+-0.74, 40 pairs, Expand.5 -> Mazes.2)

leaderboard_simulate(leaderboard, file_name, seeds, speedup)
# runs from the leaderboard's start state, nothing submitted -> list of times
# (None for a failed run or a run that missed the goal)

sim_options({"detail": True})   # set options (saved); sim_options() returns them all
```

The first three take an optional last argument, a dict of options for that call only. `speedup` is accepted for symmetry with `simulate()`; the runs go as fast as they can. Each run costs 200 ticks, like one `simulate()` call. All three raise an error inside `leaderboard_run` and inside simulations, and only the main drone can call them. The in-game help (hover a function name, or the docs window) lists every argument, return key and option.

`compare` returns `verdict` (`"a"` / `"b"` = that file is faster, `"none"`, `"undecided"`, `"start_differs"`), `diff` (b − a on the judged segment, seconds), `se`, `z`, `pairs`, `from`, `to`, `before`, `after`, `whole` (each `{"diff", "se"}`), `look`, `errors`.

## Options

Set with `sim_options({...})`, stored in `BepInEx/config/FasterSimulations.cfg` under the same names. Unknown names are an error that lists the valid ones.

```python
workers           0                 # 0 = run in this game (safe default); N >= 1 = N background copies (EXPERIMENTAL, see "Safety first")
shared_trees      True              # drones share stateless parts of the program tree (see below)
gc_every_mb       200               # while simulating: pause the automatic GC, collect every N MB; 0 = game default
stages            True              # record stage times
stage_prefix      "@stage "         # printed lines starting with this are stages
until             None              # stop each run at this stage; its time is the stage time
detail            False             # return dicts: seed, time, finished, error, stages, goal_met, printed
bound             None              # compare: |z| to decide; None = 2.7 (<= 200 pairs), 2.55 (<= 100), 2.3 (<= 40)
looks             None              # compare: pair counts to check at; None = every 20
min_effect        0.5               # compare: stop "none" when |diff| + 2 se < this; 0 = never
max_pairs         200               # compare: most pairs
from              None              # compare: segment start; None = last stage where both are identical
to                None              # compare: segment end; None = first stage where they differ
max_game_seconds  86400             # give up on a run after this much game time
max_real_seconds  1800              # ... or this much real time
hot_spots         True              # faster scheduler / dinosaur / unlock-check / token paths (after a restart); False = game code
vm                True              # run the mod's simulations on a bytecode interpreter (after a restart); False = game interpreter
report_time       False             # print one line per call with the real time it took
in_game_functions True              # add the functions (after a restart)
workers_force     -                 # only together with workers, in the same dict: allow more copies than recommended; never saved
workers_max_cpu, workers_max_memory, workers_recommended   # read-only: what this PC allows (see "Using several CPU cores")
```

## Stages

Every successful `unlock()` in a simulated run records a stage `<Unlock>.<level>` (`Expand.3` = Expand reaching level 3) at the exact game time, for 0 ticks. A printed line starting with `@stage name` adds stage `name` (the print costs its usual ticks). `detail` returns them; `compare` uses them to find the part of the run that changed.

## seqtest (how `compare` decides)

1. Both files run on the same seeds; per seed, d = time(b) − time(a). The luck of a seed mostly cancels.
2. The stages split each run. `from` = the last stage at which a and b are identical on every seed, `to` = the first stage at which they differ: the stage the change acts in. Only that segment is judged, so the noise before and after it does not count. `before`, `after` and `whole` are reported as well, so a change that gives time back later shows up.
3. At each look (every 20 pairs) it computes mean d, se = sd/√n, z = mean/se. It decides when |z| ≥ `bound`, stops with `"none"` when |mean| + 2 se < `min_effect`, and otherwise adds pairs up to `max_pairs`.
4. If `before` moved by more than 2.5 se (possible only with your own `from`), the verdict is `"start_differs"`.

Keep the code before your change tick-identical: new top-level code or `def`s in a module that loads at the start shift every later tick, and the segment then starts at the beginning of the run. After picking a winner among several variants on the same seeds, check it on new seeds.

Measured properties, from paired full-run comparisons (11 real paired comparisons, resampled 20,000 times each, and a check on 200 fresh seeds). False "faster" rate on a no-effect change, either direction, with looks every 20 pairs up to 200: 20 % at bound 2.0, 6.5 % at 2.555 (Pocock), 4.4-4.8 % at the default 2.7 (2-2.5 % on heavy-tailed segments); a real one-tick change gave no verdict in 200 pairs. An injected 1.0 s delay (segment sd 2.9 s) was found at 140 pairs with estimate 0.83 s (se 0.25); detection by 20/40 pairs at 2.7 is 45 %/82 % at segment sd 1.8 s, 17 %/38 % at 2.8 s, 7 %/15 % at 4.7 s. Pairing needs 3-220x fewer runs than unpaired comparison (median ~25x); judging on the segment saves a further 1.0-3.0x pairs over the paired whole run, most when the segment ends at the first stage after the change. Effects reported at an early stop run slightly high (a 1 s effect reads about 1.1-1.3 s).

## How it works

- **In the game (default).** A call takes a snapshot of your code windows and the start state `simulate()` would use (unlocks, items, globals, your farm's hats) and runs the seeds one after another on a background thread of the game you are playing; the calling drone waits like it does for `simulate()`, and the stop button cancels the remaining runs.
- **Background copies (experimental, `workers` >= 1).** The game starts copies of its own executable (`-batchmode -nographics`, no window, below-normal priority, one simulation at a time each) with switches of this mod (`-fsdata`, `-fssave`, `-fsautoplay`, `-fsnooutput`, `-fsworker`, `-fsparent`), strictly one at a time. Each must write `fsready.txt` with its own process id into its own folder within 20 s or it is killed; at most one retry per call; if a copy cannot be used the call fails with an error that says so (it does not quietly do something else). Copies get the same snapshot and start state, run jobs handed over through files in their own folder, and return time, stages and printed text. They are reused between calls and end with the game: on exit, through a parent-process check in each copy, and through a Windows job object that the OS closes even if the game crashes.
- **Same simulation code.** Runs use the game's own `Simulation` and `Execution` classes with the constructor arguments `simulate()` / `leaderboard_run()` use, stepped as fast as possible with no rendering. Each run parses its own syntax trees from the snapshot.
- **Shared program trees.** `spawn_drone` deep-copies the program for every drone, about half of the CPU time of a drone-heavy reset. During that copy the mod shares the parts that hold no per-call state; function and `def` nodes are still copied, and the two kinds of state the game keeps on nodes are kept per (drone, node) as the game keeps them per node object. Option `shared_trees`.
- **Garbage collection.** While the mod simulates, the automatic collector is paused and the mod collects every `gc_every_mb` MB.
- **Hot spots** (`hot_spots`, on). For the mod's own simulations only: the scheduler step is a C# copy of the game's `Simulation.RunNextStep` + `Execution.Execute` with two LINQ `Min` scans written as loops; the dinosaur hat's free-cell flood fill visits cells in the same order without allocating; an unlock check that passed is not repeated until the farm unlocks something; parsed token streams are reused per text. Same results, by construction and by the gate below.
- **Bytecode VM** (`vm`, on). The mod's simulations run each file and function as bytecode whose every instruction mirrors, in order, what the game's syntax-tree node does (same yields, same tick charges, same errors and messages); deeply immutable tuples are shared instead of deep-copied for drones. A file the compiler does not support runs on the game's interpreter. Turn it off with `sim_options({"vm": False})` and a restart if you ever suspect it.
- Patches act only on the mod's own simulations (or only in the background copies); the game's `simulate()`, `leaderboard_run()` and normal runs go through the game's own code. Details: `REVIEW_NOTES.md`.

## Notes

- **Same results as the game.** On the game build this release was tested on (Steam, Windows; `Core.dll` SHA-256 `da7373f9...`), `simulate_many` returned exactly the times of the game's own `simulate()` for the same seeds, and on 9 runs of two full-game farm programs (drones, mazes, dinosaurs, every unlock) it matched the reference times, every stage time and every printed line, with `hot_spots` and `vm` off, each on alone, and both on. The test suite also covers drones, errors inside runs, warnings, globals and items, leaderboard start states, `until`, `compare` verdicts, 34 kinds of bad arguments, and the safety guards.
- **Speed.** A full-game program (about 1,600 game seconds per run), 3 seeds, an 8-core desktop CPU, quiet machine, seconds of real time per run: the game's own `simulate()` in a loop 18.6 s; `simulate_many` with `hot_spots` and `vm` off 12.4 s; `simulate_many` with the defaults 4.9 s, about 3.8x faster than `simulate()`. Same in-game times returned in every case.
- **Speed on a busy machine** (another game running at the same time): 18.1 s, 12.4 s and 4.6 s for the same three; a simulation uses one CPU thread, so other work on a multi-core machine barely changes it.
- **Timing it yourself.** `get_time()` and `get_tick_count()` around a call show what the call costs your drone (200 ticks per run), not how long you waited; use a clock to see the real time.
- **How long `compare` takes.** A 1 s change in a segment with ~2 s of seed-to-seed noise needs about 40 pairs for a clear verdict, i.e. 80 runs: about 80 x the seconds per run above, inside the game.
- **After a game update** a simulation could differ from the new game until the mod is rebuilt and retested; set `hot_spots` and `vm` to False if you see a difference, and report it.
- `speedup` is ignored; runs are as fast as the machine allows. The game stays responsive during a call and the stop button cancels the rest of the runs.

## Files

This package: `FasterSimulations.dll`, `README.md`, `CHANGELOG.md`, `LICENSE`. The source (C#, BepInEx 5, Harmony), its test suite and the review notes that list every patch and the adapted game code are not published in this repository yet.

## Licence and game code

The mod patches the game at run time (Harmony); it ships no game files and no game assets. To give results identical to the game, parts of it are adapted from the game's own code: the simulation scheduler step (`Simulation.RunNextStep`, `Execution.Execute`) and several interpreter operations (binary operators, comparisons, assignment, the statement-list result list), listed in `REVIEW_NOTES.md`. Those parts remain the property of the game's developer. The MIT licence in `LICENSE` covers only the original parts of this mod. This mod is not affiliated with or endorsed by the developer of The Farmer Was Replaced.

## Command line switches

Used by the mod's own background copies and by its test suite; players never need them.

| switch | effect |
|---|---|
| `-fsdata DIR` | the game's data folder (options.txt, Saves, output.txt) is DIR |
| `-fssave NAME` | open save NAME (options.txt is not rewritten for it) |
| `-fsautoplay` | leave the title screen as soon as the save is loaded |
| `-fsnooutput` | do not write output.txt |
| `-fsworker` | run as a background copy (takes jobs from files in its data folder; never saves) |
| `-fsparent PID` | quit when process PID has ended |
| `-fsrun FILE`, `-fsquit` | tests: start code file FILE once the farm is open; quit when it has finished |
| `-fsnospeed`, `-fsnoshare`, `-fsnohot`, `-fsnovm` | tests: switch off all speedups / `shared_trees` / `hot_spots` / `vm` for this process |
| `-fsgcmb N`, `-fsnostages`, `-fsmaxreal S`, `-fsmaxgame S` | tests: `gc_every_mb`, no stages, `max_real_seconds`, `max_game_seconds` for this process |
| `-fstesthook`, `-fstestlimits CPU,FREE_GB[,POOL_FREE_GB]` | tests only: allow the test stub instead of a background copy (`FASTERSIM_TEST_WORKER_EXE`), and replace the measured CPU threads / free memory for the limit |
