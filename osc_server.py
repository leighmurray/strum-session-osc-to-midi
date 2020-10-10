import event
import argparse
import math
from pitch import Pitch
import re

from pythonosc import dispatcher
from pythonosc import osc_server

def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None

class OSCServer():

    stroke_deadzone = 8
    current_pitch = None
    previous_acceleration = 0

    def __init__(self, ip_address = "192.168.137.1", port = 8009):
        self.on_pitch_change = event.Event()
        self.on_acceleration = event.Event()
        self.on_button_press = event.Event()
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/accelerometer/linear/x", self.linear_accelerometer_handler)
        self.dispatcher.map("/oscControl/gridButton4", self.button_handler)
        self.dispatcher.map("/oscControl/gridButton8", self.button_handler)
        self.dispatcher.map("/oscControl/gridButton12", self.button_handler)
        self.dispatcher.map("/oscControl/gridButton16", self.button_handler)
        self.dispatcher.map("/orientation/pitch", self.pitch_handler)
        self.server = osc_server.ThreadingOSCUDPServer((ip_address, port), self.dispatcher)

    def pitch_handler(self, axis, value):
        pitch_value = Pitch(int(abs(value)/30)+1)
        if self.current_pitch != pitch_value:
            self.current_pitch = pitch_value
            self.on_pitch_change(self.current_pitch)

    def linear_accelerometer_handler(self, axis, acceleration):
        acceleration = int(acceleration)
        magnitude = abs(acceleration - self.previous_acceleration)
        if (self.previous_acceleration ^ acceleration) < 0 and magnitude >= self.stroke_deadzone:
            print("Acceleration change from {} to {}, magnitude {}.".format(self.previous_acceleration, acceleration, magnitude))
            self.on_acceleration(axis[-1], 1 if acceleration > 0 else -1)

        self.previous_acceleration = acceleration

    def button_handler(self, button, value):
        print("[{0}] ~ {1}".format(button, value))
        self.on_button_press(get_trailing_number(button))

    def serve(self):
        self.server.serve_forever()

