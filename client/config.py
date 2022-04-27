"""!
Handling reading and writing data in the configuration yaml file (config.yaml).
"""
from typing import Optional
from customTypes import Config

import yaml


def read_config(path: str) -> Optional[Config]:
    """!
    Read config file.

    @param path The path to the config file.

    @return The config file as an object
    """
    with open(path) as file:
        return yaml.safe_load(file)


def write_config(data: Config, path: str) -> None:
    """!
    Update config file.

    @param data The data to write.
    @param path Where to store the data.
    """
    try:
        file = open(path, "w+")
        yaml.dump(data, file, allow_unicode=True, default_flow_style=False)
    except FileNotFoundError as err:
        print("Could not write to file:", err)
