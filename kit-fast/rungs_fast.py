# rungs_fast.py: the same harness as rungs.py, all seeds in one call. Needs the Faster Simulations mod; run it as your main program.
# Put the names of your farm files below. Each file must set up its own field:
#   rung 2: a pumpkin farm that starts with set_world_size(6)
#   rung 3: a sunflower farm that starts with set_world_size(8) and uses 8 drones
# Settings (the same ones the numbers to beat were measured with): every unlock, 100,000 carrots.
# It reports the mean game time over the seeds and the number to beat.

MY_PUMPKINS = "my_pumpkins"
MY_SUNFLOWERS = "my_sunflowers"
items = {Items.Carrot: 100000}

def mean_time(name, seeds):
	times = simulate_many(name, Unlocks, items, {}, seeds, 64)
	total = 0
	for i in range(len(seeds)):
		t = times[i]
		if t == None:
			quick_print(name, "could not run (seed", seeds[i], "): does the file exist, and does the game accept its code?")
			return None
		total += t
	return total / len(seeds)

t = mean_time(MY_PUMPKINS, [1, 2, 3, 4, 5])
if t != None:
	quick_print("rung 2:", MY_PUMPKINS, "6x6 pumpkins, mean game time over seeds 1-5:", t, "s | to beat: 15.0 s")

t = mean_time(MY_SUNFLOWERS, [1])
if t != None:
	quick_print("rung 3:", MY_SUNFLOWERS, "8x8 sunflowers, 8 drones, seed 1:", t, "s | to beat: 14.92 s at 406.8 power")
	quick_print("        (print num_items(Items.Power) at the end of your farm to compare the power)")
