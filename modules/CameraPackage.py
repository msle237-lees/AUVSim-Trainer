from ultralytics import YOLO
import pyautogui
import json
import cv2
import os
from roboflow import Roboflow


class CameraPackage:
    def __init__(self, apiKey):
        rf = Roboflow(api_key=apiKey)
        project = rf.workspace("kennesaw-state-university").project("auvsim-prequals")
        version = project.version(2)
        self.dataset = version.download("yolov8")
    
    def take_picture(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        img = cv2.imread("screenshot.png")
        os.remove("screenshot.png")
        return img
    
    def gather_distance_measurement(self, img):
        pass
    
    def predict(self, img, classes=[], conf=0.5):
        if classes:
            results = self.model(img, classes=classes, conf=conf)
        else:
            results = self.model(img, conf=conf)
        return results
    
    def predict_and_detect(self, img, classes=[], conf=0.5):
        results = self.predict(img, classes, conf)
        for result in results.xyxy:
            x1, y1, x2, y2 = result[:4]
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return img, results
    

if __name__ == '__main__':
    with open("../config/api_key.json", "r") as f:
        api_key = json.load(f)["api_key"]
    camera_package = CameraPackage(apiKey=api_key)
    img = camera_package.take_picture()
    img, results = camera_package.predict_and_detect(img)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()