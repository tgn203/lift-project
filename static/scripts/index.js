// Open file dialog on button press
document.getElementById("uploadButton").addEventListener("click", function () {
    document.getElementById("fileInput").click();
});

// POST the file when uploaded
document.getElementById("fileInput").addEventListener("change", function () {
    let file = this.files[0];
    
    // If no file is uploaded, don't do anything
    if (!file) return;

    // Add the file as form data (to be extracted by Flask)
    let formData = new FormData();
    formData.append("file", file);

    // Upload to index route via POST
    fetch("/", {
        method: "post",
        body: formData,
    })
    .then(response => response.text())
    .then(data => {
        // Redirect to the animation page
        window.location.href = "/algorithm";
    })
    .catch(error => console.error("Error: ", error));
});
