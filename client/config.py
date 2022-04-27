"""!
Handle config data
"""
import yaml


class Config:
    def __init__(self, path):
        self.config = dict()
        self.path = path
        self.read()

    def read(self) -> None:
        with open(self.path) as file:
            self.config = yaml.safe_load(file)

    def write(self, data) -> None:
        try:
            file = open(self.path, "w+")
            yaml.dump(data, file, allow_unicode=True, default_flow_style=False)
        except FileNotFoundError as err:
            print("Could not write to file:", err)

        self.read()

    def __getitem__(self, item):
        return self.config[item]

    def __setitem__(self, key, value):
        self.config[key] = value
