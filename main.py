# Import the modules from the modules folder
from modules import CameraPackage
from modules import MovementPackage
from modules import StateMachine

import numpy as np
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class SubprocessHandler:
    def __init__(self, command):
        self.command = command
        self.process = None

    def start(self):
        if self.process is None:
            self.process = subprocess.Popen(self.command)
            print(f"Started subprocess with PID: {self.process.pid}")
        else:
            print("Process is already running.")

    def stop(self):
        if self.process is not None:
            self.process.terminate()  # Graceful termination
            self.process.wait()  # Wait for the process to terminate
            print(f"Terminated subprocess with PID: {self.process.pid}")
            self.process = None
        else:
            print("Process is not running.")

class Inputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    X = db.Column(db.Integer)
    Y = db.Column(db.Integer)
    Z = db.Column(db.Integer)
    Rz = db.Column(db.Integer)
    Torp1 = db.Column(db.Integer)
    Torp2 = db.Column(db.Integer)
    claw = db.Column(db.Integer)

    def __repr__(self):
        return f'<Inputs {self.id}>'

class Outputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(1))
    mouse = db.Column(db.String(2))
    click = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Outputs {self.id}>'
    
class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20))

    def __repr__(self):
        return f'<State {self.id}>'

class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    w = db.Column(db.Integer)
    h = db.Column(db.Integer)

    def __repr__(self):
        return f'<Objects {self.id}>'

@app.route('/inputs', methods=['POST'])
def inputs():
    data = request.get_json()
    inputs = Inputs(X=data['X'], Y=data['Y'], Z=data['Z'], Rz=data['Rz'], Torp1=data['Torp1'], Torp2=data['Torp2'], claw=data['claw'])
    db.session.add(inputs)
    db.session.commit()
    return 'OK'

@app.route('/inputs', methods=['GET'])
def get_inputs():
    inputs = Inputs.query.order_by(Inputs.id.desc()).first()
    return {'X': inputs.X, 'Y': inputs.Y, 'Z': inputs.Z, 'Rz': inputs.Rz, 'Torp1': inputs.Torp1, 'Torp2': inputs.Torp2, 'claw': inputs.claw}

@app.route('/outputs', methods=['POST'])
def outputs():
    data = request.get_json()
    outputs = Outputs(key=data['key'], mouse=data['mouse'], click=data['click'])
    db.session.add(outputs)
    db.session.commit()
    return 'OK'

@app.route('/outputs', methods=['GET'])
def get_outputs():
    outputs = Outputs.query.order_by(Outputs.id.desc()).first()
    return {'key': outputs.key, 'mouse': outputs.mouse, 'click': outputs.click}

@app.route('/state', methods=['POST'])
def state():
    data = request.get_json()
    state = State(state=data['state'])
    db.session.add(state)
    db.session.commit()
    return 'OK'

@app.route('/state', methods=['GET'])
def get_state():
    state = State.query.order_by(State.id.desc()).first()
    return state.state

@app.route('/objects', methods=['POST'])
def objects():
    data = request.get_json()
    objects = Objects(name=data['name'], x=data['x'], y=data['y'], w=data['w'], h=data['h'])
    db.session.add(objects)
    db.session.commit()
    return 'OK'

@app.route('/objects', methods=['GET'])
def get_objects():
    objects = Objects.query.all()
    return [{'name': obj.name, 'x': obj.x, 'y': obj.y, 'w': obj.w, 'h': obj.h} for obj in objects]

commands = {
    'M': ['python3', 'modules/MovementPackage.py'],
    'C': ['python3', 'modules/CameraPackage.py'],
    'S': ['python3', 'modules/StateMachine.py']
}

subprocesses = {f'{key}': SubprocessHandler(value) for key, value in commands.items()}

@app.route('/run', methods=['POST'])
def run():
    for key, value in subprocesses.items():
        value.start()
    return 'OK'

@app.route('/stop', methods=['POST'])
def stop():
    for key, value in subprocesses.items():
        value.stop()
    return 'OK'

@app.route('/')
def index():
    return render_template('index.html')

def create_tables():
    with app.app_context():
        db.create_all()
    
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)