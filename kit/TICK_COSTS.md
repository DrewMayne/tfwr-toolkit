# What the game charges: tick costs

Everything your program does is paid for in ticks, and the game clock is ticks. An action costs 200. Almost
everything else costs 1 or 0. This page is the price list, as measured in the game.

**Measured 2026-11-22** on the Steam version (the build after the 5 November 2026 patch), by running each line
in the game and reading `get_tick_count()` before and after. A game update can change any of these. If a number
matters to you, measure it yourself (see the end of this page).

## The short version

| what | ticks |
|---|---|
| An action that succeeds: `move`, `till`, `plant`, `harvest`, `swap`, `use_item`, `spawn_drone`, `clear` ... | **200** |
| An action that fails (returns `False`): a move into a wall, `swap` on something that is not a cactus, `use_item` with too few items | **1** |
| `harvest()` on an empty cell | **1** |
| A look: `can_harvest()`, `get_entity_type()`, `get_ground_type()`, `measure()`, `get_pos_x()`, `num_items()`, `get_water()` ... | **1** |
| `get_time()`, `get_tick_count()`, `quick_print()` called by name | **0** |

## Statements and operators

| what | ticks |
|---|---|
| Assignment `a = b` | 0 |
| Reading a variable or a constant | 0 |
| An operator: `a + c`, `a * c`, `a % c`, `a // c` ... | 1 |
| A comparison: `a < c`, `a == c` (a chain `a < b < c` pays for each) | 1 |
| `and`, `or` | 1 each, even when the right side is skipped |
| `not`, unary minus | 0 |
| `if` | 1 |
| `else` | 0 |
| `while` | 1 to start, plus its condition on every test |
| `for` | 1 in total, however many times it loops |
| `pass` | 1 |
| `return`, `continue` | 0 |
| `def` (when the line runs, as the file loads) | 1 |

## Lists, tuples, sets, dicts

| what | ticks |
|---|---|
| A tuple literal `(a, b)` | 1 |
| A list or set literal | 1 per item (a set charges more for a tuple item) |
| A dict literal | 1, plus 1 per item |
| Index read `l[i]` | 1 |
| Index write `l[i] = x` | 1 |
| `l[i] += 1` | 2 |
| Unpack a tuple `a, b = t` | 0 |
| Unpack a list `a, b = l` | 1 |
| `len()`, `range()` | 1 |
| `min()`, `max()` | 1 per argument |
| A slice | 1 per item in the result |
| A dict or set lookup | 1 per item of the key (a number or a name is 1; a tuple `(x, y)` is more) |
| `x in some_list` | the comparisons it makes: cheap at the front, expensive at the back |
| `l += [x]` | the length of the right side (1 here) |
| `l.remove(x)` | the length of the list |

## Calls

| what | ticks |
|---|---|
| Calling a function by the name it was defined with: `f()` | 0, plus what its body costs |
| Calling a function held in a variable, a list or a tuple: `g = f` then `g()` | 1 |
| `get_time`, `get_tick_count`, `quick_print` through a variable | 1 (by name they are 0) |

## Imports

| what | ticks |
|---|---|
| `import m` the first time | what the top-level lines of `m` cost |
| `import m` again | 0 |
| A module imported once: `m.name`, `m.name = x`, `m.f()` | 0 |
| `from m import f`, then `f()` | 0 |
| The same module imported **twice into one file** | that name gets slower: reads 1, writes 1, calls 1 more |
| A module held in a variable: reading through it | 1 |
| A module held in a variable: calling through it | 2 |
| `from m import *` anywhere in a file | `get_time`, `get_tick_count` and `quick_print` cost 1 per call in that file |

## What this adds up to

- **A wasted move costs as much as 200 lines of thinking.** Look before you act.
- **Thinking is not free either.** A loop over 100 cells that does three things per cell is 300 ticks: a move and a half.
- **The same idea can cost different amounts.** `x in my_list` on a long list, a tuple key in a dict, a call through a
  variable: each is cheap once and adds up inside a loop.
- **Your tools cost ticks too.** `timed()` in `toolkit.py` takes its own counting out of the "thinking ticks" it reports.

## Measure it yourself

```python
t = get_tick_count()
# the line you want to price
quick_print(get_tick_count() - t)
```

`get_tick_count()` and `quick_print()` are free when called by name, so the number printed is the cost of your
line alone. Do it twice: the first run of a line can include one-time costs, such as an import.
