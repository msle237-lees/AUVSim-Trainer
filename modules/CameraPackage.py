import cv2
from ultralytics import YOLO


class CameraPackage:
    def __init__(self):
        self.imgs_dir = input('Enter the full directory of the images folder: ')
        
        self.model = YOLO("yolov8n.pt")
    
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
    camera_package = CameraPackage()
    img = cv2.imread('test.jpg')
    img, results = camera_package.predict_and_detect(img)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()