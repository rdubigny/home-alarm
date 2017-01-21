import RPi.GPIO as io
import signal
import socket
import sys
import threading

from modules import logger
from modules.message_server import MessageServer

import config
import parameters


class SirenListener:
    def __init__(self):
        self.timer = None
        self.siren_message_server = MessageServer(config.siren_command_port)
        self.siren_pin = 14
        io.setmode(io.BCM)
        io.setup(self.siren_pin, io.OUT)
        io.output(self.siren_pin, io.HIGH)
        logger.logger.info('SIREN OFF!')
        self.siren_alert_duration = parameters.siren_alert_duration

    def turn_on(self, duration=parameters.siren_alert_duration):
        if self.timer is None:
            # if no timer was previously set then turn on the light
            io.output(self.siren_pin, io.LOW)
            logger.logger.info('SIREN ON!')
        else:
            # reset timer
            self.timer.cancel()
            self.timer = None

        # auto shut down the light after <duration> seconds
        self.timer = threading.Timer(duration, self.turn_off)
        self.timer.start()

    def turn_off(self):
        io.output(self.siren_pin, io.HIGH)
        logger.logger.info('SIREN OFF!')
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def on_message(self, data):
        if data == 'siren on':
            self.turn_on()

    def listen(self):
        self.siren_message_server.listen(self.on_message)

    def cleanup(self, *args):
        self.turn_off()
        sys.exit(0)
