class Algorithm:
    def __init__(self, config):
        # Set up initial elevator state from configuration file
        self.total_floors = config.get('num_floors', 10)
        self.CAPACITY = config.get('capacity', 20)
        self.current_floor = 1
        self.queued_floors = []
        self.direction = "none"
        self.weight = 0
        self.time_elapsed = 0
        self.stop_history = []
        self.pickups = []
        self.dropoffs = []

    def floorCheck(self, floor):
        # Convert both floor numbers to integers for comparison
        return str(floor) in self.queued_floors
        
    def pathing(self):
        # Decide which direction to move
        if not self.queued_floors:
            return "none"  # No more floors to visit
            
        # Split requested floors into those above and below current floor
        floors_above = [int(f) for f in self.queued_floors if int(f) > self.current_floor]
        floors_below = [int(f) for f in self.queued_floors if int(f) < self.current_floor]
        
        if not floors_above and not floors_below:
            return "none"
        elif not floors_above:
            return "down"
        elif not floors_below:
            return "up"
            
        # Calculate shortest path
        up_dist = min(floors_above) - self.current_floor
        down_dist = self.current_floor - max(floors_below)
        return "up" if up_dist <= down_dist else "down"

    def move(self):
        # Handle current floor if it's in queue
        if self.floorCheck(self.current_floor):
            self.queued_floors.remove(str(self.current_floor))
            self.stop_history.append(self.current_floor)
            self.pickups.append(0)
            self.dropoffs.append(0)
            print(f"Stopped at floor: {self.current_floor}")
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
    controller = Algorithm(config)
    
    # Process each request in order of floor number
    for start_floor, destinations in sorted(requests.items(), key=lambda x: int(x[0])):
        start_floor = int(start_floor)
        destinations = sorted(destinations)  # Sort destinations for each floor
        
        for dest in destinations:
            # Go to pickup floor
            if start_floor != controller.current_floor:
                controller.queued_floors.append(str(start_floor))
                while controller.move():
                    pass

            # Take passenger to destination if capacity allows
            if controller.weight < controller.CAPACITY:
                if controller.stop_history and controller.stop_history[-1] == controller.current_floor:
                    controller.pickups[-1] += 1
                    controller.add_passenger()
                
                controller.queued_floors.append(str(dest))
                while controller.move():
                    pass
                
                if controller.stop_history and controller.stop_history[-1] == controller.current_floor:
                    controller.dropoffs[-1] += 1
                    controller.remove_passenger()

    return {
        "final_floor": controller.current_floor,
        "direction": controller.direction,
        "weight": controller.weight,
        "total_time": controller.time_elapsed,
        "stops": controller.stop_history,
        "pickups": controller.pickups,
        "dropoffs": controller.dropoffs
    }