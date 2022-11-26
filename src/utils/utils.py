import json
import sys


def get_settings():
    with open(sys.argv[1], "r") as openfile:
        return json.load(openfile)

def get_settings_notebook(path):
    with open(path, "r") as openfile:
        return json.loads(json.dumps(json.load(openfile)).replace('src/files/', 'files/'))

def pretty_print(d):
    print(f'=======\n{json.dumps(d, sort_keys=True, indent=4)}\n======')