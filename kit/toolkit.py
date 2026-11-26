# toolkit.py: measuring tools for The Farmer Was Replaced.
# Where does my time go? timed(). Did that change help, or was I lucky? bench().

# Counted actions: use these instead of move / till / plant / harvest, so timed() can split
# action ticks (200 each) from thinking ticks.
# The counting costs ticks too: each counted action adds COUNT_TICKS over the bare builtin, and timed() adds TIMED_TICKS (calling f).
COUNT_TICKS = 1
TIMED_TICKS = 1
actions = 0
def Move(d):
	global actions
	actions += 1
	move(d)
def Till():
	global actions
	actions += 1
	till()
def Plant(crop):
	global actions
	actions += 1
	plant(crop)
def Harvest():
	global actions
	actions += 1
	harvest()

# Where does the time go: seconds, counted actions, thinking ticks, and stock of the watched items.
# Returns the number of counted actions.
def timed(name, f, watch):
	global actions
	actions = 0
	t = get_time()
	k = get_tick_count()
	f()
	ticks = get_tick_count() - k
	quick_print(name, get_time() - t, "s |", actions, "actions |", ticks - actions * (200 + COUNT_TICKS) - TIMED_TICKS, "thinking ticks")
	for item in watch:
		quick_print("   ", item, num_items(item))
	return actions

# Did that help, or was I lucky: an A/B bench. Run it as your main program (simulate() inside a
# simulation returns None). file_a and file_b are whole runs that differ by one change. items: what
# each run starts with (for example {Items.Carrot: 100000}: pumpkins and sunflowers cost carrots to plant).
def bench(file_a, file_b, seeds, items):
	wins = 0
	total = 0
	worst = None
	for s in seeds:
		a = simulate(file_a, Unlocks, items, {}, s, 64)
		b = simulate(file_b, Unlocks, items, {}, s, 64)
		d = b - a
		total += d
		if d < 0:
			wins += 1
		if worst == None or d > worst:
			worst = d
	quick_print("B - A: mean", total / len(seeds), "s | worst", worst, "s | B wins", wins, "of", len(seeds))
