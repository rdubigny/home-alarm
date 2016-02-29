import bluetooth
from modules import logger
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
