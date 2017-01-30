from rx.subjects import Subject

from modules import logger
from modules import utils
from modules.message_server import MessageServer

import config
import parameters


class DoorListener:
    def __init__(self):
        self.door_message_server = MessageServer(config.door_tag_port)
        self.openDoorStream = Subject()
        self.vibeDoorStream = Subject()

    def on_message(self, data):
        if data == 'door opened':
            self.openDoorStream.on_next(True)
        if data == 'door hit':
            self.vibeDoorStream.on_next(True)

    def listen(self):
        self.door_message_server.listen(self.on_message)
