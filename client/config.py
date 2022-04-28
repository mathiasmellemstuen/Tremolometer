"""!
Handling reading and writing data in the configuration yaml file (config.yaml).
"""
from typing import Any

import yaml


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
        self.path = path
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
        
        """
        self.config[key] = value
