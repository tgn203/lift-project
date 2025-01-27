class Elevator:
    def __init__(self, id, total_floors):
        self.id = id
        self.current_floor = 0
        self.total_floors = total_floors
        self.passengers = []

    def move_up(self):
        if self.current_floor < self.total_floors - 1:
            self.current_floor += 1

    def move_down(self):
        if self.current_floor > 0:
            self.current_floor -= 1

    def load_passenger(self, passenger):
        self.passengers.append(passenger)

    def unload_passenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)