import requests
from rx import Observer

from modules import logger

import config


class LightOnObserver(Observer):
    def __init__(self):
        self.url = 'http://' + config.light_api_ip + '/api/' + config.light_api_key + '/lights/' \
                   + config.light_api_lamp_id + '/state'

    def turn_on(self):
        # TODO make this async
        payload = "{\"on\":true}"
        r = requests.request("PUT", self.url, data=payload)
        if r.status_code is 200:
            logger.logger.info('LIGHT ON!')
        else:
            # TODO manage error case
            logger.logger.info('LIGHT NOT RESPONDING!')

    def on_next(self, x):
        self.turn_on()

    def on_error(self, error):
        pass

    def on_completed(self):
        pass


class LightOffObserver(Observer):
    def __init__(self):
        self.url = 'http://' + config.light_api_ip + '/api/' + config.light_api_key + '/lights/' \
                   + config.light_api_lamp_id + '/state'

    def turn_off(self):
        payload = "{\"on\":false}"
        r = requests.request("PUT", self.url, data=payload)
        if r.status_code is 200:
            logger.logger.info('LIGHT OFF!')
        else:
            logger.logger.info('LIGHT NOT RESPONDING!')

    def on_next(self, x):
        self.turn_off()

    def on_error(self, error):
        pass

    def on_completed(self):
        pass
