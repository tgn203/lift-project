class Building:
    def __init__(self, num_floors=10):
        self.num_floors = num_floors
        self.elevators = []
    
    def add_elevator(self, elevator):
        self.elevators.append(elevator)