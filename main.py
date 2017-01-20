#!/usr/bin/env python3.5

import time
import threading

from modules.camera import Camera
from modules.door_listener import DoorListener
from modules.light import Light
from modules.siren_client import SirenClient
from modules.sms import Sms
from modules.pirs import Pirs
from modules.blue import Scanner

camera = Camera()
door_listener = DoorListener()
light = Light()
siren_client = SirenClient()
sms = Sms()
pirs = Pirs()
scanner = Scanner()

# check that everything is ok
sms.send_sms_async('alarm started')
light.turn_on(5)
camera.capture_and_upload_async()
scanner.scan()


def main():
    while True:
        if pirs.is_detecting_move() or door_listener.is_opened():
            light.turn_on()
        if scanner.is_armed:
            if pirs.is_detecting_move() or door_listener.is_opened():
                sms.send_sms_async('presence detected')
                siren_client.turn_on()
                camera.capture_and_upload_async()
            else:
                if door_listener.is_vibrating():
                    sms.send_sms_async('presence felt')
                    time.sleep(0.5)
        else:
            time.sleep(1)


# start bluetooth scanning in the background
new_bluetooth_thread = threading.Thread(target=scanner.watch)
new_bluetooth_thread.daemon = True  # stop if the program exits
new_bluetooth_thread.start()

# start listening door tag
new_doortag_thread = threading.Thread(target=door_listener.listen)
new_doortag_thread.daemon = True  # stop if the program exits
new_doortag_thread.start()

# start main loop
if __name__ == '__main__':
    main()
