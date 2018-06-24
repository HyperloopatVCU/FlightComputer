
import logging
from time import sleep, time
from threading import Thread
from configparser import ConfigParser


class MainSM(object):

    def __init__(self, tcp, *hardware):

        self.logger = logging.getLogger('SM')

        self.logger.info("[+] Initializing State Machine")

        self.estop_signal = False

        self.frames = 0

        self.tcp = tcp

        self.hardware = {
            "brakes": hardware[0],
            "motor": hardware[1]
        }

        self.states = {
            "cold"     : 0x01,  # Pod is off, This is the safe state
            "warm"     : 0x02,  # Preparing pod for flight
            "hot"      : 0x03,  # Pod is in flight
            "emergency": 0x04,  # Bring hot pod to a stop
            "stop"     : 0x05   # Emergency stop
        }

        self.state_str = {
            0x01: "cold",
            0x02: "warm",
            0x03: "hot",
            0x04: "emergency",
            0x05: "stop"
        }

        self.cold()

        self.config = ConfigParser()
        self.config.read('config.ini')
        
        self.frame_rate = self.config['State'].getint('frame_rate')

    def cold(self):
        self.logger.info("[+] State set to 'cold'")
        self.state = self.states["cold"]

    def warm_up(self):
        """
        Disengage Breaks, microcontrollers should zero sensors
        """
        if self.state != self.states["cold"]:
            self.logger.warn("[*] Pod must be cold in order to enter warm")
            return

        self.logger.info("[+] State set to 'warm'")
        self.state = self.states["warm"]

        self.hardware["brakes"].disengage()


    def launch(self, mode):
        if self.state != self.states["warm"]:
            self.logger.warn("[*] Pod must be warm to move")
            return

        # Create seperate execution thread for comm
        tcp_thread = Thread(target=self.tcp.connect, name='TCPThread')
        tcp_thread.start()

        self.logger.info("[+] State set to hot")
        self.logger.info("[+] Launch Clock Started")
        t0 = time()
        self.state = self.states["hot"]

        while True:
            if self.update(mode): break
            sleep(1/self.frame_rate)
            self.frames += 1

        self.stop()
        self.cold()

        self.logger.info("[+] Flight time {:.2f} seconds".format(time() - t0))

        # Join thread after launch finished
        self.tcp.stop_signal = True
        tcp_thread.join()

    def update(self, mode):
        """
        if critical error
            emergency
        if at max speed || at max distance
            stop
        """

        if self.estop_signal:
            return 1


        return 0


    def emergency(self, ecode):
        """
        Determine Severity
        If it can recover - try to
        Else - stop the pod
        """

        logger.info("[!!!] State set to 'emergency'")
        logger.debug("[-] %s", ecode)
        self.state = self.states["emergency"]
        


    def stop(self):
        
        # TODO: [!!!] Be 100% sure the pod isn't accelerating before brakes engage
        
        self.logger.info("[+] State set to 'stop'")
        self.state = self.states["stop"]

        self.hardware["brakes"].engage()

        # TODO: block until stopped

    def estop(self):
        self.estop_signal = True


