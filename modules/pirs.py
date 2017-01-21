import RPi.GPIO as io
from rx.subjects import Subject

from modules import logger


class Pirs:
    def __init__(self):
        io.setmode(io.BCM)
        self.pir_pin = 4
        io.setup(self.pir_pin, io.IN)
        self.pirStream = Subject()
        io.add_event_detect(self.pir_pin, io.RISING, callback=self.hit_callback)

    def hit_callback(self, channel):
        logger.logger.debug('PIR DETECTION!')
        self.pirStream.on_next(True)

    def is_detecting_move(self):
        move_detected = io.input(self.pir_pin)
        if move_detected:
            logger.logger.debug('PIR DETECTION!')
        return move_detected
