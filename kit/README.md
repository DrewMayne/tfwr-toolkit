# kit: measuring tools for your own farms

Plain game code: no mod, no Python, no notebook needed. These tools don't farm for you; they tell you
where your farm's time goes and whether a change really helped.

| file | the question it answers |
|---|---|
| `toolkit.py` | **Where does my time go?** `timed()`. **Did that help, or was I lucky?** `bench()` |
| `rungs.py` | **How does my farm compare?** A harness: give it your farm's file name, it reports your mean game time on fixed settings and the number to beat |

## Install

In the game, make a code window named `toolkit` and paste `toolkit.py` into it (same for `rungs`).
Or, with the game closed, copy the files into your save folder
(`%USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\<your save>\`) and
start the game. **Back up that save first.** Start a farm with `from toolkit import *`.

## toolkit.py

| function | what it does | example |
|---|---|---|
| `Move(d)`, `Till()`, `Plant(crop)`, `Harvest()` | the game's `move` / `till` / `plant` / `harvest`, each adding 1 to the global `actions`, so `timed()` can split action ticks (200 each) from thinking ticks. Use them in the code you want to measure | `Move(North)` |
| `timed(name, f, watch)` | runs `f()` and prints the seconds, the counted actions, the thinking ticks and the stock of each item in `watch`; returns the number of actions | `acts = timed("planting", plant_all, [Items.Pumpkin])` |
| `bench(file_a, file_b, seeds, items)` | runs two whole-run files with `simulate()` on the same seeds, starting with `items`, and prints the mean and worst difference (B - A) and how often B won. **Run it as your main program**: `simulate()` inside a simulation returns `None` | `bench("farm_a", "farm_b", [1, 2, 3, 4, 5], {Items.Carrot: 100000})` |

Tested in the game (a test copy, 2026-11-26): `timed()` reports the farm's own thinking ticks: it subtracts what the
counting itself costs (`COUNT_TICKS`, 1 tick per counted action, and `TIMED_TICKS`, the 1 tick of calling `f`), so `f`'s own
ticks are what's left: 10 wrapped moves report 2 thinking ticks, the same as 10 bare `move()` calls in a loop,
and an `f` whose body is only `pass` reports 1 (the `pass` itself costs a tick). The
measured farm still runs 1 tick per counted action slower for being counted; that can't be removed.
`bench` needs `items` (with `{}` a pumpkin or sunflower farm cannot plant: planting costs carrots).

Know this: `get_time()`, `get_tick_count()` and `quick_print()` are free only in a file with no
`from X import *`. `toolkit.py` has none, so `timed()` is accurate, but a farm that star-imports the
toolkit pays a few extra thinking ticks.

## rungs.py: your farm against a number

Edit the two names at the top (`MY_PUMPKINS`, `MY_SUNFLOWERS`) to your files and run `rungs` as your
main program. Your save needs `simulate()` (the Simulation unlock); inside the simulation everything is
unlocked and you start with 100,000 carrots.

| rung | your file | the number to beat |
|---|---|---|
| 2 | a pumpkin farm that starts with `set_world_size(6)`; mean over seeds 1-5 | **15.0 s** mean game time |
| 3 | a sunflower farm that starts with `set_world_size(8)` and uses 8 drones; seed 1 | **14.92 s** at power **406.8** (print `num_items(Items.Power)` at the end of your farm) |

Then use `bench` to test each change you make against your previous version.

Testing many seeds is slow with `simulate()` in a loop: [kit-fast](../kit-fast/README.md) asks the same questions
through the [Faster Simulations](../faster-simulations/README.md) mod, all seeds in one call.
