import json
import os

d = {
    'lvl1': {
        'lvl': 1,
        'choices': 3,
        'characters': ['rock', 'paper', 'scissors'],
        'legends': {'rock': 'r', 'paper': 'p', 'scissors': 's'},
        'logic': ['r/s', 'p/r', 's/p']
    },
    'lvl2': {
        'lvl': 2,
        'choices': 5,
        'characters': ['rock', 'paper', 'scissors', 'lizard', 'spock'],
        'legends': {'rock': 'Ro', 'paper': 'Pa', 'scissors': 'Sc', 'lizard': 'Li', 'spock': 'Sp'},
        'logic': ['Ro/Pa', 'Ro/Li',
                  'Pa/Ro', 'Pa/Sp',
                  'Sc/Pa', 'Sc/Li',
                  'Sp/Ro', 'Sp/Sc',
                  'Li/Pa', 'Li/Sp']
    },
    'lvl3': {}
}


file_path = os.path.join('RPS/Assets', 'logic.json')


def file_to_dict(file=file_path):
    with open(file, "r") as readfile:
        return json.load(readfile)


if __name__ == '__main__':
    file_path = os.path.join('Assets', 'logic.json')

with open(file_path, 'w') as f:
    json.dump(d, f)
