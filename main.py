#!/usr/bin/env python3

from modules.camera import Camera
from modules.door import Door
from modules.message import Message
from modules.blue import Bluetooth
from modules.pirs import Pirs
from modules.brightpi import BrightPI
import time
import threading
import parameters

camera = Camera()
door = Door()
message = Message()
bluetooth = Bluetooth()
pirs = Pirs()
bright_pi = BrightPI()

# check that everything is ok
message.send_message_async('alarm started')
bright_pi.turn_leds_on(mode='all')
camera.capture_and_upload_async()

# get a first scan
is_armed_wrapper = [not bluetooth.is_there_friendly_devices_nearby()]
if is_armed_wrapper[0]:
    message.send_message_async('system armed')
else:
    message.send_message_async('system disarmed')

# define loops


def recurrent_bluetooth_scan(is_armed_wrapper):
    while True:
        if is_armed_wrapper[0]:
            time.sleep(parameters.main_interval_between_scan_while_armed)
        else:
            time.sleep(parameters.main_interval_between_scan_while_disarmed)
        will_arm = not bluetooth.is_there_friendly_devices_nearby()
        if not is_armed_wrapper[0]:
            if will_arm:
                message.send_message_async('system armed')
                is_armed_wrapper[0] = True
        else:
            if not will_arm:
                message.send_message_async('system disarmed')
                is_armed_wrapper[0] = False


def main_loop():
    while True:
        if is_armed_wrapper[0] and (pirs.is_detecting_move() or door.is_opened()):
            message.send_message_async('presence detected')
            bright_pi.turn_leds_on(mode='ir_only')
            camera.capture_and_upload_async()
        else:
            time.sleep(1)


# start bluetooth scanning in the background
new_bluetooth_thread = threading.Thread(target=recurrent_bluetooth_scan, args=[is_armed_wrapper])
new_bluetooth_thread.daemon = True  # stop if the program exits
new_bluetooth_thread.start()

# start listening door tag
new_doortag_thread = threading.Thread(target=door.listen)
new_doortag_thread.daemon = True  # stop if the program exits
new_doortag_thread.start()

# start main loop
main_loop()
