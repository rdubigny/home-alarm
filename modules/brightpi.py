from smbus import SMBus
import sys
import signal
import threading
from modules import logger
import parameters


class BrightPI:
    BrightPiAddress = 0x70
    AddressControl = 0x00
    AddressAllLed = 0x09
    maxBrightness = 0x32

    def __init__(self):
        self.bus = SMBus(1)
        self.timer = None
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

    def turn_leds_on(self, mode='all'):
        if self.timer is None:
            # if no timer was previously set then turn on the light
            mask = {
                'all': 0xff,
                'ir_only': 0xa5,
                'white_only': 0x5a
            }.get(mode, 0xff)
            result = self.bus.read_byte_data(self.BrightPiAddress, self.AddressControl) | mask
            self.bus.write_byte_data(self.BrightPiAddress, self.AddressControl, result)
            self.bus.write_byte_data(self.BrightPiAddress, self.AddressAllLed, 15)
            logger.logger.info('LIGHTS ON!')
        else:
            # reset timer
            self.timer.cancel()
            self.timer = None

        # auto shut down the light after 5 seconds
        self.timer = threading.Timer(parameters.brightpi_turnoff_timer, self.reset)
        self.timer.start()

    def reset(self):
        self.bus.write_byte_data(self.BrightPiAddress, self.AddressControl, 0x00)
        if self.timer is not None:
            self.timer = None
            logger.logger.info('LIGHTS OFF!')

    def cleanup(self, *args):
        self.reset()
        sys.exit(0)
