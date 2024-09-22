import json
import pyautogui
import os
import importlib
from RPS.constants import SCROLL

'''
Format->>
    {'vx': 1,
     'vy': -1,
     'gravity': 0.00,
     'lifetime_min': 5,
     'lifetime_max': 10,
     'limit': 60,
     'end_radius': 0,
     'spread': 0.001,
     'size_death_rate': 0.08,
     'alpha_death_rate': 0,
     'color_set': None,
     'optimization_factor': 1,
     'properties': None,
     'special_flags': None
     }
'''
data_loader = False
add = False
update = True
clear = False
delete = False
warning = True

try:
    m = importlib.import_module(f'{os.path.basename(os.path.dirname(os.path.realpath(__file__)))}.constants')
    preset_file_path = m.PRESET_FILE_PATH
    data_file_path = m.DATA_FILE_PATH
except (ImportError, AttributeError):
    preset_file_path = 'Assets/presets.json'
    data_file_path = 'Assets/particle_data.json'

FILE_NAME = preset_file_path
if __name__ == '__main__':
    FILE_NAME = 'presets.json'

if data_loader:
    FILE_NAME = data_file_path
    if __name__ == '__main__':
        FILE_NAME = 'particle_data.json'


def data_writer(data):
    new_data = []
    for p_type, positions in data.items():
        for position in positions:
            new_data.append({p_type: position})
    return new_data


PRESET_NAME = 'SMOKE'
INDEX_TO_DELETE = None

s = 64
d1 = 209
y1 = 85
y2 = 50
y3 = 75
DATA = data_writer({'FIRE': [[s, y1], [s + d1, y1]],
                    'SMOKE': [[s, y2], [s + d1, y2]],
                    'FIRE_SPARK': [[s, y3], [s + d1, y3]]})


def load_preset(file_path, preset_name='BASE'):
    with open(file_path, 'r') as file:
        try:
            return json.load(file)[preset_name]
        except (TypeError, KeyError):
            return {}


def add_preset(file_path, preset_name, data):
    with open(file_path, 'r') as read_file:
        try:
            previous_content = json.load(read_file)
        except json.decoder.JSONDecodeError:
            previous_content = {}
        with open(file_path, 'w') as write_file:
            json.dump(previous_content | {preset_name: data}, write_file, indent=4)


def clear_file(file_path):
    if pyautogui.confirm(text='Are you sure you want to clear your file?', title=f'Warning. FILE: {file_path}',
                         buttons=['Proceed', 'Cancel']) == 'Proceed' if warning else True:
        with open(file_path, 'w') as file:
            json.dump(None, file)


def delete_preset(file_path, preset_name):
    if pyautogui.confirm(text='Are you sure you want to delete your preset?', title=f'Warning. PRESET: {preset_name}',
                         buttons=['Proceed', 'Cancel']) == 'Proceed' if warning else True:
        with open(file_path, 'r') as read_file:
            try:
                previous_content = json.load(read_file)
            except json.decoder.JSONDecodeError:
                previous_content = {}
            with open(file_path, 'w') as write_file:
                if preset_name in previous_content:
                    del previous_content[preset_name]
                json.dump(previous_content, write_file, indent=4)


def add_data(file_path, data):
    with open(file_path, 'r') as read_file:
        try:
            previous_content = json.load(read_file)
        except json.decoder.JSONDecodeError:
            previous_content = {}
        with open(file_path, 'w') as write_file:
            new_data = {}
            index = len(previous_content)
            for element in data:
                index += 1
                new_data[index] = element
            json.dump(previous_content | new_data, write_file, indent=4)


def delete_data(file_path, index):
    if pyautogui.confirm(text="Are you sure you want to you delete your data?", title=f"Preset Name: {index}",
                         buttons=['Proceed', 'Cancel']) == 'Proceed' if warning else True:
        with open(file_path, 'r') as read_file:
            try:
                previous_content = json.load(read_file)
            except json.decoder.JSONDecodeError:
                previous_content = {}
            with open(file_path, 'w') as write_file:
                if index in previous_content:
                    del previous_content[index]
                json.dump(previous_content, write_file, indent=4)


def update_data(file_path, data):
    if pyautogui.confirm(text="Are you sure you want to you update your data?",
                         title=f"Warning: Your previous data would be deleted",
                         buttons=['Proceed', 'Cancel']) == 'Proceed' if warning else True:
        with open(file_path, 'w') as write_file:
            data = {index + 1: value for index, value in enumerate(data)}
            json.dump(data, write_file, indent=4)


def load_data(file_path):
    with open(file_path, 'r') as file:
        try:
            return json.load(file)
        except json.decoder.JSONDecodeError:
            return {}


if not data_loader:
    if add:
        if DATA is not None and PRESET_NAME is not None:
            add_preset(FILE_NAME, PRESET_NAME, DATA)
    if delete:
        delete_preset(FILE_NAME, PRESET_NAME)
    if clear:
        clear_file(FILE_NAME)
elif data_loader:
    if add:
        if DATA is not None:
            add_data(FILE_NAME, DATA)
    if update:
        if DATA is not None:
            update_data(FILE_NAME, DATA)
    if delete:
        if INDEX_TO_DELETE is not None:
            delete_data(FILE_NAME, INDEX_TO_DELETE)
    if clear:
        clear_file(FILE_NAME)
