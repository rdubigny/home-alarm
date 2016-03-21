import requests
import threading
from modules import logger
from modules import utils
import config
import parameters


class Message:

    def __init__(self):
        self.min_second_between_messages = parameters.message_min_interval_between_message
        self.last_message_datetime = utils.get_time_x_seconds_ago(self.min_second_between_messages + 1)

    def send_message(self, message):
        logger.logger.info('SENDING MESSAGE...')
        payload = {
            'user': config.free_user_id,
            'pass': config.free_user_pass,
            'msg': message + ' at ' + utils.get_time()
        }
        r = requests.post('https://smsapi.free-mobile.fr/sendmsg', json=payload)
        if r.status_code is 200:
            logger.logger.info('MESSAGE SENT!')
        else:
            logger.logger.error('MESSAGE NOT SENT!')
        pass

    def send_message_async(self, message):
        logger.logger.info(message.upper() + '!')
        # send one message max per n seconds
        if utils.seconds_between(self.last_message_datetime, utils.get_time()) > self.min_second_between_messages:
            self.last_message_datetime = utils.get_time()
            new_message_thread = threading.Thread(target=self.send_message, args=[message])
            new_message_thread.start()
