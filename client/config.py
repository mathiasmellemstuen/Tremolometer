import yaml

def read_config(path):

    with open(path) as file:
        return yaml.safe_load(file)

    return None

def write_config(data, path):
    try:
        file = open(path, "w+")
        yaml.dump(data, file, allow_unicode=True, default_flow_style=False)
    except:
        print("Could not write to file")