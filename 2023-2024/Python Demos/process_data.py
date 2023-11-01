import json
import pathlib

LEADERBOARD_PATH = pathlib.Path.cwd() / "leaderboard.json"

with open(LEADERBOARD_PATH) as file:
    data: dict = json.load(file)

sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)

for item in sorted_data:
    print(f"{item[0]}: {item[1]}")
