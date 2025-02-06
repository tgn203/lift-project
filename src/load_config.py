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

    # Check if the file is a `.json` or `.txt` file
    extension = filepath.split(".")[-1]
    if extension not in ["json", "txt"]:
        raise NotImplementedError("Config file must be of type JSON or TXT.")

    # Attempt to open the file
    try:
        with open(filepath, "r", encoding="utf8") as file:
            text = file.read()
            file.close()
    # Generic error handling
    except Exception as e:
        raise Exception(f"An error occurred: \n\t{e}")

    # Convert text config to JSON
    if extension == "txt":
        config = convert_config_txt_to_dict(text)

    # Attempt to convert the text to a dict using JSON decoder
    elif extension == "json":
        try:
            config = json.loads(text)
        # Catch errors on decoding the JSON
        except json.decoder.JSONDecodeError as e:
            raise Exception(f"JSON Decoding error: \n\t{e}")

    return config


def convert_config_txt_to_dict(text: str) -> dict[str, str]:
    # Note: assume the file exists, already checked in calling scope

    # Take text from already opened file, split into lines
    lines = text.split("\n")
    new_lines: list[str] = []
    for line in lines:
        # Remove empty lines
        if not line:
            continue

        # Remove 'comment lines', i.e. starts with `#`
        if line[0] == "#":
            continue

        # Add remaining lines to the new list
        new_lines.append(line)

    # Create empty config dict
    config: dict = {
        "num_floors": 0,
        "capacity": 0,
        "requests": {},
    }

    # First line contains num. floors and capacity
    [num_floors, capacity] = new_lines[0].split(", ")
    config["num_floors"] = int(num_floors)
    config["capacity"] = int(capacity)

    # Remaining lines are floors and their requests
    for line in new_lines[1::]:
        # Seperate line into segments and remove spaces
        split = [_.strip() for _ in line.split(":")]

        # Add empty floors to dict
        if not split[1]:
            config["requests"][int(split[0])] = []
            continue

        else:
            requests = [int(_) for _ in split[1].split(", ")]
            config["requests"][int(split[0])] = requests

    return config


def write_config_to_json(config: dict, filepath: str) -> None:
    # Convert the config dict to a JSON object
    json_config = json.dumps(config)

    # Attempt to open and write the file
    try:
        with open(filepath, "w", encoding="utf8") as file:
            file.write(str(json_config))
            file.close()
    # Generic error handling
    except Exception as e:
        raise Exception(f"An error occurred: \n\t{e}")
