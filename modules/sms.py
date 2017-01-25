import requests
import threading
from rx import Observer

from modules import logger
from modules import utils

import config
import parameters


class Sms:
    def __init__(self):
        self.min_second_between_sms = parameters.sms_min_interval_between_sms
        self.last_sms_datetime = utils.get_time_x_seconds_ago(self.min_second_between_sms + 1)

    def send_sms(self, sms):
        logger.logger.info('SENDING SMS...')
        payload = {
            'user': config.free_user_id,
            'pass': config.free_user_pass,
            'msg': sms + ' at ' + utils.get_time()
        }
        r = requests.post('https://smsapi.free-mobile.fr/sendmsg', json=payload)
        if r.status_code is 200:
            logger.logger.info('SMS SENT!')
        else:
            # TODO: catch error instead of that
            logger.logger.info('SMS NOT SENT!')
        pass

    def send_sms_async(self, sms):
        logger.logger.info(sms.upper() + '!')
        # send one sms max per n seconds
        if utils.seconds_between(self.last_sms_datetime, utils.get_time()) > self.min_second_between_sms:
            self.last_sms_datetime = utils.get_time()
            new_sms_thread = threading.Thread(target=self.send_sms, args=[sms])
            new_sms_thread.start()


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
