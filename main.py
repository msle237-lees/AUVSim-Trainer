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

# Define the subprocesses to be executed
def process_imgs():
    """
    Process images to detect objects and post each detection to the database.
    """
    img = get_screenshot_as_opencv_images()
    results = get_results(img)
    for result in results:
        for box in result.boxes:
            # Access class id with `cls`
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            # Get the coordinates of the bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            # Save the object to the database
            data = {
                'object_name': class_name,
                'object_x': x1,
                'object_y': y1,
                'object_width': x2 - x1,
                'object_height': y2 - y1
            }
    return data

def process_movement(movements):
    # Get the movement data from the database
    if len(movements) == 0:
        return
    else:
        if movements['X'] >= 0.5:
            pyautogui.press('w')  
        elif movements['X'] <= -0.5:
            pyautogui.press('s')
        if movements['Y'] >= 0.5:
            pyautogui.press('a')
        elif movements['Y'] <= -0.5:
            pyautogui.press('d')
        if movements['Z'] >= 0.5:
            pyautogui.press('c')
        elif movements['Z'] <= -0.5:
            pyautogui.press('z')
        if movements['Rz'] >= 0.5:
            pyautogui.press('e')
        elif movements['Rz'] <= -0.5:
            pyautogui.press('q')
        if movements['Torp1']:
            pyautogui.press('r')
        if movements['Torp2']:
            pyautogui.press('f')
        if movements['Claw'] == 1:
            pyautogui.press('v')
        elif movements['Claw'] == -1:
            pyautogui.press('x')    

def main():
    start_sim()
    while True:
        results = process_imgs()
        object_area = results['object_width'] * results['object_height']
        print(object_area)
    
if __name__ == '__main__':
    main()