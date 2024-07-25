from ultralytics import YOLO
import pyautogui
import time
import cv2
import os

model = YOLO('models/prequals.pt')

def get_screenshot_as_opencv_images():
    # Code to capture screenshot and return it as OpenCV image
    # Returns a list of OpenCV images (3 cameras in the game)
    imgs = []
    for i in range(3):
        image = pyautogui.screenshot(region=(0, 0, 1920, 1080))
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        imgs.append(img)
        pyautogui.press('T')
    for i in range(3):
        pyautogui.press('G')
    return imgs

def get_results(imgs):
    # Code to get the results from the model
    # Returns a list of results (3 cameras in the game)
    results = []
    for img in imgs:
        result = model(img)
        results.append(result)
    return results

def process_movement(data : dict):
    '''
    data : dict
        data is a dictionary containing the results of the model
        X : float : X speed of the sub range -1 to 1
        Y : float : Y speed of the sub range -1 to 1
        Z : float : Z speed of the sub range -1 to 1
        Rx : float : Rx rotation of the sub range -1 to 1
        Torp1 : bool : Fire torpedo 1
        Torp2 : bool : Fire torpedo 2
        Claw : float : Claw movement range -1 to 1
    Output : Keyboard events
        'w' : Move forward
        'a' : Move left
        's' : Move backward
        'd' : Move right
        'q' : Rotate left
        'e' : Rotate right
        'z' : Move down
        'c' : Move up
        'x' : Claw open
        'v' : Claw close
        'r' : Torpedo 1
        'f' : Torpedo 2
    '''
    if data['X'] >= 0.5:
        pyautogui.press('w')
    elif data['X'] <= -0.5:
        pyautogui.press('s')
    if data['Y'] >= 0.5:
        pyautogui.press('d')
    elif data['Y'] <= -0.5:
        pyautogui.press('a')
    if data['Z'] >= 0.5:
        pyautogui.press('x')
    elif data['Z'] <= -0.5:
        pyautogui.press('v')
    if data['Rx'] >= 0.5:
        pyautogui.press('e')
    elif data['Rx'] <= -0.5:
        pyautogui.press('q')
    if data['Torp1']:
        pyautogui.press('r')
    if data['Torp2']:
        pyautogui.press('f')
    if data['Claw'] >= 0.5:
        pyautogui.press('c')
    if data['Claw'] <= -0.5:
        pyautogui.press('z')

def main():
    # Scan for the gate
    gate_found = False
    while not gate_found:
        imgs = get_screenshot_as_opencv_images()
        results = get_results(imgs)
        for result in results:
            for obj in result.pandas().xyxy[0].values:
                if obj[5] == 0:
                    gate_found = True
                    break
        process_movement({'X': 0, 'Y': 0, 'Z': 0, 'Rx': 0.5, 'Torp1': False, 'Torp2': False, 'Claw': 0})
        time.sleep(0.5)
        process_movement({'X': 0, 'Y': 0, 'Z': 0, 'Rx': 0, 'Torp1': False, 'Torp2': False, 'Claw': 0})
