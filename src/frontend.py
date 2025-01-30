#!/usr/bin/env python

"""
frontend.py
Thomas Noakes, 2025

Handles all web-related requests to create a website GUI.
Utilises Flask as a web server, serving dynamically formatted HTML templates,
with CSS for styling and Javascript for scripting
"""

import sys
from flask import Flask, render_template, request

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
def config() -> str:
    if request.method == "POST":
        # TODO: implement POSTing config
        pass

    # A list of options and their formatting that is passed to the HTML
    # template. Format = {literalName: [type, prettyName, defaultValue]}
    CONFIG_OPTIONS: dict[str, list] = {
        "username": ["text", "Username", ""],
        "numLifts": ["number", "Number of lifts", 1],
        "numFloors": ["number", "Number of floors", 1],
    }

    return render_template("config.html", config_options=CONFIG_OPTIONS)


if __name__ == "__main__":
    # Check for debug mode in command-line arguments
    debug_mode = False
    if "--debug" in sys.argv:
        debug_mode = True

    # Start the Flask webserver
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=debug_mode)
