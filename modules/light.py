import requests
import signal
import sys
import threading
from modules import logger
import config
import parameters

class Light:

    def __init__(self):
        self.timer = None
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        self.url = 'http://' + config.light_api_ip + '/api/' + config.light_api_key + '/lights/' \
              + config.light_api_lamp_id + '/state'

    def turn_on(self, duration = parameters.lightup_duration):
        if self.timer is None:
            # if no timer was previously set then turn on the light
            # TODO make this async
            payload = "{\"on\":true}"
            r = requests.request("PUT", self.url, data=payload)
            if r.status_code is 200:
                logger.logger.info('LIGHT ON!')
            else:
                # TODO manage error case
                logger.logger.info('LIGHT NOT RESPONDING!')
        else:
            # reset timer
            self.timer.cancel()
            self.timer = None

        # auto shut down the light after <duration> seconds
        self.timer = threading.Timer(duration, self.turn_off)
        self.timer.start()

    def turn_off(self):
        payload = "{\"on\":false}"
        r = requests.request("PUT", self.url, data=payload)
        if r.status_code is 200:
            logger.logger.info('LIGHT OFF!')
        else:
            logger.logger.info('LIGHT NOT RESPONDING!')
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def cleanup(self, *args):
        self.turn_off()
        sys.exit(0)
