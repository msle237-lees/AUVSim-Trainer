import pyautogui
import json
import time


class MovementPackage:
    def __init__(self):
        self.input_data = None

        with open('config.json') as f:
            self.config = json.load(f)
    
    def set_input_data(self, input_data):
        self.input_data = input_data

    def move_mouse(self, x, y):
        pyautogui.moveTo(x, y)

    def click(self):
        pyautogui.click()

    def press_key(self, key):
        pyautogui.press(key)

    def convert(self, data):
        if data['X'] == 0.5:
            self.input_data.append({'key': 'w'})
        if data['X'] == -0.5:
            self.input_data.append({'key': 's'})
        if data['Y'] == 0.5:
            self.input_data.append({'key': 'c'})
        if data['Y'] == -0.5:
            self.input_data.append({'key': 'z'})
        if data['Z'] == 1:
            self.input_data.append({'key': 'd'})
        if data['Z'] == -1:
            self.input_data.append({'key': 'a'})
        if data['Rz'] == 1:
            self.input_data.append({'key': 'q'})
        if data['Rz'] == -1:
            self.input_data.append({'key': 'e'})
        if data['Torp1']:
            self.input_data.append({'key': 'r'})
        if data['Torp2']:
            self.input_data.append({'key': 'f'})
        if data['claw'] == 1:
            self.input_data.append({'key': 'x'})
        if data['claw'] == -1:
            self.input_data.append({'key': 'v'})

    def execute(self):
        for data in self.input_data:
            if 'key' in data:
                self.press_key(data['key'])
            if 'mouse' in data:
                self.move_mouse(data['mouse']['x'], data['mouse']['y'])
            if 'click' in data:
                self.click()
            time.sleep(0.01)