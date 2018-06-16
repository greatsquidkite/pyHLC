intervals = ["Local", "Half", "One", "Two", "Three", "Four"]
nodes = ["1", "2", "3", "4", "5"]
max_results = {}
average_results = {}
for interval in intervals:
	averages = []
	maxs = []
	for node in nodes:
		seen_values = []
		max_value = 0
		infile = "stats" + interval + node + ".log"
		with open(infile, "r") as f:
			for line in f:
				if "Seen" in line:
					seen_value = int(line[22:].strip())
					seen_values.append(seen_value)
				elif "Max" in line:
					max_value = int(line[23:].strip())
		maxs.append(max_value)
		average = sum(seen_values)/len(seen_values)
		averages.append(average)
	max_results[interval] = maxs
	average_results[interval] = averages
print(max_results)
for key in max_results:
	print(key)
	print(sum(max_results[key])/len(max_results[key]))
print(average_results)
for key in average_results:
	print(key)
	print(sum(average_results[key])/len(average_results[key]))


