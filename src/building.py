class Building:
    def __init__(self, num_floors=10):
        self.num_floors = num_floors
        self.elevators = []
    
    def add_elevator(self, elevator):
        if elevator.total_floors == self.num_floors:
            self.elevators.append(elevator)
            return True
        return False