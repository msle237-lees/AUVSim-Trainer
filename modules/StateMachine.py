from statemachine import StateMachine, State
from statemachine.contrib.diagram import DotGraphMachine

import json
import logging
import requests


class SM(StateMachine):
    # Define states for Prequals
    idle = State('Idle', initial=True)
    scan = State('Scan')
    move = State('Move')
    identify = State('Identify')
    end = State('End')
    
    # Define transitions for Prequals
    idle_to_scan = idle.to(scan)
    scan_to_move = scan.to(move)
    move_to_identify = move.to(identify)
    identify_to_move = identify.to(move)
    move_to_end = move.to(end)
    
    # Define functions for Prequals
    def on_enter_idle(self):
        logging.info('Entered Idle')
        
    def on_enter_scan(self):
        logging.info('Entered Scan')
        
    def on_enter_move(self):
        logging.info('Entered Move')
        
    def on_enter_identify(self):
        logging.info('Entered Identify')
        
    def on_enter_end(self):
        logging.info('Entered End')
        

