import requests
import threading
from rx import Observer

from modules import logger
from modules import utils

import config


class SmsObserver(Observer):
    def __init__(self, sms_body):
        super().__init__()
        self.sms_body = sms_body

    def send_sms(self):
        logger.logger.info('SENDING SMS...            ' + self.sms_body.upper())
        payload = {
            'user': config.free_user_id,
            'pass': config.free_user_pass,
            'msg': self.sms_body + ' at ' + utils.get_time()
        }
        r = requests.post('https://smsapi.free-mobile.fr/sendmsg', json=payload)
        if r.status_code is 200:
            logger.logger.info('SMS SENT!')
        else:
            # TODO: catch error instead of that
            logger.logger.info('SMS NOT SENT!')

    def on_next(self, x):
        self.send_sms()

    def on_error(self, error):
        pass

    def on_completed(self):
        pass
