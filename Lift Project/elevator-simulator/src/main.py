import json
from building import Building
from elevator import Elevator
from terminal_ui import TerminalUI

def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

def main():
    config = load_config()
    num_floors = config.get('num_floors', 10)
    num_elevators = config.get('num_elevators', 1)

    building = Building(num_floors)
    
    # Create and add elevators
    for i in range(num_elevators):
        elevator = Elevator(i, num_floors)
        building.add_elevator(elevator)

    # Start terminal UI
    ui = TerminalUI(building)
    ui.run()

if __name__ == "__main__":
    main()