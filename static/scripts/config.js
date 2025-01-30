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
