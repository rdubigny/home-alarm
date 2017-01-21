from rx.subjects import Subject

from modules import logger
from modules import utils
from modules.message_server import MessageServer

import config
import parameters


class DoorListener:
    def __init__(self):
        self.door_message_server = MessageServer(config.door_tag_port)
        self.opening_alert_duration = parameters.door_opening_alert_duration
        self.last_opened = utils.get_time_x_seconds_ago(self.opening_alert_duration + 1)
        self.hit_alert_duration = parameters.door_hit_alert_duration
        self.last_hitten = utils.get_time_x_seconds_ago(self.hit_alert_duration + 1)
        self.openDoorStream = Subject()

    def is_opened(self):
        is_opened = utils.seconds_between(self.last_opened, utils.get_time()) < self.opening_alert_duration
        if is_opened:
            logger.logger.debug('OPEN DETECTION!')
        return is_opened

    def is_vibrating(self):
        is_vibrating = utils.seconds_between(self.last_hitten, utils.get_time()) < self.hit_alert_duration
        if is_vibrating:
            logger.logger.debug('VIBE DETECTION!')
        return is_vibrating

    def on_message(self, data):
        if data == 'door opened':
            self.last_opened = utils.get_time()
            self.openDoorStream.on_next(True)
        if data == 'door hit':
            self.last_hitten = utils.get_time()

    def listen(self):
        self.door_message_server.listen(self.on_message)
