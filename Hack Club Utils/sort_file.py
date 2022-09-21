with open("Hack Club Members.txt") as file:
	names = []
	for line in file.readlines():
		name_list = line.split(" ")

		if last.endswith("\n"):
			last = last[:-1]

		names.append((first, last))

sorted_names = sorted(names, key=lambda e: e[0])

with open("Hack Club Members.txt", "w") as file:
	for name in sorted_names:
		file.write(f"{name[0]} {name[1]}\n")
