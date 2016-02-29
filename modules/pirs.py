import RPi.GPIO as io


class Pirs:

    def __init__(self):
        io.setmode(io.BCM)
        self.pir_pin = 4
        io.setup(self.pir_pin, io.IN)

    def is_detecting_move(self):
        return io.input(self.pir_pin)
