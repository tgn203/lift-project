#!/usr/bin/env python
# coding: utf-8

# In[2]:


# queuedFloors.remove(-2)


# In[17]:


# queuedFloors


# In[2]:


queuedFloors = [-2, 5, 7, -9]


# In[4]:


currentFloor = 0


# In[5]:


# top = 9 # I intended to use this to set the limits of the elevator but it ended up being useless
# bottom = -9
# floorCount = top - bottom


# In[6]:


def floorCheck(currentFloor, queuedFloors): # a simple check to see if the current floor is inside a list
    if currentFloor in queuedFloors:
        return True 
    else:
        return False
    


# In[7]:


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
    
    


# In[8]:


while True: # the most basic version that just makes the elevator visit all floors on the list given as the shortest route
    stopHere = floorCheck(currentFloor, queuedFloors)
    if stopHere == True:
        queuedFloors.remove(currentFloor)
        print(currentFloor)
    direction = pathing(currentFloor, queuedFloors)
    if direction == "up":
        currentFloor = currentFloor + 1
    elif direction == "down":
        currentFloor = currentFloor - 1
    else:
        break


# In[9]:


backupQueue = [6, 8, 0]
queuedFloors = [-2, 5, 7, -9]
currentFloor = 0


# In[ ]:



    


# In[10]:


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
    


# In[11]:


prior = "none"
while True: # adds the additional instructions so that it continues going in a direction if there's floors further in the backupQueue
    stopHere = floorCheck(currentFloor, queuedFloors) 
    stopHerebackup = floorCheck(currentFloor, backupQueue)
    if stopHere == True or stopHerebackup == True: 
        if stopHere == True:
            queuedFloors.remove(currentFloor)
        if stopHerebackup == True:
            backupQueue.remove(currentFloor)
        print(currentFloor)

    if len(queuedFloors) == 0:
        queuedFloors = backupQueue
        backupQueue = []
    
    if len(queuedFloors) > 0 and prior == "none":
        direction = pathing(currentFloor, queuedFloors)
    else:
        if prior == "up":
            check1 = pathing(currentFloor, queuedFloors)
            check2 = followup(currentFloor, backupQueue, prior)
            if check1 == "up" or check2 == True:
                direction = "up"
            else:
                direction = pathing(currentFloor, queuedFloors)
        if prior == "down":
            check1 = pathing(currentFloor, queuedFloors)
            check2 = followup(currentFloor, backupQueue, prior)
            if check1 == "down" or check2 == True:
                direction = "down"
            else:
                direction = pathing(currentFloor, queuedFloors)

    if direction == "up":
        currentFloor = currentFloor + 1
    elif direction == "down":
        currentFloor = currentFloor - 1
    else:
        break
    prior = direction


# In[12]:


calledUp = []
calledDown = []


# In[13]:


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
    
    


# In[17]:


backupQueue = [6, 8, 0] # backup queue contains the later set of buttons pressed when the elevator already has locations in queuedFloors, it is currently redundant at the moment
queuedFloors = [-2, 5, 7, -9] #queuedFloors would be the initial set of buttons pressed when someone gets on the elevator when the elvator has no other locations
currentFloor = 0
calledUp = [-13]
calledDown = [10, 9, - 14]


prior = "none"
direction = "none"
# while True:
# for silly in range(69):
while True:
    reset = False
    stopHere = floorCheck(currentFloor, queuedFloors) # checks if there any floors to stop at
    stopHerebackup = floorCheck(currentFloor, backupQueue)
    stopHereup = floorCheck(currentFloor, calledUp)
    stopHeredown = floorCheck(currentFloor,calledDown)

    
    if stopHere == True or stopHerebackup == True or stopHereup == True or stopHeredown == True: # 
        if stopHere == True:
            queuedFloors.remove(currentFloor)
        if stopHerebackup == True:
            backupQueue.remove(currentFloor)
        if stopHereup == True:
            calledUp.remove(currentFloor)
            print(currentFloor)
            print(stopHereup) # I used some of these prints to make sure everythings working and to keep trck of the floors
        if stopHeredown == True:
            calledDown.remove(currentFloor)
            print(currentFloor)
            print(stopHeredown)

        print(currentFloor)

    if len(queuedFloors) == 0: # if queuedFloors is empty then everything from the backupQueue replaces it
        queuedFloors = backupQueue
        backupQueue = []

    if len(calledUp) != 0 or len(calledDown) != 0: 
        callCheck = True
    else:
        callCheck = False
    
    if len(queuedFloors) == 0 and callCheck == True: # if there are no more queued floors and there are people calling the elevator, this determines the direction to prioritise
        direction = takeRequest(currentFloor, calledUp, calledDown)

        if direction == "up":
            destination = calledDown[0]
            for i in calledDown:
                if i > destination: # chooses the highest possible floor to travel too
                    destination = i
                if currentFloor > destination: # checks if the destination is above or below the current floor
                    x = -1
                else: 
                    x = 1
            # for useless in range(30): # Used for loops in testing to stop the program crashing
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
                    print(currentFloor)

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
                    print(currentFloor)
                    
    if reset == True:
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


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




