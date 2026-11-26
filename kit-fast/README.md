# kit-fast: the kit's questions, all seeds in one call

The same questions as the plain [kit](../kit/README.md), with the same output lines, answered with the
[Faster Simulations](../faster-simulations/README.md) mod: every seed runs in one call (`simulate_many`, `compare`)
instead of `simulate()` in a loop, about 4x faster in real time. Needs the mod installed; without it, use the plain kit.

| file | the question it answers |
|---|---|
| `toolkit_fast.py` | **Did that help, or was I lucky?** `bench_fast()`, the same line as `bench()`; or `verdict()`: one plain sentence, stopping as soon as the answer is clear |
| `rungs_fast.py` | **How does my farm compare?** The same harness and numbers to beat as `rungs.py` |

## Install

In the game, make a code window named `toolkit_fast` and paste `toolkit_fast.py` into it (same for `rungs_fast`).
Or, with the game closed, copy the files into your save folder
(`%USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\<your save>\`) and
start the game. **Back up that save first.** Run them from your main program: the mod's functions, like
`simulate()`, do not work inside a simulation.

## First call

```python
from toolkit_fast import *
bench_fast("farm_a", "farm_b", [1, 2, 3, 4, 5], {Items.Carrot: 100000})
# B - A: mean -4.22 s | worst -4.22 s | B wins 5 of 5
verdict("farm_a", "farm_b", {Items.Carrot: 100000})
# farm_b is faster than farm_a by 4.22 s (+- 0 s, over 20 seed pairs)
```

## toolkit_fast.py

| function | what it does | example |
|---|---|---|
| `bench_fast(file_a, file_b, seeds, items)` | runs both whole-run files on the same seeds with `simulate_many`, starting with `items`, and prints the mean and worst difference (B - A) and how often B won: the same line as `bench()`. A seed where a run failed is left out and listed. It does not print what the runs print (`bench()` does) | `bench_fast("farm_a", "farm_b", [1, 2, 3, 4, 5], {Items.Carrot: 100000})` |
| `verdict(file_a, file_b, items)` | `compare()` on up to 40 seed pairs: says which file is faster, by how much, +- what, over how many pairs, or "no difference found"; returns compare's dict. `compare` also prints its own one-line summary | `verdict("farm_a", "farm_b", {Items.Carrot: 100000})` |

## rungs_fast.py

Edit the two names at the top (`MY_PUMPKINS`, `MY_SUNFLOWERS`) to your files and run `rungs_fast` as your
main program. Same settings, same output and the same numbers to beat as `rungs.py` (rung 2: **15.0 s** mean over
seeds 1-5; rung 3: **14.92 s** at power **406.8**, seed 1).

Tested in the game with the mod (2026-11-26): `bench_fast` printed exactly the same lines as `bench` on the same
files and seeds, `rungs_fast` the same lines as `rungs`, and `verdict` on a farm and a copy without a wasted walk
back said the copy is faster by 4.22 s.
