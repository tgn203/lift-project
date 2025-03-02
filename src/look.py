floorrequests: dict = {
    1: [4, 6],
    2: [3, 5, 7],
    3: [8],
    4: [2, 5],
    5: [6, 1],
    6: [7],
    7: [4, 2],
    8: [3],
}
floorcount: int = 8
currentfloor: int = 1  # int(floorcount / 2)
capacity: int = 5


direction: int = 0
"""
countdown: int = 0
countup: int = 0
if len(floorrequests[currentfloor]):
    for call in floorrequests[currentfloor]:
        if call < currentfloor:
            countdown += 1
        else:
            countup += 1
else:
    for floornum, calls in enumerate(floorrequests.items()):
        if floornum < currentfloor:
            countdown += len(calls)
        else:
            countup += len(calls)

if countup < countdown:
    direction = -1
else:
    direction = 1
"""

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
    if len(floorrequests[currentfloor]) > 0 and len(lift) < capacity:
        stopping = True
        amountentering.append(0)
    # while there is people wanting to get on the lift and there is space, add the next person onto the lift
    while len(floorrequests[currentfloor]) > 0 and len(lift) < capacity:
        lift.append(floorrequests[currentfloor][0])
        floorrequests[currentfloor].pop(0)
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
