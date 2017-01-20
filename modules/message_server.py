import socket

from modules import logger


class MessageServer:
    def __init__(self, port):
        self.host = ''
        self.port = port
        self.socket = None

    def listen(self, on_message):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        logger.logger.debug('MESSAGE LISTENING...      ' + str(self.port))
        while True:
            conn, addr = self.socket.accept()
            logger.logger.debug('INCOMING DATA...          ' + str(addr))
            while True:
                data = conn.recv(1024).decode('UTF-8')
                if not data:
                    break
                logger.logger.debug('DATA RECEIVED!            \"' + data + '\"')
                on_message(data)
            conn.close()
