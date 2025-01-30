#!/usr/bin/env python

"""
frontend.py
Thomas Noakes, 2025

Loads configuration for the lift system from a source
This can be from a given dictionary, loaded via a file path, or via a web
response
"""

import os
import json


def load_config_from_file(filepath: str) -> dict[str, str]:
    # Check if the file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Config file {filepath} cannot be found.")

    # Check if the file is a `.json` file
    extension = filepath.split(".")[-1]
    if extension != "json":
        raise NotImplementedError("Config file must be of type JSON.")

    # Attempt to open the file
    try:
        with open(filepath, "r", encoding="utf8") as file:
            text = file.read()
            file.close()
    # Generic error handling
    except Exception as e:
        raise Exception(f"An error occurred: \n\t{e}")

    # Attempt to convert the text to a dict using JSON decoder
    try:
        config = json.loads(text)
    # Catch errors on decoding the JSON
    except json.decoder.JSONDecodeError as e:
        raise Exception(f"JSON Decoding error: \n\t{e}")

    return config
