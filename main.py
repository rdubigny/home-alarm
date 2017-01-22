#!/usr/bin/env python3.5

from rx import Observable
import time
import threading

from modules.camera import Camera
from modules.door_listener import DoorListener
from modules.light import LightOnObserver
from modules.light import LightOffObserver
from modules.siren_client import SirenClient
from modules.siren_client import SirenClientObserver
from modules.sms import Sms
from modules.sms import SmsObserver
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
Observable.timer(2000).subscribe(LightOffObserver())
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

    # send sms when unknown presence is detected
    pirs.pirStream.pausable(scanner.blueStream)\
        .throttle_first(parameters.sms_min_interval_between_sms*1000).subscribe(SmsObserver('presence detected'))

    # send sms on open door
    door_listener.openDoorStream.pausable(scanner.blueStream)\
        .throttle_first(parameters.sms_min_interval_between_sms*1000).subscribe(SmsObserver('door open'))

    # send sms on door vibe
    door_listener.vibeDoorStream.pausable(scanner.blueStream)\
        .throttle_first(parameters.sms_min_interval_between_sms*1000).subscribe(SmsObserver('door vibe'))

    # turn siren when unknown presence is detected with both open door and pir
    # TODO: put timer duration in a variable
    door_listener.openDoorStream\
        .join(pirs.pirStream,
              lambda x: Observable.timer(15*1000),
              lambda x: Observable.timer(15*1000),
              lambda x, y: True)\
        .pausable(scanner.blueStream).subscribe(SirenClientObserver())

    # take photo if pir detection or door opened or door vibe
    # TODO: complete this
    # door_listener.openDoorStream.merge(door_listener.vibeDoorStream).merge(pirs.pirStream).repeat(10)\
    #     .pausable(scanner.blueStream)\
    #     .subscribe(print)

    # if the subscriber doesn't get the first blueStream event they will be paused by default
    # TODO:  use a replay here instead of the following workaround
    scanner.scan()

    while True:
        if scanner.is_armed:
            if pirs.is_detecting_move() or door_listener.is_opened():
                camera.capture_and_upload_async()
        else:
            time.sleep(1)

# start main loop
if __name__ == '__main__':
    main()
