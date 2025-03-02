import json
from pathlib import Path
import sys

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Local import
from algorithm import Algorithm, run_algorithm

def calculate_theoretical_time(requests):
    """Calculate time based on floor movements and passenger handling"""
    time = 0
    for start_floor, destinations in requests.items():
        for dest in destinations:
            # 3 seconds per floor moved
            time += abs(int(start_floor) - dest) * 3
            # 5 seconds for loading/unloading at each end
            time += 10
    return time

def run_elevator_simulation():
    # Read the config file
    config_path = project_root / 'config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("Loading configuration:")
    print(json.dumps(config, indent=2))
    print("\nStarting simulation...")
    
    # Calculate theoretical time
    theoretical_time = calculate_theoretical_time(config['requests'])
    
    result = run_algorithm(config['requests'], config)
    
    print(f"\nSimulation completed")
    print(f"Theoretical time: {theoretical_time} seconds ({theoretical_time/60:.1f} minutes)")
    print(f"Final state - Floor: {result['final_floor']}, Direction: {result['direction']}")
    print(f"Final weight: {result['weight']}")
    print("\nElevator Journey:")
    print(f"Stops made: {result['stops']}")
    print(f"Passengers boarding: {result['pickups']}")
    print(f"Passengers exiting: {result['dropoffs']}")

if __name__ == '__main__':
    run_elevator_simulation()