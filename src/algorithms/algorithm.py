class Algorithm:
    def __init__(self, config):
        # Set up initial elevator state from configuration file
        self.total_floors = config.get('floors', 10)  # Total number of floors in building
        self.CAPACITY = config.get('capacity', 20)    # Maximum number of passengers
        self.current_floor = 1                        # Start at floor 1
        self.queued_floors = []                       # List of floors to visit
        self.direction = "none"                       # Current direction (up/down/none)
        self.weight = 0                               # Current passenger weight
        self.time_elapsed = 0                         # Total time taken

    def floorCheck(self, floor):
        # Check if we need to stop at this floor
        return floor in self.queued_floors
        
    def pathing(self):
        # Decide which direction to move
        if not self.queued_floors:
            return "none"  # No more floors to visit
            
        # Split requested floors into those above and below current floor
        floors_above = [f for f in self.queued_floors if f > self.current_floor]
        floors_below = [f for f in self.queued_floors if f < self.current_floor]
        
        # Determine direction based on pending requests
        if not floors_above and not floors_below:
            return "none"
        elif not floors_above:
            return "down"  # Only floors below
        elif not floors_below:
            return "up"    # Only floors above
            
        # Calculate shortest path
        up_dist = min(floors_above) - self.current_floor    # Distance to closest up floor
        down_dist = self.current_floor - max(floors_below)  # Distance to closest down floor
        return "up" if up_dist <= down_dist else "down"     # Choose shortest distance

    def move(self):
        # Handle current floor if it's in queue
        if self.floorCheck(self.current_floor):
            self.queued_floors.remove(self.current_floor)
            print(f"Stopped at floor: {self.current_floor}")
            print(f"New queued floors: {sorted(self.queued_floors)}")
            self.time_elapsed += 5  # 5 seconds for stop
            
        # Determine next movement
        self.direction = self.pathing()
        
        # Move up or down if possible
        if self.direction == "up" and self.current_floor < self.total_floors:
            self.current_floor += 1
            self.time_elapsed += 3  # 3 seconds per floor movement
            print(f"Current Floor = {self.current_floor}")
            return True
        elif self.direction == "down" and self.current_floor > 1:
            self.current_floor -= 1
            self.time_elapsed += 3  # 3 seconds per floor movement
            print(f"Current Floor = {self.current_floor}")
            return True
        return False

    def add_passenger(self, weight=1):
        self.weight += weight
        self.time_elapsed += 5  # Add 5 seconds for loading
        print(f"weight (increased) = {self.weight}")

    def remove_passenger(self, weight=1):
        self.weight -= weight
        self.time_elapsed += 5  # Add 5 seconds for unloading
        print(f"weight (reduced) = {self.weight}")

def run_algorithm(requests, config):
    # Initialize elevator
    controller = Algorithm(config)
    
    # Sort floors in numerical order
    floor_numbers = [int(floor) for floor in requests.keys()]
    floor_numbers.sort()
    
    # Process requests floor by floor
    for floor in floor_numbers:
        start_floor = str(floor)  # Convert back to string to match requests dict
        destinations = requests[start_floor]
        destinations.sort()  # Sort destinations for efficiency
        
        for dest in destinations:
            # Move to pickup floor if needed
            if start_floor != controller.current_floor:
                controller.queued_floors.append(start_floor)
                while controller.move():  # Keep moving until we reach pickup floor
                    pass
                    
            # Handle passenger if capacity allows
            if controller.weight < controller.CAPACITY:
                controller.add_passenger()                    # Load passenger
                controller.queued_floors.append(dest)         # Add destination
                while controller.move():                      # Move to destination
                    pass
                controller.remove_passenger()                 # Unload passenger
            else:
                print(f"Warning: Skip passenger - At capacity ({controller.CAPACITY})")
    
    # Return final elevator state
    return {
        "final_floor": controller.current_floor,
        "direction": controller.direction,
        "weight": controller.weight,
        "total_time": controller.time_elapsed
    }