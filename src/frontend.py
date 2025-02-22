#!/usr/bin/env python

"""
frontend.py
Thomas Noakes, 2025

Handles all web-related requests to create a website GUI.
Utilises Flask as a web server, serving dynamically formatted HTML templates,
with CSS for styling and Javascript for scripting
"""

import sys
from flask import Flask, render_template, request, redirect, url_for

# Flask configuration variables
FLASK_PORT = 8080
FLASK_TEMPLATE_FOLDER = "../templates"
FLASK_STATIC_FOLDER = "../static"

# Set up Flask application
app = Flask(__name__)
app.template_folder = FLASK_TEMPLATE_FOLDER
app.static_folder = FLASK_STATIC_FOLDER


# Default homepage
@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


# Apply config
@app.route("/config", methods=["GET", "POST"])
def Config() -> str:
    if request.method == "POST":
        config = {}

        # Get values from form
        num_floors = int(request.form.get("numFloorsInput"))
        capacity = int(request.form.get("capacityInput"))

        config["num_floors"] = num_floors
        config["capacity"] = capacity
        config["requests"] = {}

        # Get the requests for each floor
        for i in range(num_floors):
            floor_requests = request.form.get(f"floor{i+1}Input")
            if floor_requests:
                floor_requests = floor_requests.split(",")
                floor_requests = [int(x) for x in floor_requests]
                config["requests"][i+1] = floor_requests

        print(config)

        return redirect(url_for("index"))

    # A list of options and their formatting that is passed to the HTML
    # template. Format = {literalName: [type, prettyName, defaultValue]}
    CONFIG_OPTIONS: dict[str, list] = {
        "numFloors": ["number", "Number of floors", 1],
        "capacity": ["number", "Lift Capacity", 1],
    }

    return render_template("config.html", config_options=CONFIG_OPTIONS)


if __name__ == "__main__":
    # Check for debug mode in command-line arguments
    debug_mode = False
    if "--debug" in sys.argv:
        debug_mode = True

    # Start the Flask webserver
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=debug_mode)
