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

        if len(split) != 2:
            raise Exception(
                'Please make sure each floor call is in the format "floor: calls"'
            )

        # Add empty floors to dict
        if not split[1]:
            config["requests"][int(split[0])] = []
            continue

        else:
            try:
                requests = [int(_) for _ in split[1].split(", ")]
            except ValueError:
                raise Exception(
                    "Please make sure each call is an integer and seperated by commas"
                )
            config["requests"][int(split[0])] = requests

    return config


def write_config_to_file(config: dict, filepath: str) -> None:
    # Check if the file is a `.json` or `.txt` file
    extension = filepath.split(".")[-1]
    if extension not in ["json", "txt"]:
        raise NotImplementedError("Config file must be of type JSON or TXT.")

    if extension == "json":
        # Convert the config dict to a JSON object
        config_text = str(json.dumps(config))

    else:
        # Convert to text form
        lines = ["# Number of Floors, Capacity"]

        # Add line for floor number and capacity config
        lines.append(f"{config["num_floors"]}, {config["capacity"]}")
        lines.append("")

        # Add line for each floor config
        lines.append("# Floor Requests")
        for floor, requests in config["requests"].items():
            # Convert floor numbers to strs
            requests = [str(_) for _ in requests]
            lines.append(f"{floor}: {", ".join(requests)}".strip())

        config_text = "\n".join(lines)

    # Attempt to open and write the file
    try:
        with open(filepath, "w", encoding="utf8") as file:
            file.write(config_text)
            file.close()
    # Generic error handling
    except Exception as e:
        raise Exception(f"An error occurred: \n\t{e}")


def check_config(config: dict) -> None:
    # creates a list of all the floors their should be
    allfloors: list[int] = [i for i in range(1, config["num_floors"] + 1)]
    # checks if all floors are set, even if empty
    if not all(floor in list(config["requests"].keys()) for floor in allfloors):
        raise Exception(
            f"Not all floors are set, please make sure you have all floors 1-{config["num_floors"]} set"
        )
    # checks if all floors are within the bounds as set by the number of floors
    if not all(floor in allfloors for floor in list(config["requests"].keys())):
        raise Exception(
            f"Not all floors are valid, please make sure you have all floors between 1-{config["num_floors"]}"
        )
    # checks if all floors are in a list
    if not all(type(floor) == list for floor in list(config["requests"].values())):
        raise Exception(f"Not all floor calls are stored in a list")
    # checks if all floors are integers
    if not all(
        all(type(value) == int for value in floor)
        for floor in config["requests"].values()
    ):
        raise Exception(
            f"Not all calls are integers, make sure each value is an integer"
        )
    # checks if all calls are for a valid floor
    if not all(
        all(value in allfloors for value in floor)
        for floor in config["requests"].values()
    ):
        raise Exception(f"Not all calls are between 1-{config["num_floors"]}")


# config: dict = load_config_from_file("test.txt")
# check_config(config)
# print(config)
