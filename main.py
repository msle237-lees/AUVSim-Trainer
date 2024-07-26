import time
import pyautogui
import cv2
import numpy as np
from ultralytics import YOLO
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import multiprocessing

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
    while True:
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
                # make a post request to the server
                requests.post('http://localhost:5000/object', json=data)
        
        time.sleep(0.5)

def process_decisions():
    output = {
        'X': 0,
        'Y': 0,
        'Z': 0,
        'Rz': 0,
        'Torp1': False,
        'Torp2': False,
        'Claw': 0
    }
    
    while True:
        # Get the latest object from the database
        objects = Object.query.order_by(Object.id.desc()).limit(1).all()
        
        if len(objects) == 0:
            return
        else:
            pass

def process_movement():
    while True:
        # Get the movement data from the database
        movements = requests.get('http://localhost:5000/movement').json()
        if len(movements) == 0:
            continue
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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Movement(db.Model):
    """
    Movement class to store the movement data.
    """
    id = db.Column(db.Integer, primary_key=True)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Z = db.Column(db.Float, nullable=False)
    Rz = db.Column(db.Float, nullable=False)
    Torp1 = db.Column(db.Boolean, nullable=False)
    Torp2 = db.Column(db.Boolean, nullable=False)
    Claw = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Movement(X={self.X}, Y={self.Y}, Z={self.Z}, Rz={self.Rz}, Torp1={self.Torp1}, Torp2={self.Torp2}, Claw={self.Claw})"
    
class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(100), nullable=False)
    object_x = db.Column(db.Float, nullable=False)
    object_y = db.Column(db.Float, nullable=False)
    object_width = db.Column(db.Float, nullable=False)
    object_height = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Object(object_name={self.object_name}, object_x={self.object_x}, object_y={self.object_y}, object_width={self.object_width}, object_height={self.object_height})"

@app.route('/object', methods=['POST'])
def add_object():
    """
    Add an object to the database.
    """
    data = request.json
    object = Object(object_name=data['object_name'], object_x=data['object_x'], object_y=data['object_y'], object_width=data['object_width'], object_height=data['object_height'])
    db.session.add(object)
    db.session.commit()
    return jsonify({'message': 'Object added successfully!'})

@app.route('/object', methods=['GET'])
def get_objects():
    """
    Get all objects from the database.
    """
    objects = Object.query.all()
    output = []
    for object in objects:
        object_data = {
            'object_name': object.object_name,
            'object_x': object.object_x,
            'object_y': object.object_y,
            'object_width': object.object_width,
            'object_height': object.object_height
        }
        output.append(object_data)
    return jsonify({'objects': output})

@app.route('/movement', methods=['POST'])
def add_movement():
    """
    Add a movement to the database.
    """
    data = request.json
    movement = Movement(X=data['X'], Y=data['Y'], Z=data['Z'], Rz=data['Rz'], Torp1=data['Torp1'], Torp2=data['Torp2'], Claw=data['Claw'])
    db.session.add(movement)
    db.session.commit()
    return jsonify({'message': 'Movement added successfully!'})

@app.route('/movement', methods=['GET'])
def get_movements():
    """
    Get all movements from the database.
    """
    movements = Movement.query.all()
    output = []
    for movement in movements:
        movement_data = {
            'X': movement.X,
            'Y': movement.Y,
            'Z': movement.Z,
            'Rz': movement.Rz,
            'Torp1': movement.Torp1,
            'Torp2': movement.Torp2,
            'Claw': movement.Claw
        }
        output.append(movement_data)
    return jsonify({'movements': output})

def start_server():
    """
    Start the server to receive the movement data.
    """
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000, host='0.0.0.0')

def main():
    """
    Main function to start the simulation and scan for the gate.
    """
    # Start the server subprocess
    server_process = multiprocessing.Process(target=start_server)
    server_process.start()
    
    # Delay to switch to game
    time.sleep(5)

    # Start the simulation
    start_sim()
    
    # Start the object detection subprocess
    imgs_process = multiprocessing.Process(target=process_imgs)
    imgs_process.start()
    
    # Start the movement subprocess
    movement_process = multiprocessing.Process(target=process_movement)
    movement_process.start()
    
    # Start the decision subprocess
    decision_process = multiprocessing.Process(target=process_decisions)
    decision_process.start()
    
    # Wait for the subprocesses to finish
    imgs_process.join()
    movement_process.join()
    decision_process.join()

if __name__ == "__main__":
    main()