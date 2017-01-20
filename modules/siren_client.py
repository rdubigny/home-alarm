from modules.message_client import MessageClient

import config


class SirenClient:
    def __init__(self):
        self.siren_client = MessageClient(config.siren_ip, config.siren_port)

    def turn_on(self):
        self.siren_client.send('siren on')
