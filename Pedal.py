#!/usr/bin/env python
import os
import logging
import evdev

class Pedal:
    
    def __init__(self, path):
        self._device = evdev.InputDevice(path)
        logging.info(self._device)

    def watchLoop(self):
        for message in self._device.read_loop():
            logging.debug(message)
            try:
                if message.type == evdev.ecodes.EV_KEY:
                    event = evdev.categorize(message)
                    logging.info(event)

                    code = event.keycode
                    logging.debug(code)
                    state = event.keystate
                    logging.debug(state)

                    self._handleEvent(code, state)
            except AttributeError as e:
                raise(e)

    def _handleEvent(self, code, state):
        if 'BTN_A' in code:
            if state == 0: # up
                os.system("pactl set-source-mute @DEFAULT_SOURCE@ 1")
            if state == 1: # down
                os.system("pactl set-source-mute @DEFAULT_SOURCE@ 0")

logger = logging.getLogger()
logger.setLevel("WARNING")

pedal = Pedal("/dev/input/by-id/usb-1a86_e026-event-joystick")

try:
    pedal.watchLoop()
except KeyboardInterrupt:
    exit(0)
