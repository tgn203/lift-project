import time
import sys
import json
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.Algorithm import floorCheck, pathing, followup, takeRequest

def run_elevator_simulation():
    # Read the config file
    config_path = Path(__file__).parent.parent.parent / 'config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("Loading configuration:")
    print(json.dumps(config, indent=2))
    print("\nStarting simulation...")
    
    # Setup initial conditions
    current_floor = 0
    queued_floors = []
    called_up = []
    called_down = []
    
    # Start timing
    start_time = time.time()
    
    # Parse requests from config
    for floor, destinations in config['requests'].items():
        floor = int(floor)
        for dest in destinations:
            if dest > floor:
                called_up.append(floor)
            else:
                called_down.append(floor)
    
    # Run main algorithm loop
    direction = takeRequest(current_floor, called_up, called_down)
    print(f"Initial direction: {direction}")
    
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\nSimulation completed in {execution_time:.4f} seconds")
    print(f"Final state - Floor: {current_floor}, Direction: {direction}")
    print(f"Remaining calls up: {called_up}")
    print(f"Remaining calls down: {called_down}")

if __name__ == '__main__':
    run_elevator_simulation()