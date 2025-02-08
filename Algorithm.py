#!/usr/bin/env python
# coding: utf-8

# In[15]:


def floorCheck(currentFloor, queuedFloors): # a simple check to see if the current floor is inside a list
    if currentFloor in queuedFloors:
        return True 
    else:
        return False
    


# In[16]:


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
    for i in queuedFloors: # compares the distances until it finds the furthest distance up and down
        distance = i - currentFloor
        if distance > finalUp: 
            finalUp = distance
        elif distance < finalDown:
            finalDown = distance
    finalDown = finalDown*-1 # makes the downward distance positive for comparison
    if finalUp < finalDown: # the shorter distance is chosen 
        return "up" 
    else:
        return "down"
    
    


# In[17]:


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
    


# In[18]:


def takeRequest(currentFloor, calledUp, calledDown): # this would be used if the elevator has no one on it but there are people calling it
    checkUp = True
    checkDown = True
    # for i in queuFloors:
    #     if i > currentFloor:
    #         checkUp = True
    #     elif i < currentFloor:
            # checkDown = True
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
    
    


# In[19]:


# next one: fixing the issue when passengers want to go to the same floor by replacing instances of .remove with .pop


# In[22]:


floorLimits: list = [-5, 5]
requestDict: dict = {}
for i in range(floorLimits[0], floorLimits[1] + 1):
    requestDict[i] = []
requestDict[4].append(2) # these are test values to show how the program should work, however in practice I expect the dictionary to be made with something imported
requestDict[4].append(2)
requestDict[4].append(3)

requestDict[4].append(-4)
requestDict[5].append(0)
# requestDict[5].append(0)
# requestDict[5].append(0)

requestDict[1].append(4)
requestDict[-3].append(-2)
requestDict[-2].append(5)

queuedFloors: list[int] = [] #queuedFloors would be the initial set of buttons pressed when someone gets on the elevator when the elvator has no other locations
currentFloor: int = 0

calledUp: list[int] = []
calledDown: list[int] = []

for i in requestDict.keys():
    for k in requestDict[i]:
        if k < currentFloor:
            calledDown.append(i)
        else:
            calledUp.append(i)

hardCapacity: int = 15
softCapacity: int = hardCapacity/2
weightCount: int = 0

backupQueue = [] # this is currently redundant and I intend on getting rid of everything related to it soon if I can't find any reason to keep it


# In[23]:


prior: str = "none"
direction: str = "none"
while True:
    reset = False
    stopHere = floorCheck(currentFloor, queuedFloors) # checks if there any floors to stop at
    stopHerebackup = floorCheck(currentFloor, backupQueue)
    stopHereup = floorCheck(currentFloor, calledUp)
    stopHeredown = floorCheck(currentFloor,calledDown)

    if ((stopHereup == True and direction == "up") or (stopHeredown == True and direction == "down")) and weightCount < softCapacity: # the elevator won't stop to let new people on if it's at the softcap for weight
            if stopHereup == True:
                calledUp.remove(currentFloor)
                for i in range(len(requestDict[currentFloor])):
                    queuedFloors.append(requestDict[currentFloor][0])
                    requestDict[currentFloor].pop(0)
                    weightCount += 1
                    print("weight (increased) =", weightCount) # keeps track of changes in weight
                stopHereup = False
    
            if stopHeredown == True:
                calledDown.remove(currentFloor)
                for i in range(len(requestDict[currentFloor])):
                    queuedFloors.append(requestDict[currentFloor][0])
                    requestDict[currentFloor].pop(0)
                    weightCount += 1
                    print("weight (increased) =", weightCount) # keeps track of changes in weight

                stopHeredown = False
            print("Stopped at floor:", currentFloor) # informs of a stop
            print("")

    
        
    
    if stopHere == True or stopHerebackup == True: # opens to let people off the elevator, but can't stop people from getting on if there are any
        if stopHere == True:
            y = 0 # counter in order to remove every entry of the current floor from the queuedFloors list
            for i in queuedFloors:
                if currentFloor == i:
                    weightCount = weightCount - 1
                    print("weight (reduced) =", weightCount) # keeps track of changes in weight
                    y = y + 1
                    # print(i)
            for i in range(y):
                queuedFloors.remove(currentFloor)
            
        if stopHereup == True:
            calledUp.remove(currentFloor)

            for i in range(len(requestDict[currentFloor])):
                queuedFloors.append(requestDict[currentFloor][0])
                requestDict[currentFloor].pop(0)
                weightCount += 1
                print("weight (increased) =", weightCount) # keeps track of changes in weight
                print(requestDict[currentFloor])


        if stopHeredown == True:
            calledDown.remove(currentFloor)
            for i in range(len(requestDict[currentFloor])):
                queuedFloors.append(requestDict[currentFloor][0])
                requestDict[currentFloor].pop(0)
                weightCount += 1
                print("weight (increased) =", weightCount) # keeps track of changes in weight
                print(requestDict[currentFloor])


        print("Stopped at floor:", currentFloor) # informs of a stop
        print("")

    if len(queuedFloors) == 0: # if queuedFloors is empty then everything from the backupQueue replaces it
        queuedFloors = backupQueue
        backupQueue = []

    if len(calledUp) != 0 or len(calledDown) != 0: 
        callCheck = True
    else:
        callCheck = False
    
    if len(queuedFloors) == 0 and callCheck == True: # if there are no more queued floors and there are people calling the elevator, this determines the direction to prioritise
        direction = takeRequest(currentFloor, calledUp, calledDown)
        reset = True

        if direction == "up":
            destination = calledDown[0]
            for i in calledDown:
                if i > destination: # chooses the highest possible floor to travel too
                    destination = i
                if currentFloor > destination: # checks if the destination is above or below the current floor
                    x = -1
                else: 
                    x = 1
            while True:
                if currentFloor == destination: # checks to see if the currentFloor is one floor away from destination
                    destinationCheck = destination
                    
                    for p in calledDown: # checks to see if there are any new floors further away than the destination, I made it with the idea that there will be a way to take additional input
                        if p > destinationCheck:
                            destinationCheck = p
                    if destinationCheck == destination: # if there are no further floors then the while True loop breaks
                        direction = "down" # as the person called down, the elevator's next direction is down
                        reset = True
                        break
                    else:
                        destination = destinationCheck # sets the new destination if there's now a further one
                        if currentFloor < destination:
                            x = 1
                        currentFloor = currentFloor + x
                        
                else:
                    currentFloor = currentFloor + x # this will repeat until it reaches the correct floor
                    print("Current Floor =", currentFloor)


        elif direction == "down": 
            destination = calledUp[0]
            for i in calledUp:
                if i > destination:
                    destination = i

                if currentFloor < destination:
                    x = 1
                else: 
                    x = -1

            while True:
                if currentFloor == destination: # checks to see if the currentFloor is one floor away from destination
                    destinationCheck = destination
                    
                    for i in calledUp: # checks to see if there are any new floors further away than the destination, I made it with the idea that there will be a way to take additional input
                        if i > destinationCheck:
                            destinationCheck = i
                    if destinationCheck == destination: # if there are no further floors then the while True loop breaks
                        direction = "up"
                        reset = True
                        break
                    else:
                        destination = destinationCheck # sets the new destination if there's now a further one
                        if currentFloor > destination:
                            x = -1
                        currentFloor = currentFloor + x
                else:
                    currentFloor = currentFloor + x
                    print("Current Floor =", currentFloor)

                    
    if reset == True:
        reset = False
        continue
        

                    


    
    if len(queuedFloors) > 0 and prior == "none": # this happens if the elevator going in no direction and at least one person on the elevator has picked a location
        direction = pathing(currentFloor, queuedFloors)
    else:
        if prior == "up": # if the elevator was previously going up, this checks if it should still go up
            check1 = pathing(currentFloor, queuedFloors)
            check2 = followup(currentFloor, backupQueue, prior)
            if check1 == "up" or check2 == True:
                direction = "up"
            else:
                direction = pathing(currentFloor, queuedFloors)
        if prior == "down": # if the elevator was previously going down this checks if it should still go down
            check1 = pathing(currentFloor, queuedFloors)
            check2 = followup(currentFloor, backupQueue, prior)
            if check1 == "down" or check2 == True:
                direction = "down"
            else:
                direction = pathing(currentFloor, queuedFloors)

    if direction == "up": # sends the elevator up or down depending on the direction
        currentFloor = currentFloor + 1
    elif direction == "down":
        currentFloor = currentFloor - 1
    else:
        break
    prior = direction
    print("Current Floor =", currentFloor)




# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




