import logging
from time import sleep, time
from configparser import ConfigParser


class MainSM(object):

    def __init__(self, tcp, *hardware):

        self.logger = logging.getLogger('SM')

        self.logger.info("[+] Initializing State Machine")

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
        self.logger.info("[+] State set to 'warm'")
        self.state = self.states["warm"]

        self.hardware["brakes"].disengage()


    def launch(self, mode):
        self.logger.info("[+] State set to hot")
        self.logger.info("[+] Launch Clock Started")
        t0 = time()
        self.state = self.states["hot"]
        while True:
            if self.update(mode): break
            sleep(1/self.frame_rate)
            self.frames += 1

        self.logger.info("[+] Flight time {:.2f} seconds".format(time() - t0))

    def update(self, mode):
        """
        if critical error
            emergency
        if at max speed || at max distance
            stop
        """
        return 1


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
        
        # TODO: Engage brakes
        # [!!!] Be 100% sure the pod isn't accelerating before brakes engage
        
        self.logger.info("[+] State set to 'stop'")
        self.state = self.states["stop"]

        self.hardware["brakes"].engage()

        # TODO: block until stopped



