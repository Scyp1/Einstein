import json
from random import choice

CONFIG = json.load(open('./packages/einstein/package_config.json'))
ANSWERS = json.load(open(CONFIG['python_datas']['answers']))['einstein']

def hello(entities):
    return choice(ANSWERS['hello'])

def feelings(entities):
    return choice(ANSWERS['feelings'])

def goodbye(entities):
    return choice(ANSWERS['goodbye'])