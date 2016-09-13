import requests
import signal
import sys
import threading
from modules import logger
import config
import parameters


class Emberlight:

    def __init__(self):
        self.timer = None
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

    def turn_on(self, duration = parameters.lightup_duration):
        if self.timer is None:
            # if no timer was previously set then turn on the light
            # TODO make this async
            r = requests.get('https://maker.ifttt.com/trigger/' + config.maker_ifttt_turn_light_on_action_name
                             + '/with/key/' + config.maker_ifttt_api_key)
            if r.status_code is 200:
                logger.logger.info('EMBERLIGHT ON!')
            else:
                # TODO manage error case
                logger.logger.info('IFTTT NOT RESPONDING!')
        else:
            # reset timer
            self.timer.cancel()
            self.timer = None

        # auto shut down the light after <duration> seconds
        self.timer = threading.Timer(duration, self.turn_off)
        self.timer.start()

    def turn_off(self):
        r = requests.get('https://maker.ifttt.com/trigger/' + config.maker_ifttt_turn_light_off_action_name
                         + '/with/key/' + config.maker_ifttt_api_key)
        if r.status_code is 200:
            logger.logger.info('EMBERLIGHT OFF!')
        else:
            logger.logger.info('IFTTT NOT RESPONDING!')
        if self.timer is not None:
            self.timer = None

    def cleanup(self, *args):
        self.turn_off()
        sys.exit(0)
