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
currentfloor: int = int(floorcount / 2)
capacity: int = 5


direction: int = 0
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

lift: list[int] = []


while sum([len(floor) for floor in floorrequests.values()]) != 0 or len(lift) != 0:
    stopping: bool = False
    if currentfloor in lift:
        stopping = True
        while currentfloor in lift:
            lift.remove(currentfloor)
    if len(floorrequests[currentfloor]) > 0 and len(lift) < capacity:
        stopping = True
    while len(floorrequests[currentfloor]) > 0 and len(lift) < capacity:
        lift.append(floorrequests[currentfloor][0])
        floorrequests[currentfloor].pop(0)
    if currentfloor == 1 or currentfloor == floorcount:
        direction *= -1

    if all(call < currentfloor for call in lift):
        direction = -1
    if all(call > currentfloor for call in lift):
        direction = 1

    if stopping:
        print(f"Stopping at {currentfloor}")
        print(f"Floor requests contain {floorrequests}")
        print(f"Lift contains {lift}")
    currentfloor += direction