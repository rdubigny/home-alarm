#!/usr/bin/env python3.5

import RPi.GPIO as io
import threading
import time

from modules import logger
from modules.message_client import MessageClient
from modules.counter import Counter
from modules.siren_listener import SirenListener

import config

message_client = MessageClient(config.control_center_ip, config.control_center_port)
counter = Counter()
siren_listener = SirenListener()

io.setmode(io.BCM)

door_pin = 23
vibration_pin = 25

io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)
io.setup(vibration_pin, io.IN, pull_up_down=io.PUD_UP)


def opened_callback(channel):
    message_client.send('door opened')


def hit_callback(channel):
    if counter.incr():
        message_client.send('door hit')


def main():
    while True:
        time.sleep(1)

io.add_event_detect(door_pin, io.RISING, callback=opened_callback, bouncetime=2000)
io.add_event_detect(vibration_pin, io.RISING, callback=hit_callback, bouncetime=500)

# start listening for siren call
new_siren_thread = threading.Thread(target=siren_listener.listen)
new_siren_thread.daemon = True  # stop if the program exits
new_siren_thread.start()

logger.logger.info('TAG STARTED!')

# start main loop
if __name__ == '__main__':
    main()
