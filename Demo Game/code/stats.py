import json
import os.path

from file import CURRENT_DIR

with open(os.path.join(CURRENT_DIR, "leaderboard.json")) as file:
	leaderboard_dict: dict[str, float] = json.load(file)

data = []
for item in leaderboard_dict.items():
	data.append(item)

data.sort(key=lambda e: e[1], reverse=True)

for pair in data:
	print(pair[0], ",", pair[1])
