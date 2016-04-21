import socket
from modules import logger
from modules import utils
import config
import parameters


class Door:
    def __init__(self):
        self.host = ''
        self.port = config.door_tag_port
        self.opening_alert_duration = parameters.door_opening_alert_duration
        self.last_opened = utils.get_time_x_seconds_ago(self.opening_alert_duration + 1)
        self.hit_alert_duration = parameters.door_hit_alert_duration
        self.last_hitten = utils.get_time_x_seconds_ago(self.hit_alert_duration + 1)
        self.socket = None

    def is_opened(self):
        return utils.seconds_between(self.last_opened, utils.get_time()) < self.opening_alert_duration

    def is_vibrating(self):
        return utils.seconds_between(self.last_hitten, utils.get_time()) < self.hit_alert_duration

    def listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        while True:
            conn, addr = self.socket.accept()
            logger.logger.debug('TAG CONNECTED!            ' + str(addr))
            while True:
                data = conn.recv(1024).decode('UTF-8')
                if not data:
                    break
                logger.logger.debug('DATA RECEIVED!            \"' + data + '\"')
                if data == 'door opened':
                    self.last_opened = utils.get_time()
                if data == 'door hit':
                    self.last_hitten = utils.get_time()
            conn.close()
