#!/usr/bin/env python

"""
frontend.py
Thomas Noakes, 2025

Handles all web-related requests to create a website GUI.
Utilises Flask as a web server, serving dynamically formatted HTML templates,
with CSS for styling and Javascript for scripting
"""

import sys
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    Response,
)
from typing import cast
import secrets
import logging

# Flask configuration variables
FLASK_PORT = 8080
FLASK_TEMPLATE_FOLDER = "../templates"
FLASK_STATIC_FOLDER = "../static"

# Set up Flask application
app = Flask(__name__)
app.template_folder = FLASK_TEMPLATE_FOLDER
app.static_folder = FLASK_STATIC_FOLDER

# Create and assign a 32-bit (64 character) secret key for session storage
SECRET_KEY = secrets.token_hex(32)
app.secret_key = SECRET_KEY


# Default homepage
@app.route("/", methods=["GET"])
def Index() -> str:
    return render_template("index.html")


# Apply config
@app.route("/config", methods=["GET", "POST"])
def Config() -> Response | str:
    if request.method == "POST":
        config: dict[str, int | dict[str, list[int]]] = {}

        # Get values from form
        num_floors = str(request.form.get("numFloorsInput"))
        capacity = str(request.form.get("capacityInput"))

        config["num_floors"] = int(num_floors)
        config["capacity"] = int(capacity)

        # Get the requests for each floor
        requests_dict: dict[str, list[int]] = {}
        for i in range(int(num_floors)):
            floor_requests = request.form.get(f"floor{i+1}Input")

            if floor_requests:
                floor_requests_list = floor_requests.split(",")
                floor_requests_ints = [int(x) for x in floor_requests_list]
                requests_dict[str(i + 1)] = floor_requests_ints

        config["requests"] = requests_dict

        # Add the config to the session storage
        session["config"] = config

        return cast(Response, redirect(url_for("Animation")))

    # A list of options and their formatting that is passed to the HTML
    # template. Format = {literalName: [type, prettyName, defaultValue]}
    CONFIG_OPTIONS: dict[str, list] = {
        "numFloors": ["number", "Number of floors", 1],
        "capacity": ["number", "Lift Capacity", 1],
    }

    return render_template("config.html", config_options=CONFIG_OPTIONS)


# Display the animation
@app.route("/animation", methods=["GET"])
def Animation() -> str | Response:
    # Check if config has been generated
    if "config" in session.keys():
        return render_template("animation.html", config=session["config"])

    # Otherwise, redirect to config setup page
    return cast(Response, redirect(url_for("Config")))


# Return JSON data
@app.route("/data", methods=["GET"])
def Data() -> Response:
    # Retrieve the config from session storage

    # TODO: implement running the algorithm
    # Example output:

    data = {
        "config": session["config"],
        "stops": [1, 2, 3, 4, 2, 1],
        "movements": 4,
        "on": [3, 1, 2, 1, 4, 1],
        "off": [1, 2, 1, 4, 1, 2],
    }

    return jsonify(data)


if __name__ == "__main__":
    # Check for debug mode in command-line arguments
    debug_mode = False
    if "--debug" in sys.argv:
        debug_mode = True

    # Set logging verbosity based on debug mode
    # Werkzeug is the engine behind Flask, so provides the logging handle
    logger = logging.getLogger("werkzeug")
    if debug_mode:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)

    # Start the Flask webserver
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=debug_mode)
