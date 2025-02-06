import sys

class TerminalUI:
    def run(self):
        print("\nElevator Simulator Terminal UI")
        print("Type 'help' for commands")
        
        while True:
            try:
                command = input("\nEnter command: ").strip().split()
                if not command:
                    continue
                
                cmd_name = command[0].lower()
                if cmd_name in self.commands:
                    if cmd_name in ['help', 'status', 'quit']:
                        self.commands[cmd_name]()
                    else:
                        self.commands[cmd_name](command[1:])
                else:
                    print("Unknown command. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

    def __init__(self, building):
        self.building = building
        self.commands = {
            'help': self.show_help,
            'status': self.show_status,
            'up': self.move_up,
            'down': self.move_down,
            'load': self.load_passenger,
            'unload': self.unload_passenger,
            'quit': self.quit
        }

    def show_help(self):
        print("\nAvailable commands:")
        print("status - Show elevator status")
        print("up <elevator_id> - Move elevator up")
        print("down <elevator_id> - Move elevator down")
        print("load <elevator_id> <current_floor> <destination_floor> - Load passenger")
        print("unload <elevator_id> <passenger_index> - Unload passenger")
        print("quit - Exit program")

    def show_status(self):
        for elevator in self.building.elevators:
            print(f"\nElevator {elevator.id}:")
            print(f"Current floor: {elevator.current_floor}")
            print(f"Passengers: {len(elevator.passengers)}")
            for i, p in enumerate(elevator.passengers):
                print(f"  {i}: Floor {p.current_floor} → {p.destination_floor}")

    def move_up(self, args):
        if len(args) != 1:
            print("Usage: up <elevator_id>")
            return
        elevator_id = int(args[0])
        elevator = self._get_elevator(elevator_id)
        if elevator:
            elevator.move_up()
            print(f"Elevator {elevator_id} moved up to floor {elevator.current_floor}")

    def move_down(self, args):
        if len(args) != 1:
            print("Usage: down <elevator_id>")
            return
        elevator_id = int(args[0])
        elevator = self._get_elevator(elevator_id)
        if elevator:
            elevator.move_down()
            print(f"Elevator {elevator_id} moved down to floor {elevator.current_floor}")

    def load_passenger(self, args):
        if len(args) != 3:
            print("Usage: load <elevator_id> <current_floor> <destination_floor>")
            return
        elevator_id, current_floor, dest_floor = map(int, args)
        elevator = self._get_elevator(elevator_id)
        if elevator:
            from passenger import Passenger
            passenger = Passenger(current_floor, dest_floor)
            elevator.load_passenger(passenger)
            print(f"Loaded passenger: Floor {current_floor} → {dest_floor}")

    def unload_passenger(self, args):
        if len(args) != 2:
            print("Usage: unload <elevator_id> <passenger_index>")
            return
        elevator_id, passenger_idx = map(int, args)
        elevator = self._get_elevator(elevator_id)
        if elevator and 0 <= passenger_idx < len(elevator.passengers):
            passenger = elevator.passengers[passenger_idx]
            elevator.unload_passenger(passenger)
            print(f"Unloaded passenger {passenger_idx}")

    def _get_elevator(self, elevator_id):
        for elevator in self.building.elevators:
            if elevator.id == elevator_id:
                return elevator
        print(f"Elevator {elevator_id} not found")
        return None

    def quit(self):
        print("Goodbye!")
        sys.exit(0)

    def run(self):
        print("Elevator Simulator Terminal UI")
        print("Type 'help' for commands")
        
        while True:
            try:
                command = input("\nEnter command: ").strip().split()
                if not command:
                    continue
                
                cmd_name = command[0].lower()
                if cmd_name in self.commands:
                    if cmd_name == 'help' or cmd_name == 'status' or cmd_name == 'quit':
                        self.commands[cmd_name]()
                    else:
                        self.commands[cmd_name](command[1:])
                else:
                    print("Unknown command. Type 'help' for available commands.")
            except Exception as e:
                print(f"Error: {e}")

#Example commands:
#Enter command: help
#Enter command: status
#Enter command: load 0 1 5
#Enter command: up 0
#Enter command: unload 0 0
#Enter command: quit