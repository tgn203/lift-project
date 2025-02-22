// Reset the checkbox to unchecked at page load
document.getElementById('toggleCheckbox').checked = false;

function toggleLiteralNames() {
    // Get the checkbox object and arrays of all the label items
    const toggleCheckbox = document.getElementById("toggleCheckbox");
    const literalNamesLabels = document.querySelectorAll(".literal-name");
    const prettyNamesLabels = document.querySelectorAll(".pretty-name");

    // Toggle the visibility of the labels based on the state of the button
    var state = toggleCheckbox.checked;
    literalNamesLabels.forEach(label => {
        label.style.display = state ? 'inline-block' : 'none';
    });
    prettyNamesLabels.forEach(label => {
        label.style.display = state ? 'none' : 'inline-block';
    });
}

// Update the number of floors input
function updateFloorsInput() {
    const numFloorsInput = document.getElementById("numFloorsInput");
    const numFloors = parseInt(numFloorsInput.value) || 0;  // Zero if invalid
    const floorsInputContainer = document.getElementById("floorInputs");

    // Check the input is a non-zero integer
    const numFloorsIsValid = !isNaN(numFloors) && numFloors > 0;
    // Automatically converts to integer, however check if there is a decimal
    const numFloorsIsFloat = numFloorsInput.value.includes(".");
    numFloorsInput.classList.toggle("error", !numFloorsIsValid || numFloorsIsFloat);
    

    // Remove all existing floor inputs
    floorsInputContainer.innerHTML = "";

    for (let i = 0; i < numFloors; i++) {
        const newDiv = document.createElement("div");
        newDiv.classList.add("form-group", "floor-input");
        newDiv.innerHTML = `
            <label for="floor${i + 1}Input">
                <p class="pretty-name">Waiting on Floor ${i + 1}:</p>
                <p class="literal-name">floor${i + 1}waiting:</p>
            </label>
            <input class type="text" id="floor${i + 1}Input" placeholder="Waiting...">
        `;
        floorsInputContainer.appendChild(newDiv);
    }
}

const numFloorsInput = document.getElementById("numFloorsInput");
numFloorsInput.addEventListener("input", updateFloorsInput);
