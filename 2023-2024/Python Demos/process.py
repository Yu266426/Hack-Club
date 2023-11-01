import json


def json_key(element):
    return element[1]


file = open("leaderboard.json")

data = json.load(file)

sorted_data = sorted(data.items(), key=json_key, reverse=True)

for element in sorted_data[:3]:
    print(element[0], ":", element[1])

file.close()
