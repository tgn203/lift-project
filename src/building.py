class Building:
    def __init__(self, num_floors=10):
        self.num_floors = num_floors
        self.elevators = []
    
    def add_elevator(self, elevator):
        self.elevators.append(elevator)
    
    def request_elevator(self, floor):
        # Logic to request an elevator from a specific floor
        pass
    
    def get_elevator_status(self):
        # Logic to get the status of all elevators
        pass