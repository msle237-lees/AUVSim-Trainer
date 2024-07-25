import time
import pyautogui
import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('models/prequals.pt')

def start_sim():
    """
    Start the simulation by locating and clicking the start button.
    """
    while True:
        try:
            location = pyautogui.locateOnScreen('imgs/Start_Button.PNG')
            pyautogui.click(location)
            pyautogui.press('t')
            break
        except Exception as e:
            pyautogui.press('space')

def get_screenshot_as_opencv_images():
    """
    Capture a screenshot and return it as an OpenCV image.

    Returns:
        numpy.ndarray: The captured image in OpenCV format.
    """
    image = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return img

def get_results(img):
    """
    Get the results from the model.

    Args:
        img (numpy.ndarray): The image to analyze.

    Returns:
        list: The results from the model for the image.
    """
    result = model(img)
    return result

def process_movement(data):
    """
    Process movement based on the input data.

    Args:
        data (dict): Dictionary containing movement commands.
    """
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
    elif data['Claw'] <= -0.5:
        pyautogui.press('z')

def main():
    """
    Main function to start the simulation and scan for the gate.
    """
    # Delay to switch to game
    time.sleep(5)

    # Start the simulation
    start_sim()

    # Scan for the gate
    gate_found = False
    width = 0.0
    height = 0.0
    while not gate_found:
        img = get_screenshot_as_opencv_images()
        results = get_results(img)
        for result in results:
            for box in result.boxes:
                # Access class id with `cls`
                class_id = int(box.cls[0])
                if class_id == 2:  # Assuming class index 2 corresponds to 'Gate'
                    # Get the coordinates of the bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    width = x2 - x1
                    height = y2 - y1
                    print(f"Gate detected! Width: {width}, Height: {height}")
                    gate_found = True
                    break
            if gate_found:
                break
        if not gate_found:
            # Process movement or other actions here if gate is not found
            process_movement({'X': 0, 'Y': 0, 'Z': 0, 'Rx': 0.5, 'Torp1': False, 'Torp2': False, 'Claw': 0})
            time.sleep(0.5)
            process_movement({'X': 0, 'Y': 0, 'Z': 0, 'Rx': 0, 'Torp1': False, 'Torp2': False, 'Claw': 0})

    gate_passed = False
    while not gate_passed:
        img = get_screenshot_as_opencv_images()
        results = get_results(img)
        for result in results:
            for box in result.boxes:
                # Access class id with `cls`
                class_id = int(box.cls[0])
                if class_id == 2:  # Assuming class index 2 corresponds to 'Gate'
                    # Get the coordinates of the bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    width = x2 - x1
                    height = y2 - y1
                    print(f"Gate detected! Width: {width}, Height: {height}")
                    gate_found = True
                    break
            if gate_passed:
                break
        if gate_found:
            # Process movement or other actions here if gate is not found
            process_movement({'X': 1.0, 'Y': 0, 'Z': 1.0, 'Rx': 0, 'Torp1': False, 'Torp2': False, 'Claw': 0})
            time.sleep(0.5)
            process_movement({'X': 0, 'Y': 0, 'Z': 0, 'Rx': 0, 'Torp1': False, 'Torp2': False, 'Claw': 0})
            gate_found = False

if __name__ == "__main__":
    main()