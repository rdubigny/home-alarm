import socket

from modules import logger
import parameters


class MessageClient:
    def __init__(self, server_ip, server_port):
        self.HOST = server_ip
        self.PORT = server_port

    def send(self, message):
        logger.logger.info(message.upper() + '!')
        try:
            logger.logger.debug('SENDING MESSAGE...     ' + message.upper())
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(parameters.message_timeout)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((self.HOST, self.PORT))
            s.sendall(bytes(message, 'UTF-8'))
            logger.logger.debug('MESSAGE SENT!')
            s.close()
        except OSError:
            logger.logger.debug('MESSAGE NOT SENT!')
