class Algorithm:
    def __init__(self, total_floors=10):
        self.current_floor = 0
        self.total_floors = total_floors
        self.queued_floors = []
        self.direction = "none"
        self.weight = 0
        self.time_elapsed = 0  # Add time tracking

    def floorCheck(self, floor):
        return floor in self.queued_floors
        
    def pathing(self):
        if not self.queued_floors:
            return "none"
            
        floors_above = [f for f in self.queued_floors if f > self.current_floor]
        floors_below = [f for f in self.queued_floors if f < self.current_floor]
        
        if not floors_above and not floors_below:
            return "none"
        elif not floors_above:
            return "down"
        elif not floors_below:
            return "up"
            
        up_dist = min(floors_above) - self.current_floor
        down_dist = self.current_floor - max(floors_below)
        return "up" if up_dist <= down_dist else "down"

    def move(self):
        if self.floorCheck(self.current_floor):
            self.queued_floors.remove(self.current_floor)
            print(f"Stopped at floor: {self.current_floor}")
            print(f"New queued floors: {self.queued_floors}")
            self.time_elapsed += 5  # Add 5 seconds for stop
            
        self.direction = self.pathing()
        
        if self.direction == "up" and self.current_floor < self.total_floors - 1:
            self.current_floor += 1
            self.time_elapsed += 3  # Add 3 seconds for movement
            print(f"Current Floor = {self.current_floor}")
            return True
        elif self.direction == "down" and self.current_floor > 0:
            self.current_floor -= 1
            self.time_elapsed += 3  # Add 3 seconds for movement
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

def run_algorithm(requests, total_floors=10):
    controller = Algorithm(total_floors)
    
    # Process pickup and dropoff requests
    for start_floor, destinations in requests.items():
        start_floor = int(start_floor)
        for dest in destinations:
            # Add pickup floor to queue
            controller.queued_floors.append(start_floor)
            
            # Move until we reach pickup
            while controller.move():
                pass
                
            # Pickup passenger
            controller.add_passenger()
            
            # Add destination to queue
            controller.queued_floors.append(dest)
            
            # Move until we reach destination
            while controller.move():
                pass
                
            # Drop off passenger
            controller.remove_passenger()
    
    return {
        "final_floor": controller.current_floor,
        "direction": controller.direction,
        "weight": controller.weight,
        "total_time": controller.time_elapsed  # Add actual time to result
    }