def split_yaml_line(line):
    try:
        left, right = line.split(": ")
        return left, right
    except:
        try:
            left, right = line.split(":")
            return left, right
        except:
            return None, None

def read_config(path):
    config = {}

    with open(path) as file:
        for line in file.readlines():
            left, right = split_yaml_line(line)

            if left is None or right is None:
                continue

            config[left] = int(right)
    return config