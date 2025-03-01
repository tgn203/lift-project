// Global variables set in the setup function
let floorHeight = null;
let capacity = 0;
let stops = null;
let currentFloor = null;
let boardingList = [];  // Track the number of people boarding per movement
let exitingList = [];   // Track the number of people exiting per movement
let peopleOnOffset = [];  // Used for ensuring boarding animations can play in reverse
let peopleOffOffset = [];  // Used for ensuring boarding animations can play in reverse

let numPasseners = 0;
let currentIndex = 0;
let moving = false;
let animationInterval = null;   // Used to start and stop the animation with the same button

// Translate the elevator div
function moveElevator(floor) {  
    elevator.style.transform = `translateY(-${(floor - 1) * floorHeight}px)`;
}

// Toggle if the animation is playing
function playPauseAnimation() {
    // Apply styles with the negative of the pre-changed state to avoid the delays
    stylePlayButton(!moving)

    if (moving) {
        // Cancel any animations
        clearInterval(animationInterval);
        moving = false;
    } else {
        moving = true;

        // Immediately make one move, if possible (skips delay from Interval)
        stepForward();

        // Set a recurring function to happen every 1s
        animationInterval = setInterval(() => {
            if (currentIndex < stops.length - 1) {
                // If there are animation steps left, move
                stepForward();
            } else {
                // End the animation once no steps remain
                clearInterval(animationInterval);
                moving = false;
            }
        }, 1750)
    }
}

// Do one previous step of the animation
function stepBackward() {
    // If there are any moves made, undo the last one
    if (currentIndex > 0) {
        // Move passengers then apply a small amount of delay
        handlePassengersReverse(currentIndex);
        
        setTimeout(() => {
            currentIndex--;
            currentFloor = stops[currentIndex];
            moveElevator(currentFloor);
        }, 1750);
    };
}

// Do one next step of the animation
function stepForward() {
    // If there are any moves remaining, make the next one
    if (currentIndex < stops.length - 1) {
        currentIndex++;
        currentFloor = stops[currentIndex];
        moveElevator(currentFloor);

        // Apply a small delay then move passengers
        setTimeout(() => handlePasseners(currentIndex), 750);
    }    
}

function handlePasseners(index) {
    // Handle passeners embarking
    let on = boardingList[index - 1];
    let off = exitingList[index - 1];

    // Remove people from floor who are boarding
    let floor = document.getElementById(`floor${currentFloor}`);
    let peopleList = Array.from(floor.children);

    for (let i = 0; i < on; i++) {
        // Note: +1 skips the floor label
        peopleList[i + 1].style.transform = "translateX(-1000px)";
    }
    peopleOnOffset[currentFloor - 1] = peopleOnOffset[currentFloor - 1] + on;

    // Add people to the floor who are exiting
    let extraFloor = document.getElementById(`extraFloor${currentFloor}`);

    for (let i = 0; i < off; i++) {
        // Create a new person in a separate "layer"
        let newPerson = document.createElement("img");
        newPerson.classList.add("person");
                    
        // Apply the image
        newPerson.src = "static/images/person.svg";
        newPerson.alt = "Person";

        newPerson.style.transform = `translateX(${-500 + 40*i}px)`;
        extraFloor.appendChild(newPerson);
        
        // Wait before moving them
        setTimeout(() => {newPerson.style.transform = `translateX(${1500 + 40*i}px)`}, 50);
    }
    peopleOffOffset[currentFloor - 1] = peopleOffOffset[currentFloor - 1] + off;

    // Change the text on the elevator to new number of passengers
    const capacityText = document.getElementById("capacity-text");
    numPasseners = numPasseners + on - off;
    capacityText.innerHTML = `${numPasseners}/${capacity}`;
}

function handlePassengersReverse(index) {
    // This is used when the step backwards button is used
    let on = boardingList[index - 1];
    let off = exitingList[index - 1];

    // Place previously exited people back on
    offOffset = peopleOffOffset[currentFloor - 1];
    let extraFloor = document.getElementById(`extraFloor${currentFloor}`);
    let extraPeopleList = Array.from(extraFloor.children);

    for (let i = 0; i < off; i++) {
        let oldPerson = extraPeopleList.at(-(i+1));     // Use negative index to subtract from the 'back' of the array
        oldPerson.style.transform = `translateX(${-500 - 40*i}px)`; 
        setTimeout(() => {extraFloor.removeChild(oldPerson)}, 5000);
    }
    peopleOffOffset[currentFloor - 1] = peopleOffOffset[currentFloor - 1] - off;

    // Take previously boarded people back off
    let floor = document.getElementById(`floor${currentFloor}`);
    let peopleList = Array.from(floor.children);

    onOffset = peopleOnOffset[currentFloor - 1];
    for (let i = 0; i < on; i++) {
        // Note: no -1 skips the floor label
        peopleList[onOffset - i].style.transform = "translateX(0px)";
    }
    peopleOnOffset[currentFloor - 1] = peopleOnOffset[currentFloor - 1] - on;

    // Change the text on the elevator to new number of passengers
    const capacityText = document.getElementById("capacity-text");
    numPasseners = numPasseners - on + off;
    capacityText.innerHTML = `${numPasseners}/${capacity}`;
}

function stylePlayButton(moving) {
    const playPauseButton = document.getElementById("start-stop-btn");
    const playImg = document.getElementById("play-img");
    const pauseImg = document.getElementById("pause-img");

    if (moving) {
        // Change to green, hide play and show pause
        playPauseButton.style.backgroundColor = "var(--colour-accent)";
        playImg.style.display = "none";
        pauseImg.style.display = "block";

    } else {
        // Change to white, hide pause and show play
        playPauseButton.style.backgroundColor = "var(--text-dark)";
        pauseImg.style.display = "none";
        playImg.style.display = "block";
    }
}

function setup() {
    // Initialise DOM elements
    const shaft = document.getElementById("shaft");
    const elevator = document.getElementById("elevator");

    // Load output from the algorithm
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            // Assign global variables
            capacity = data.config.capacity;
            stops = data.stops;
            currentFloor = stops[0];
            boardingList = data.on;
            exitingList = data.off;

            // Give elevator correct height
            let numFloors = data.config.num_floors;
            floorHeight = shaft.getBoundingClientRect().height / numFloors;
            elevator.style.height = `${floorHeight * 0.95}px`;

            // Initialise arrays for boarding and exiting
            peopleOnOffset = new Array(numFloors).fill(0);
            peopleOffOffset = new Array(numFloors).fill(0);

            // Add people to floors
            requests = data.config.requests;
            Object.entries(requests).forEach(([floor, waiting]) => {
                // Get each floor in turn
                let floorElement = document.getElementById(`floor${floor}`);

                waiting.forEach(person => {
                    // Add each new person in turn
                    let newPerson = document.createElement("img");
                    newPerson.classList.add("person");
                    
                    // Apply the image
                    newPerson.src = "static/images/person.svg";
                    newPerson.alt = "Person";

                    // Add to the floor element
                    floorElement.appendChild(newPerson);
                });
            });
        })
        .catch(error => console.error("Error: " + error));
}

// When the page loads
document.addEventListener("DOMContentLoaded", function () {
    setup();
});
