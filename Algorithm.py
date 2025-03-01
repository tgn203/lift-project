#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import json


def load_config_from_file(filepath: str) -> dict[str, str]:
    # Check if the file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Config file {filepath} cannot be found.")

    # Check if the file is a `.json` or `.txt` file
    extension = filepath.split(".")[-1]
    if extension not in ["json", "txt"]:
        raise NotImplementedError("Config file must be of type JSON or TXT.")

    # Attempt to open the file
    try:
        with open(filepath, "r", encoding="utf8") as file:
            text = file.read()
            file.close()
    # Generic error handling
    except Exception as e:
        raise Exception(f"An error occurred: \n\t{e}")

    # Convert text config to JSON
    if extension == "txt":
        config = convert_config_txt_to_dict(text)

    # Attempt to convert the text to a dict using JSON decoder
    elif extension == "json":
        try:
            config = json.loads(text)
        # Catch errors on decoding the JSON
        except json.decoder.JSONDecodeError as e:
            raise Exception(f"JSON Decoding error: \n\t{e}")

    return config


def convert_config_txt_to_dict(text: str) -> dict[str, str]:
    # Note: assume the file exists, already checked in calling scope

    # Take text from already opened file, split into lines
    lines = text.split("\n")
    new_lines: list[str] = []
    for line in lines:
        # Remove empty lines
        if not line:
            continue

        # Remove 'comment lines', i.e. starts with `#`
        if line[0] == "#":
            continue

        # Add remaining lines to the new list
        new_lines.append(line)

    # Create empty config dict
    config: dict = {
        "num_floors": 0,
        "capacity": 0,
        "requests": {},
    }

    # First line contains num. floors and capacity
    [num_floors, capacity] = new_lines[0].split(", ")
    config["num_floors"] = int(num_floors)
    config["capacity"] = int(capacity)

    # Remaining lines are floors and their requests
    for line in new_lines[1::]:
        # Seperate line into segments and remove spaces
        split = [_.strip() for _ in line.split(":")]

        # Add empty floors to dict
        if not split[1]:
            config["requests"][int(split[0])] = []
            continue

        else:
            requests = [int(_) for _ in split[1].split(", ")]
            config["requests"][int(split[0])] = requests

    return config


def write_config_to_file(config: dict, filepath: str) -> None:
    # Check if the file is a `.json` or `.txt` file
    extension = filepath.split(".")[-1]
    if extension not in ["json", "txt"]:
        raise NotImplementedError("Config file must be of type JSON or TXT.")

    if extension == "json":
        # Convert the config dict to a JSON object
        config_text = str(json.dumps(config))

    else:
        # Convert to text form
        lines = ["# Number of Floors, Capacity"]

        # Add line for floor number and capacity config
        lines.append(f"{config["num_floors"]}, {config["capacity"]}")
        lines.append("")

        # Add line for each floor config
        lines.append("# Floor Requests")
        for floor, requests in config["requests"].items():
            # Convert floor numbers to strs
            requests = [str(_) for _ in requests]
            lines.append(f"{floor}: {", ".join(requests)}".strip())

        config_text = "\n".join(lines)

    # Attempt to open and write the file
    try:
        with open(filepath, "w", encoding="utf8") as file:
            file.write(config_text)
            file.close()
    # Generic error handling
    except Exception as e:
        raise Exception(f"An error occurred: \n\t{e}")


# In[7]:


def floorCheck(currentFloor, queuedFloors): # a simple check to see if the current floor is inside a list
    if currentFloor in queuedFloors:
        return True 
    else:
        return False
    


# In[8]:


def pathing(currentFloor, queuedFloors): # compares the longest distance the elevator has to travel up, and the longest distance down, and chooses the shorter distance to travel in
    checkUp = False
    checkDown = False
    for i in queuedFloors: # this makes sure the elevator can go up and/or down
        if i > currentFloor:
            checkUp = True
        elif i < currentFloor:
            checkDown = True
    if checkUp == False and checkDown == False:
        return "stop"
    elif checkUp == False:
        return "down"
    elif checkDown == False:
        return "up"
    
    finalUp = 0
    finalDown = 0
    finalUp = abs(max(queuedFloors) - currentFloor)
    finalDown = abs(min(queuedFloors) - currentFloor)
    if finalUp < finalDown: # the shorter distance is chosen 
        return "up" 
    else:
        return "down"
    
    


# In[9]:


def followup(currentFloor, backupQueue, prior): # Once the elevator reaches its destination from the original list this checks if it should keep going
    if prior == "up":
        for i in backupQueue:
            if i > currentFloor:
                return True
        return False
    else:
        for i in backupQueue:
            if i < currentFloor:
                return True
        return False
    


# In[10]:


def takeRequest(currentFloor, calledUp, calledDown): # this would be used if the elevator has no one on it but there are people calling it
    checkUp = True
    checkDown = True
    if len(calledUp) == 0: # checks if there are any calls to go up or down
        checkDown = False
    if len(calledDown) == 0:
        checkUp = False

    
    if checkUp == False and checkDown == False:
        return "stop"
    elif checkUp == False:
        return "down"
    elif checkDown == False:
        return "up"
    
    
    finalUp = currentFloor #will be the lowest possible call up for the elevator
    finalDown = currentFloor #will be the highest possible call down for the elevator
    for i in calledUp:
        if i < finalUp:
            finalUp = i
    longestUpcall = currentFloor - finalUp #the travel down the elevator would have to make
    if longestUpcall < 0:
        longestUpcall = longestUpcall*-1 # makes both values positive if it needs to
    for i in calledDown:
        if i > finalDown:
            finalDown = i
    longestDowncall = finalDown - currentFloor
    if longestDowncall < 0:
        longestDowncall = longestDowncall*-1 # makes this value positive 

    if longestUpcall < longestDowncall: # the shortest distance is then chosen to be used
        return "down"
    else:
        return "up"
    
    


# In[11]:


# the Queue class here works using a basic python list and giving it custom methods that follow the rules of FIFO
class Queue: 

    theQueue = [] 
    # the constructor that makes the Queue
    def __init__(self):
        self.theQueue = []
        
    # returns the length of the list
    def size(self):
        return len(self.theQueue)
        
        # appends an item to the end of the list and only the end
    def addItem(self, newItem):
        self.theQueue.append(newItem)

    # removes the oldest item from the list
    def removeNext(self):
        self.theQueue.pop(0)

    def checkNext(self):
        return self.theQueue[0]
    


# In[ ]:





# In[12]:


waitingQueue = Queue()


queuedFloors: list[int] = [] #queuedFloors would be the initial set of buttons pressed when someone gets on the elevator when the elvator has no other locations
currentFloor: int = 1

calledUp: list[int] = []
calledDown: list[int] = []

config = load_config_from_file("config.json")
requestDict = {}
for i in config["requests"].keys():
    try:
        requestDict[int(i)] = config["requests"][i]
    except ValueError:
        raise ValueError("A key exists in the dictionary that can't be converted into an integer")

# adds the floors that have call up requests and call down requests to their respective list
for i in requestDict.keys():
    for k in requestDict[i]:
        if k < currentFloor:
            calledDown.append(i)
            waitingQueue.addItem(i)
        else:
            calledUp.append(i)
            waitingQueue.addItem(i)


# these values determine how much the elevator can hold
hardCapacity: int = config["capacity"] # hardCapacity is the limit at which no one else can get on the elevator or else the elevator stops and waits for others to get off
softCapacity: int = hardCapacity/1.5 # softCapacity is the limit where the elevator ignores requests to get on the elevator so it can be reduce weight
weightCount: int = 0 # this measures how many people are on the elevator


heightCheck: int = config["num_floors"]  # an easier variable to remember

# creates a list of all floors mentioned to exist in the config
allFloors = calledDown + calledUp
for i in requestDict.keys():
    allFloors.append(i)
    if len(requestDict[i]) > 0:
        allFloors.append(max(requestDict[i]))
        allFloors.append(min(requestDict[i]))

# makes sure the number of floors claimed to exist is equal or greater than the number of floors that exists in the dictionary
if (max(allFloors) - min(allFloors) + 1) > heightCheck:
    print("Floor count is less than the amount of floors on the elevator, exiting program")
    raise SystemExit(0)

# fills in any missing floors in the list
for i in range(heightCheck):
    allFloors.append(i + min(allFloors))

# removes any floors that already exist in the dictionary
for i in requestDict.keys():
    while i in allFloors:
        allFloors.remove(i)

# fills in any missing floors in the dictionary
for i in allFloors:
    requestDict[i] = []


# In[13]:


movements = 0
stops = []
debug = True

stopEntered: list = []
stopLeft: list = []
weightDecrease: int = 0
weightIncrease: int = 0
stopCheck: bool = True

timeCheck: bool = False
timeCount: int = 0
timeLimit: int = heightCheck
prior: str = "none"
direction: str = "none"
while True:
    weightDecrease = 0
    weightIncrease = 0
    
    stopCheck = True
    reset = False
    stopHere = floorCheck(currentFloor, queuedFloors) # checks if there any floors to stop at
    stopHereup = floorCheck(currentFloor, calledUp)
    stopHeredown = floorCheck(currentFloor,calledDown)

    if ((stopHereup == True and direction == "up") or (stopHeredown == True and direction == "down")) and weightCount < softCapacity: # the elevator won't stop to let new people on if it's at the softcap for weight
            if stopHereup == True:
                while currentFloor in calledUp:
                    calledUp.remove(currentFloor)
                for i in range(len(requestDict[currentFloor])):
                    queuedFloors.append(requestDict[currentFloor][0])
                    waitingQueue.addItem(requestDict[currentFloor][0])
                    requestDict[currentFloor].pop(0)
                    weightCount = weightCount + 1
                    weightIncrease = weightIncrease + 1
                    if debug:
                        print("weight (increased) =", weightCount) # keeps track of changes in weight
                stopHereup = False
    
            if stopHeredown == True:
                while currentFloor in calledDown:
                    calledDown.remove(currentFloor)
                for i in range(len(requestDict[currentFloor])):
                    queuedFloors.append(requestDict[currentFloor][0])
                    waitingQueue.addItem(requestDict[currentFloor][0])
                    requestDict[currentFloor].pop(0)
                    weightCount = weightCount + 1
                    weightIncrease = weightIncrease + 1
                    if debug:
                        print("weight (increased) =", weightCount) # keeps track of changes in weight

                stopHeredown = False

            stops.append(currentFloor)
            stopCheck = False
            if debug:
                print("Stopped at floor:", currentFloor) # informs of a stop
                print("New queued floors: ", queuedFloors)
                print("")
        

    
        
    
    if stopHere == True: # opens to let people off the elevator, but can't stop people from getting on if there are any
        if stopHere == True: # a redundant check that I'll remove
            timeCheck = True
            y = 0 # counter in order to remove every entry of the current floor from the queuedFloors list
            for i in queuedFloors:
                if currentFloor == i:
                    weightCount = weightCount - 1
                    weightDecrease = weightDecrease + 1
                    if debug:
                        print("weight (reduced) =", weightCount) # keeps track of changes in weight
                    y = y + 1
                    # print(i)
            for i in range(y):
                queuedFloors.remove(currentFloor)
            
        if stopHereup == True:
            while currentFloor in calledUp:
                calledUp.remove(currentFloor)
            for i in range(len(requestDict[currentFloor])):
                waitingQueue.addItem(requestDict[currentFloor][0])
                queuedFloors.append(requestDict[currentFloor][0])
                requestDict[currentFloor].pop(0)
                weightCount += 1
                weightIncrease = weightIncrease + 1
                if debug:
                    print("weight (increased) =", weightCount) # keeps track of changes in weight
                    print(requestDict[currentFloor])


        if stopHeredown == True:
            while currentFloor in calledDown:
                calledDown.remove(currentFloor)
            for i in range(len(requestDict[currentFloor])):
                waitingQueue.addItem(requestDict[currentFloor][0])
                queuedFloors.append(requestDict[currentFloor][0])
                requestDict[currentFloor].pop(0)
                weightCount += 1
                weightIncrease = weightIncrease + 1
                if debug:
                    print("weight (increased) =", weightCount) # keeps track of changes in weight
                    print(requestDict[currentFloor])
                
        if stopCheck == True:
            stops.append(currentFloor)
            stopCheck = False

        if debug:
            print("Stopped at floor:", currentFloor) # informs of a stop
            print("New queued floors: ", queuedFloors)
            print("")

    if stopCheck == False:
        stopEntered.append(weightIncrease)
        stopLeft.append(weightDecrease)
        
    if weightCount > hardCapacity: # if the elevator goes above its hardCapacity this simulates passengers leaving and waiting for the elevator to return
        weightDifference: int = weightCount - hardCapacity
        if debug:
            print("Previous queued floors: ", queuedFloors)
        for i in range(weightDifference):
            waitingQueue.addItem(currentFloor)
            goneDestination = queuedFloors[0]
            queuedFloors.pop(0)
            if goneDestination > currentFloor:  # checks if the passenger was travelling up or down
                calledUp.append(currentFloor)
            else:
                calledDown.append(currentFloor)
            requestDict[currentFloor].append(goneDestination)
            weightCount = weightCount - 1
            if debug:
                print("weight (reduced) =", weightCount) # keeps track of changes in weight
                print("New queued floors: ", queuedFloors)
            # print("New called up: ", calledUp)
            # print("New called down: ", calledDown)
        
        if debug:
            print("Passenger(s) left early due to overcrowding at floor:", currentFloor) # informs of a stop
            print("")
            
    timeCount = timeCount + 1
    for i in range(waitingQueue.size()):
        if waitingQueue.checkNext in queuedFloors or waitingQueue.checkNext in calledUp or waitingQueue.checkNext in calledDown:
            break;
        else:
            timeCount = 0
            waitingQueue.removeNext()
    if ((timeCheck == True) and (timeCount > timeLimit)) and (waitingQueue.size() > 0):
        if waitingQueue.checkNext() > currentFloor:
            direction = "up"
            currentFloor = currentFloor + 1
            movements += 1
            prior = direction
            queuedFloors.append(waitingQueue.checkNext)
            if debug:
                print("Current Floor =", currentFloor)
            continue
        else:
            direction = "down"
            currentFloor = currentFloor - 1
            movements += 1
            prior = direction
            queuedFloors.append(waitingQueue.checkNext)
            if debug:            
                print("Current Floor =", currentFloor)
            continue

    if len(calledUp) != 0 or len(calledDown) != 0: 
        callCheck = True
    else:
        callCheck = False
    
    if len(queuedFloors) == 0 and callCheck == True: # if there are no more queued floors and there are people calling the elevator, this determines the direction to prioritise
        direction = takeRequest(currentFloor, calledUp, calledDown)
        reset = True

        if direction == "up":
            destination = max(calledDown)
            if currentFloor > destination: # checks if the destination is above or below the current floor
                x = -1
            else: 
                x = 1
            while True:
                if currentFloor == destination: # checks to see if the currentFloor is one floor away from destination
                    direction = "down" # as the person called down, the elevator's next direction is down
                    reset = True
                    break
                else:
                    currentFloor = currentFloor + x # this will repeat until it reaches the correct floor
                    if debug:
                        print("Current Floor =", currentFloor)
                    movements = movements + 1


        elif direction == "down": 
            destination = min(calledUp)
            if currentFloor < destination:
                x = 1
            else: 
                x = -1

            while True:
                if currentFloor == destination: # checks to see if the currentFloor is one floor away from destination
                        direction = "up"
                        reset = True
                        break
                else:
                    currentFloor = currentFloor + x
                    if debug:
                        print("Current Floor =", currentFloor)
                    movements = movements + 1

                    
    if reset == True:
        reset = False
        continue
        
    if len(queuedFloors) == 0 and len(calledUp) == 0 and len(calledDown) == 0:
        break
                    


    
    if len(queuedFloors) > 0 and prior == "none": # this happens if the elevator going in no direction and at least one person on the elevator has picked a location
        direction = pathing(currentFloor, queuedFloors)
    else:
        check1 = pathing(currentFloor, queuedFloors)
        if prior == check1: # this checks if the elevator should stay moving in its current direction based on whether there are any more floors to stop at
            direction = prior
        else:
            direction = pathing(currentFloor, queuedFloors)

    if direction == "up": # sends the elevator up or down depending on the direction
        currentFloor = currentFloor + 1
        movements = movements + 1
    elif direction == "down":
        currentFloor = currentFloor - 1
        movements = movements + 1
    else:
        break
    prior = direction
    if debug:
        print("Current Floor =", currentFloor)




# In[ ]:





# In[ ]:





# In[14]:


returningDictionary = {"stops" : list(stops), "movements" : int(movements), "on" : list(stopEntered), "off" : list(stopLeft)}


# In[15]:


print(returningDictionary)


# In[ ]:





# In[ ]:




