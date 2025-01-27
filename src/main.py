import json
from building import Building

def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

def main():
    config = load_config()
    num_floors = config.get('num_floors', 10)
    num_elevators = config.get('num_elevators', 1)

    building = Building(num_floors, num_elevators)
    building.start_simulation()

if __name__ == "__main__":
    main()