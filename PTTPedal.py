#!/usr/bin/env python
import os, sys, getopt
import logging
import evdev

class PTTPedal:
    
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

def usage():
    print('Usage:\n\tPedal.py -d <joystick event FIFO> [-v <verbosity>]')

def main(argv):
    logger = logging.getLogger()

    try:
      opts, args = getopt.getopt(argv,"d:v:h",["device=","verbosity=","help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(0)
        elif opt in ("-d", "--device"):
            devicePath = arg
        elif opt in ("-v", "--verbosity"):
            logger.setLevel(arg)
        else:
            logging.error("Unknown option(s)")
            usage()

    pedal = PTTPedal(devicePath)

    try:
        pedal.watchLoop()
    except KeyboardInterrupt:
        print()
        exit(130)
    except Exception as e:
        logging.error(e)
        exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])
