class Elevator:
    def __init__(self, id, total_floors):
        self.id = id
        self.current_floor = 0
        self.total_floors = total_floors
        self.passengers = []
        self.queued_floors = []
        self.backup_queue = []
        self.direction = "stop"
        self.prior_direction = "none"
        self.weight_count = 0
        self.SOFT_CAPACITY = 10
        self.HARD_CAPACITY = 20

    def check_floor(self):
        return self.current_floor in self.queued_floors

    def determine_path(self):
        if not self.queued_floors:
            return "stop"
            
        check_up = any(floor > self.current_floor for floor in self.queued_floors)
        check_down = any(floor < self.current_floor for floor in self.queued_floors)
        
        if not check_up and not check_down:
            return "stop"
        elif not check_up:
            return "down"
        elif not check_down:
            return "up"
            
        up_dist = max((f - self.current_floor for f in self.queued_floors if f > self.current_floor), default=0)
        down_dist = abs(min((f - self.current_floor for f in self.queued_floors if f < self.current_floor), default=0))
        
        return "up" if up_dist < down_dist else "down"

    def move(self):
        if self.check_floor():
            self.queued_floors.remove(self.current_floor)
            
        self.direction = self.determine_path()
        
        if self.direction == "up" and self.current_floor < self.total_floors - 1:
            self.current_floor += 1
            self.prior_direction = "up"
        elif self.direction == "down" and self.current_floor > 0:
            self.current_floor -= 1
            self.prior_direction = "down"

    def add_stop(self, floor):
        if floor not in self.queued_floors:
            self.queued_floors.append(floor)

    def load_passenger(self, passenger):
        if self.weight_count < self.HARD_CAPACITY:
            self.passengers.append(passenger)
            self.add_stop(passenger.destination_floor)
            self.weight_count += 1
            return True
        return False

    def unload_passenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            self.weight_count -= 1

    def move_up(self, args):
        if len(args) != 1:
            print("Usage: up <elevator_id>")
            return
        elevator_id = int(args[0])
        elevator = self._get_elevator(elevator_id)
        if elevator:
            elevator.move()
            print(f"Elevator {elevator_id} at floor {elevator.current_floor}")

    def move_down(self, args):
        if len(args) != 1:
            print("Usage: down <elevator_id>")
            return
        elevator_id = int(args[0])
        elevator = self._get_elevator(elevator_id)
        if elevator:
            elevator.move()
            print(f"Elevator {elevator_id} at floor {elevator.current_floor}")