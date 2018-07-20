
import json
import logging
import threading
from configparser import ConfigParser
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM

class TCPComm(object):

    def __init__(self):

        self.logger = logging.getLogger('COMM')

        self.logger.info("[+] Initializing Communication")

        self.stop_signal = False

        # Buffers for each microcontroller
        # TODO: The goal is to get ride of these at some point
        self.controller1 = Queue(1)
        self.controller2 = Queue(1)
        self.controller3 = Queue(1)
        self.controller4 = Queue(1)
        self.controller5 = Queue(1)

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

            # Decodes message, converts to python dict, puts dict in the buffer
            packet = json.loads(data.decode('utf-8'))

            """
            Check packet ID. The packet gets put in the proper place for the
            place to be processed. If there is already a packet blocking the
            space, the most recent packet repalces it.
            """
            if packet["identity"] == "EMS1":
                if self.controller1.full(): # Check if full
                    self.controller1.get()  # Replace with most current
                self.controller1.put(packet)
            elif packet["identity"] == "EMS2":
                if self.controller2.full():
                    self.controller2.get()
                self.controller2.put(packet)
            elif packet["identity"] == "EMS3":
                if self.controller3.full():
                    self.controller3.get()
                self.controller3.put(packet)
            elif packet["identity"] == "EMS4":
                if self.controller4.full():
                    self.controller4.get()
                self.controller4.put(packet)
            elif packet["identity"] == "BMS":
                if self.controller5.full():
                    self.controller5.get()
                self.controller5.put(packet)
            else:
                self.logger.critical("[!!!] Packet isn't IDed right!")

        self.logger.debug("[*] Client disconnect %s", addr)

    def close(self):
        self.logger.info("[+] Shutting down TCP Server")
        self.server.close()

    def test_connection(self):
        self.logger.info("[*] Testing Communication System")
        self.server.listen(10)

        for i in range(5):
            try:
                self.server.settimeout(0.5)
                client, addr = self.server.accept()
                self.logger.info("======> [  %d  ] Controller Connection", i+1)
            except:
                self.logger.critical("[!!!] COMMUNCATION TEST FAILURE")
                break
        else:
            self.logger.info("[+] Communcation Test Success!")

