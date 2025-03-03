import random
import json
import algs.inputread as inputread


def generate_floor_requests(floors, capacity):
    requests = {}
    for floor in range(1, floors + 1):
        # Random chance (60%) for floor to have requests
        if random.random() < 0.6:
            possible_destinations = [f for f in range(1, floors + 1) if f != floor]
            num_requests = random.randint(1, min(3, len(possible_destinations)))
            destinations = sorted(random.sample(possible_destinations, num_requests))
            requests[floor] = destinations
        else:
            requests[floor] = []
    return requests


def generate_script(floors, capacity):
    requests = generate_floor_requests(floors, capacity)
    script = f"# Number of Floors, Capacity\n{floors}, {capacity}\n# Floor Requests\n"

    for floor in range(1, floors + 1):
        destinations = requests.get(floor, [])
        script += f"{floor}: {', '.join(map(str, destinations))}\n"

    return script


# Main execution
resultjson = []
resulttxt = []
for i in range(1000):
    floors = random.randint(5, 20)
    capacity = random.randint(5, 10)
    result = generate_script(floors, capacity)
    resulttxt.append(result)
    resultjson.append(inputread.convert_config_txt_to_dict(result))

with open("testdata.txt", "w") as file:
    file.write("\n*\n\n".join(resulttxt))

resultjson = {"tests": resultjson}

with open("testdata.json", "w") as file:
    file.write(json.dumps(resultjson))
