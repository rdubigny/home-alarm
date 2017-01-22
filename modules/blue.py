import bluetooth
from rx.subjects import Subject
import time

from modules import logger
from modules.sms import Sms

import config
import parameters


class Bluetooth:
    def __init__(self):
        pass

    @staticmethod
    def is_there_friendly_devices_nearby():
        logger.logger.debug('BLUETOOTH SCANNING...')
        result = None
        for name, address in config.remote_bluetooth_devices.items():
            result = bluetooth.lookup_name(address, timeout=parameters.bluetooth_lookup_timeout)
            if result is not None:
                if result == name:
                    logger.logger.debug(name.upper() + ' IN!')
                    return True
                else:
                    result = None
        if result is None:
            logger.logger.debug('NOBODY IN!')
            return False


class Scanner:
    def __init__(self):
        self.blueStream = Subject()
        self.bluetooth = Bluetooth()
        self.sms = Sms()
        self.is_armed = True

    def scan(self):
        self.is_armed = not self.bluetooth.is_there_friendly_devices_nearby()
        self.blueStream.on_next(self.is_armed)
        if self.is_armed:
            self.sms.send_sms_async('system armed')
        else:
            self.sms.send_sms_async('system disarmed')

    def watch(self):
        while True:
            if self.is_armed:
                time.sleep(parameters.main_interval_between_scan_while_armed)
            else:
                time.sleep(parameters.main_interval_between_scan_while_disarmed)
            will_arm = not self.bluetooth.is_there_friendly_devices_nearby()
            if not self.is_armed:
                if will_arm:
                    self.sms.send_sms_async('system armed')
                    self.is_armed = True
                    self.blueStream.on_next(True)
            else:
                if not will_arm:
                    self.sms.send_sms_async('system disarmed')
                    self.is_armed = False
                    self.blueStream.on_next(False)
