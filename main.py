# Import the modules from the modules folder
from modules import CameraPackage
from modules import MovementPacakge
from modules import StateMachine

import cv2
import logging
import numpy as np


def main():
    SM = StateMachine.SM()
    CP = CameraPackage.CameraPackage()
    MP = MovementPacakge.MovementPackage()
    
    inputs = {
        'X': 0,
        'Y': 0,
        'Z': 0,
        'Rz': 0,
        'Torp1': 0,
        'Torp2': 0,
        'claw': 0
    }
    
    while True:
        pass
