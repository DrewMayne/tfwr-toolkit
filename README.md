# The Farmer Was Replaced: tools for practising, from "From Beginner to Board"

Tools that help you get better at the game by measuring and testing your own farms. They don't solve
the game for you: the farms are yours to write.

Written for Windows and the Steam version of the game. Not affiliated with the game's developer.

## Start here

| your question | the tool | needs |
|---|---|---|
| **Where does my time go?** Actions or thinking? | `timed()` in [kit/toolkit.py](kit/README.md) | nothing: plain game code |
| **Did that help, or was I lucky?** | `bench()` in [kit/toolkit.py](kit/README.md): the same seeds, two versions | nothing: plain game code |
| **How does my farm compare?** | [kit/rungs.py](kit/README.md): your file, fixed settings, a number to beat | nothing: plain game code |
| **How do I run 40 seeds without waiting 12 minutes?** | [Faster Simulations](#faster-simulations): `simulate_many`, `compare`, `leaderboard_simulate` | BepInEx + the mod |

Tonight, in 10 minutes: copy [kit/](kit/README.md) into a save, wrap one phase of your farm in `timed()`,
and run your farm through `rungs.py`. Then change one thing and `bench` it.

Coming to this repository: the worksheet from the talk (its questions, with space for your own farms and
your own working).

## Tool list

| tool | the question it answers | where |
|---|---|---|
| **toolkit.py** | where does my time go (`timed`: seconds, counted actions, thinking ticks); did that help (`bench`: same seeds, two versions). Includes the counted `Move` / `Till` / `Plant` / `Harvest` that `timed` needs | [kit/toolkit.py](kit/toolkit.py), docs in [kit/README.md](kit/README.md) |
| **rungs.py** | how does my farm compare: give it your file name; it reports the mean game time over seeds 1-5 (pumpkins, 6x6) or seed 1 (sunflowers, 8x8, 8 drones), every unlock, 100,000 carrots, and the number to beat: **14.73 s** / **14.92 s at 406.8 power** | [kit/rungs.py](kit/rungs.py) |
| **Faster Simulations** (mod) | how do I test many seeds quickly: `simulate_many` (many seeds in one call), `compare` (a same-seed A / B verdict: which file is faster, and how sure), `leaderboard_simulate` (a leaderboard's start state, nothing submitted). About **3.8x** faster than `simulate()` in a loop (4.9 s against 18.6 s per full-game run, quiet machine); times identical to the game's `simulate()`; refuses to run inside a leaderboard run | [faster-simulations/](faster-simulations/README.md) |
| *Not ours:* **The Farmer Was Replaced** | the game (Steam) | your Steam library |
| *Not ours:* **BepInEx 5.4.23.4, Windows x64** | the mod loader the mod runs in. The game is a 64-bit Unity **Mono** game, so it needs **BepInEx 5, x64**: the file `BepInEx_win_x64_5.4.23.4.zip`. Not x86, not BepInEx 6, not an IL2CPP build | https://github.com/BepInEx/BepInEx/releases/tag/v5.4.23.4 |
| *Not ours:* **HarmonyX** | the patching library inside BepInEx 5 (`0Harmony.dll`); comes with BepInEx | https://github.com/BepInEx/HarmonyX |

## Other ways to play

- **The game as designed:** learn to program by farming, one unlock at a time. Everything else here is optional.
- **Building tools around it:** measuring, simulating, test harnesses. `timed`, `bench` and `rungs.py` are small examples; the habit is to measure before and after every change.
- **Modding:** the game is built with Unity in C#. BepInEx loads mods, and Harmony lets a mod change the game's methods.
  - Some mods change how you **work**: faster testing, for example. Others change the **rules** of the game.
  - Leaderboard runs should be played as if no mod were installed. That's why Faster Simulations refuses to run inside one.
- **Generating code instead of writing it:** at some point people write programs that write their farms. There is no tool for that in this kit.
- **An AI as a lab assistant:** it can design experiments, write code and run tests. The habit that makes it safe: a result isn't true until it has been measured against the real game.

## Install BepInEx (the mod needs it)

1. **Back up your saves.**
   ```powershell
   Copy-Item -Recurse "$env:USERPROFILE\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves" "$env:USERPROFILE\Documents\tfwr-saves-backup"
   ```
   *Worked if* `Documents\tfwr-saves-backup` has one folder per save.

2. **Find the game folder:** Steam, Library, right-click **The Farmer Was Replaced**, **Manage**,
   **Browse local files**. It's the folder with `TheFarmerWasReplaced.exe`.

3. **Download `BepInEx_win_x64_5.4.23.4.zip`** from https://github.com/BepInEx/BepInEx/releases/tag/v5.4.23.4
   and extract it **into the game folder**.

   *Worked if* `winhttp.dll`, `doorstop_config.ini`, `.doorstop_version`, `changelog.txt` and a
   `BepInEx` folder sit next to `TheFarmerWasReplaced.exe` (not inside a sub-folder).

4. **Create the folder `BepInEx\plugins`** in the game folder (the zip doesn't contain it):
   ```powershell
   New-Item -ItemType Directory "<game folder>\BepInEx\plugins"
   ```
   BepInEx itself is checked the first time the game starts with a mod in that folder: the game folder
   then has `BepInEx\LogOutput.log`, whose second line starts with
   `[Message:   BepInEx] BepInEx 5.4.23.4 - TheFarmerWasReplaced`.

## Faster Simulations

Full notes, every function and option, and the safety section: [faster-simulations/README.md](faster-simulations/README.md).

1. Install BepInEx ([above](#install-bepinex-the-mod-needs-it)).
2. Unzip [faster-simulations/dist/FasterSimulations-1.0.0-rc5.zip](faster-simulations/dist/FasterSimulations-1.0.0-rc5.zip)
   and copy its `FasterSimulations` folder into `<game folder>\BepInEx\plugins\`.
   Check the zip first: `Get-FileHash .\FasterSimulations-1.0.0-rc5.zip` must print the hash in
   [SHA256SUMS.txt](faster-simulations/dist/SHA256SUMS.txt).
3. Start the game from Steam as usual (no switches needed). *Worked if* `BepInEx\LogOutput.log` has the
   line `Faster Simulations 1.0.0` ... `loaded`, and once `simulate` is unlocked in your save the new
   functions appear (hover a name for its help).
4. **First call.** Put your farm in a file `farm`, and in another file run:
   ```python
   times = simulate_many("farm", Unlocks, {}, {}, 10, 1)   # seeds 1..10, the same times as 10 simulate() calls
   print(times)
   result = compare("farm", "farm_new", Unlocks, {}, {}, 40, 1)   # which one is faster, and how sure
   print(result["verdict"], result["diff"], result["pairs"])
   ```

Note: `get_time()` and `get_tick_count()` around a call show what the call costs your drone (200 ticks
per run, like `simulate()`), **not how long you waited**. Use a clock for real time, or turn on
`sim_options({"report_time": True})`.

Defaults are safe: everything runs inside the game you are playing, nothing else is started, nothing is
written to your saves. The `workers` option (background copies of the game, at most 4) is experimental;
read its safety note before turning it on.

This is a release candidate (rc5). It is published as a ready-built mod; its source is not in this
repository yet.

## Troubleshooting

**The mod's functions don't appear.** Check `BepInEx\LogOutput.log` in the game folder:
- no `LogOutput.log` at all, or it wasn't updated: BepInEx didn't load (files not next to the exe, wrong flavour: see below, or your antivirus removed `winhttp.dll`);
- no line `Loading [Faster Simulations ...]`: the `FasterSimulations` folder isn't in `BepInEx\plugins\` (did you create that folder?);
- the line is there but the functions are missing: `simulate` isn't unlocked in that save yet.

**Wrong BepInEx flavour.** The x86 build, BepInEx 6 or an IL2CPP build won't load the mod: no log, an
error in the log, or no `Loading [...]` line for the mod. Delete what the wrong zip put into the game
folder (`winhttp.dll`, `doorstop_config.ini`, `.doorstop_version`, `changelog.txt`, the `BepInEx` folder),
then install `BepInEx_win_x64_5.4.23.4.zip` again.

## Save safety

- **Back up first**: copy `%USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves`
  somewhere else. To restore, quit the game and copy it back.
- The kit's files are plain game code: they do only what your own code could do.
- Faster Simulations with default options writes nothing to your saves; its experimental `workers`
  option starts background copies of the game (see its README before using it).

## Leaderboards

- Faster Simulations refuses to run inside `leaderboard_run`, and `leaderboard_simulate` submits nothing.
- Play leaderboard runs yourself, in the game, by the game's rules.

## Licences

- **Code** (`kit/`): MIT, [LICENSE](LICENSE).
- **Faster Simulations**: see [faster-simulations/LICENSE](faster-simulations/LICENSE) and the "Licence and
  game code" section of its README: parts of it are adapted from the game's own code and remain the
  property of the game's developer.
- **Talk materials** (the worksheet, when it is added): CC BY 4.0, [LICENSE-talk.md](LICENSE-talk.md).
- Copyright holder: Andrew Mayne.

Third-party software this repository uses but does not include:
- BepInEx: https://github.com/BepInEx/BepInEx (its licence: https://github.com/BepInEx/BepInEx/blob/master/LICENSE)
- HarmonyX: https://github.com/BepInEx/HarmonyX (its licence: https://github.com/BepInEx/HarmonyX/blob/master/LICENSE)
- The Farmer Was Replaced is the property of its developer. This repository contains no game files.
