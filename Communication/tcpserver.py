import json
import logging
import threading
from configparser import ConfigParser
from queue import Queue
from socket import *


class TCPComm(object):

    def __init__(self):

        self.logger = logging.getLogger('TCP')

        self.logger.info("[+] Initializing Communication")

        self.stop_signal = False

        self.packets = Queue(-1)  # TODO: Probably need more than one queue

        self.config = ConfigParser()
        self.config.read('config.ini')

        self.host = self.config['Comm']['host'] 
        self.port = self.config['Comm'].getint('port')

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def connect(self):

        self.server.listen(10)
        self.logger.info("[+] Listening on %s, port %d", self.host, self.port)
        
        while not self.stop_signal:
            try:
                self.server.settimeout(0.2)
                client, address = self.server.accept()
                self.logger.debug("[+] Connection successful with %s", address)
                t = threading.Thread(target=self.start, args=(client,), name=address)
                t.start()
            except:
                return

    def start(self, client):
        addr = client.getpeername()
        while True:
            data = client.recv(4096)

            if not data:
                break

            # Decodes message, converts to python dict, puts dict in the queue
            self.packets.put(json.loads(data.decode('utf-8')))

        self.logger.debug("[*] Client disconnect %s", addr)

    def broadcast(self, msg):

        # TODO: Broadcast msg (Which should be some hex number) to all microcontrollers
        
        self.logger.info("[*] Broadcast: %s", msg)

    def pop_data_packet(self):
        
        # TODO: pop a data packet and parse it appropriately

        
        pass

    def close(self):
        self.logger.info("[+] Shutting down TCP Server")
        self.server.close()

