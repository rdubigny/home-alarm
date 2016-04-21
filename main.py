#!/usr/bin/env python3.5

import time
import threading
from modules.camera import Camera
from modules.door import Door
from modules.message import Message
from modules.blue import Scanner
from modules.pirs import Pirs
from modules.brightpi import BrightPI
import parameters

bright_pi = BrightPI()
camera = Camera()
door = Door()
message = Message()
pirs = Pirs()
scanner = Scanner()

# check that everything is ok
message.send_message_async('alarm started')
bright_pi.turn_leds_on(mode='all')
camera.capture_and_upload_async()
scanner.scan()


def main_loop():
    while True:
        if scanner.is_armed:
            if pirs.is_detecting_move() or door.is_opened():
                message.send_message_async('presence detected')
                bright_pi.turn_leds_on(mode='ir_only')
                camera.capture_and_upload_async()
            else:
                if door.is_vibrating():
                    # TODO this will be triggered every loop during one second, this is far to much
                    message.send_message_async('presence felt')
        else:
            time.sleep(1)


# start bluetooth scanning in the background
new_bluetooth_thread = threading.Thread(target=scanner.watch)
new_bluetooth_thread.daemon = True  # stop if the program exits
new_bluetooth_thread.start()

# start listening door tag
new_doortag_thread = threading.Thread(target=door.listen)
new_doortag_thread.daemon = True  # stop if the program exits
new_doortag_thread.start()

# start main loop
main_loop()
