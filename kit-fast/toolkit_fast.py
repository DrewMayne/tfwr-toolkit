# toolkit_fast.py: the kit's bench, all seeds in one call. Needs the Faster Simulations mod; run it as your main program.
# Did that help, or was I lucky? bench_fast() prints the same line as bench(); verdict() answers in one sentence.

# Did that help, or was I lucky: the same A/B bench as bench() in toolkit.py, with simulate_many instead of
# simulate() in a loop. file_a and file_b are whole runs that differ by one change; items: what each run starts with.
# A seed where either run failed (time None) is left out of the numbers and listed.
def bench_fast(file_a, file_b, seeds, items):
	ss = []
	for s in seeds:
		ss.append(s)
	ra = simulate_many(file_a, Unlocks, items, {}, ss, 64)
	rb = simulate_many(file_b, Unlocks, items, {}, ss, 64)
	wins = 0
	total = 0
	worst = None
	n = 0
	failed = []
	for i in range(len(ss)):
		a = ra[i]
		b = rb[i]
		if a == None or b == None:
			failed.append(ss[i])
		else:
			d = b - a
			total += d
			n += 1
			if d < 0:
				wins += 1
			if worst == None or d > worst:
				worst = d
	if n == 0:
		quick_print("B - A: no seed finished in both files; failed seeds:", failed)
		return None
	quick_print("B - A: mean", total / n, "s | worst", worst, "s | B wins", wins, "of", n)
	if len(failed) > 0:
		quick_print("   left out (a run failed or did not finish):", failed)
	return total / n

# Is B really faster than A: compare() on up to 40 seed pairs, stopping as soon as the answer is clear.
# Prints one plain sentence and returns compare's dict.
def verdict(file_a, file_b, items):
	c = compare(file_a, file_b, Unlocks, items, {}, 40, 64)
	v = c["verdict"]
	d = c["diff"]
	if v == "b":
		quick_print(file_b, "is faster than", file_a, "by", -d, "s (+-", c["se"], "s, over", c["pairs"], "seed pairs)")
	elif v == "a":
		quick_print(file_a, "is faster than", file_b, "by", d, "s (+-", c["se"], "s, over", c["pairs"], "seed pairs)")
	elif v == "none":
		quick_print("no difference found between", file_a, "and", file_b, "over", c["pairs"], "seed pairs: B - A =", d, "s (+-", c["se"], "s)")
	elif v == "start_differs":
		quick_print(file_a, "and", file_b, "already differ before the change; compare from an earlier stage")
	else:
		quick_print("not sure yet after", c["pairs"], "seed pairs: B - A =", d, "s (+-", c["se"], "s); try more seeds with compare()")
	return c
