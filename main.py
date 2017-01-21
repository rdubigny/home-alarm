#!/usr/bin/env python3.5

from rx import Observable
import time
import threading

from modules.camera import Camera
from modules.door_listener import DoorListener
from modules.light import LightOnObserver
from modules.light import LightOffObserver
from modules.siren_client import SirenClient
from modules.sms import Sms
from modules.pirs import Pirs
from modules.blue import Scanner

import parameters

camera = Camera()
door_listener = DoorListener()
siren_client = SirenClient()
sms = Sms()
pirs = Pirs()
scanner = Scanner()

# check that everything is ok
sms.send_sms_async('alarm started')
Observable.just(True).subscribe(LightOnObserver())
Observable.timer(1000).subscribe(LightOffObserver())
camera.capture_and_upload_async()
scanner.scan()


def main():
    # start bluetooth scanning in the background
    new_bluetooth_thread = threading.Thread(target=scanner.watch)
    new_bluetooth_thread.daemon = True  # stop if the program exits
    new_bluetooth_thread.start()

    # start listening door tag
    new_doortag_thread = threading.Thread(target=door_listener.listen)
    new_doortag_thread.daemon = True  # stop if the program exits
    new_doortag_thread.start()

    # light on if pir detection or door opened
    door_listener.openDoorStream.merge(pirs.pirStream)\
        .subscribe(LightOnObserver())

    # light of after x second with no event
    door_listener.openDoorStream.merge(pirs.pirStream).debounce(parameters.lightup_duration*1000)\
        .subscribe(LightOffObserver())

    while True:
        if scanner.is_armed:
            if pirs.is_detecting_move() or door_listener.is_opened():
                sms.send_sms_async('presence detected')
                # TODO : maybe the siren should be triggered when pirs.is_detecting_move() AND door_listener.is_opened()
                siren_client.turn_on()
                camera.capture_and_upload_async()
            else:
                if door_listener.is_vibrating():
                    sms.send_sms_async('presence felt')
                    time.sleep(0.5)
        else:
            time.sleep(1)

# start main loop
if __name__ == '__main__':
    main()
