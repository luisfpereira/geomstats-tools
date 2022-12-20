from pathlib import Path
import json


def get_global_config_file():
    path = Path.home() / '.geomstats-tools' / 'config.json'
    if path.exists():
        return str(path)


CONFIG_FILE_PATH = get_global_config_file()


def load_from_config(*args):
    # TODO: create nice error message
    with open(CONFIG_FILE_PATH, 'r') as file:
        config = json.load(file)

    vals = [config[arg] for arg in args]
    if len(vals) == 1:
        return vals[0]

    return vals
