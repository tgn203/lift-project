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
import os
from copy import deepcopy

from inputread import load_config_from_file
from algs.ed_algorithm import algorithm as ed_algorithm
from algs.max_algorithm import run_algorithm as max_algorithm
from algs.look import algorithm as look_algorithm
from algs.scan import algorithm as scan_algorithm

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
@app.route("/", methods=["GET", "POST"])
def Index() -> Response | str:
    if request.method == "POST":
        # Get the files from the 'form'
        if "file" not in request.files:
            return "No file part found"

        # Get and check the filename
        file = request.files["file"]
        filename = file.filename
        if filename == "":
            return "No selected file"

        # The file must be saved to access the contents
        filepath = os.path.join(os.path.dirname(__file__), filename)
        file.save(filepath)

        # Add the config to session storage
        config = load_config_from_file(filepath)
        session["config"] = config

        print(f"config = {session["config"]}")

        # Redirect to animation handled by JS in page.

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

        return cast(Response, redirect(url_for("Algorithm")))

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


@app.route("/algorithm", methods=["GET", "POST"])
def Algorithm() -> str | Response:
    # Ensure config is set up first
    if "config" not in session.keys():
        return cast(Response, redirect(url_for("Config")))

    if request.method == "POST":
        # Get value from form
        algorithm = str(request.form.get("algorithm"))

        # Values restricted by form, no need to check for errors
        session["algorithm"] = algorithm

        return cast(Response, redirect(url_for("Animation")))

    # Algorithms that can be chosen from
    ALG_OPTIONS = {
        "ed": "Ed's Algorithm",
        "max": "Max's Algorithm",
        "scan": "SCAN Algorithm",
        "look": "LOOK Algorithm",
    }

    return render_template("algorithm.html", alg_options=ALG_OPTIONS)


# Return JSON data
@app.route("/data", methods=["GET"])
def Data() -> Response:
    if "algorithm" not in session.keys():
        return cast(Response, redirect(url_for("Algorithm")))

    # Retrieve the config from session storage
    config_copy = deepcopy(session["config"])

    if session["algorithm"] == "ed":
        output = ed_algorithm(session["config"])
        data = {
            "stops": [0] + output["stops"],
            "movements": output["movements"],
            "on": output["on"],
            "off": output["off"],
        }

    elif session["algorithm"] == "max":
        output = max_algorithm(
            session["config"]["requests"],
            session["config"]
        )
        data = {
            "stops": output["stops"],
            "on": [1] + output["pickups"],
            "off": [0] + output["dropoffs"],
        }

    elif session["algorithm"] == "scan":
        output = scan_algorithm(session["config"])
        data = {
            "stops": output["stops"],
            "movements": output["movements"],
            "on": output["on"],
            "off": output["off"],
        }

    elif session["algorithm"] == "look":
        output = look_algorithm(session["config"])
        data = {
            "stops": output["stops"],
            "movements": output["movements"],
            "on": output["on"],
            "off": output["off"],
        }

    data["config"] = config_copy

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
