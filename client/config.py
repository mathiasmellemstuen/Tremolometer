"""!
Handling reading and writing data in the configuration yaml file (config.yaml).
"""
from typing import Any

import yaml
import sys
import os


def path_to_resource_path(relative_path: str) -> str:
    """!
    Fixing relative paths when building this code to an executable with pyinstaller.

    @param relative_path The relative path to apply fix.

    @return Returns the new relative path that works both for a normal python call of the script and pyinstaller
    executable.
    """

    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Config:
    """!
    Handle config file as a class for more consistent reference in parameters.
    """

    def __init__(self, path: str) -> None:
        """!
        Constructor.

        @param self Pointer to self.
        @param path Config file path.
        """
        self.config = dict()
        self.path = path_to_resource_path(path)
        self.read()

    def read(self) -> None:
        """!
        Read config file and store the contents to the local config variable.

        @param self Pointer to self.
        """
        with open(self.path) as file:
            self.config = yaml.safe_load(file)

    def write(self, data: dict) -> None:
        """!
        Write contents of data dict to file.

        @param self Pointer to self.
        @param data Dict with data to store.
        """
        try:
            file = open(self.path, "w+")
            yaml.dump(data, file, allow_unicode=True, default_flow_style=False)
        except FileNotFoundError as err:
            print("Could not write to file:", err)

        self.read()

    def __getitem__(self, item: str) -> str:
        """!
        Square bracket overloading to access elements of config easy.

        @param self Pointer to self.
        @param item Key to retrieve.
        """
        return self.config[item]

    def __setitem__(self, key: str, value: Any) -> None:
        """!
        Square bracket overloading to set an element in config variable.

        @param self Pointer to self.
        @param key Element to change.
        @param value Element value.
        """
        self.config[key] = value
