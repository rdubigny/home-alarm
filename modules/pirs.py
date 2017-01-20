import RPi.GPIO as io
from modules import logger


class Pirs:
    def __init__(self):
        io.setmode(io.BCM)
        self.pir_pin = 4
        io.setup(self.pir_pin, io.IN)

    def is_detecting_move(self):
        move_detected = io.input(self.pir_pin)
        if move_detected:
            logger.logger.debug('PIR DETECTION!')
        return move_detected
