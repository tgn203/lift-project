# FOR TESTING
"""
import inputread

config = inputread.load_config_from_file("input.txt")
"""


def algorithm(config):
    floorrequests = config["requests"]
    floorcount: int = config["num_floors"]
    capacity: int = config["capacity"]
    currentfloor: int = 1

    direction: int = -1

    laststop: int = currentfloor
    lift: list[int] = []
    stops: list[int] = [1]
    movements: list[tuple[int, int]] = []
    amountleaving: list[int] = []
    amountentering: list[int] = []


    # loops while there is still people to move about
    while sum([len(floor) for floor in floorrequests.values()]) != 0 or len(lift) != 0:
        stopping: bool = False
        # only executes if people are leavin the current floor
        if currentfloor in lift:
            # stops and removes the people leaving from the lift
            stopping = True
            amountleaving.append(0)
            while currentfloor in lift:
                lift.remove(currentfloor)
                amountleaving[-1] += 1
        # stops of there are people wanting to get on the lift, and the lift currently has space
        if len(floorrequests[str(currentfloor)]) > 0 and len(lift) < capacity:
            stopping = True
            amountentering.append(0)
        # while there is people wanting to get on the lift and there is space, add the next person onto the lift
        while len(floorrequests[str(currentfloor)]) > 0 and len(lift) < capacity:
            lift.append(floorrequests[str(currentfloor)][0])
            floorrequests[str(currentfloor)].pop(0)
            amountentering[-1] += 1
        # if the lift has reached the bottom or the top reverse the direction
        if currentfloor == 1 or currentfloor == floorcount:
            direction *= -1

        # if there are only calls down then send the lift down
        if all(call < currentfloor for call in lift) and len(lift) > 0:
            direction = -1
        # if there are only calls up then send the lift up
        if all(call > currentfloor for call in lift) and len(lift) > 0:
            direction = 1

        # stores and prints any info about the stop and adds items to lists for gui implementation
        if stopping:
            stops.append(currentfloor)
            movements.append((laststop, currentfloor))
            laststop = currentfloor
            print(f"Stopping at {currentfloor}")
            print(f"Floor requests contain {floorrequests}")
            print(f"Lift contains {lift}")
        currentfloor += direction

    # Return to GUI
    return {
        "stops": stops,
        "on": amountentering,
        "off": amountleaving,
        "movements": len(movements)
    }
