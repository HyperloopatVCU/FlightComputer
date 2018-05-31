import logging
from configparser import ConfigParser
from time import sleep


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
            "hot"     : 0x03,  # Pod is in flight
            "emergency": 0x04,  # Bring hot pod to a stop
            "stop"     : 0x05   # Emergency stop
        }

        self.config = ConfigParser()
        self.config.read('config.ini')
        
        self.frame_rate = self.config['State'].getint('frame_rate')

        self.logger.info("[+] State initialized to 'cold'")
        self.state = self.states["cold"]

    def cold_loop(self):
        """
        Stay here until remotely commanded to warm up
        """
        while True:
            pass

    def warm_up(self):
        """
            Disengage Breaks, microcontrollers should zero sensors
        """
        self.logger.info("[+] State set to 'warm'")
        self.state = self.states["warm"]

        self.hardware["brakes"].disengage()

        self.launch()

    def launch(self):
        self.logger.info("[+] State set to hot")
        self.logger.info("[+] Launch Clock Started")
        t0 = time.time()
        self.state = self.states["hot"]
        while True:
            if self.update(): break
            sleep(1/self.frame_rate)
            self.frames += 1

        self.logger.info("[+] Flight time {:.2f} seconds", time.time() - t0) 
        self.shutdown()

    def update(self):
        
        # TODO: Logic to determine state!
        """
        if at max speed || at max distance || critical error
            shutdown
        """
        return 1



    def shutdown(self):
        
        # TODO: Engage brakes
        # [!!!] Be 100% sure the pod isn't accelerating before brakes engage
        
        self.logger.info("[+] State set to 'stop'")
        self.state = self.states["stop"]

        self.hardware["brakes"].engage()

        # After velocity = 0 and systems shutdown
        self.logger.info("[+] State set to 'cold'")
        self.state = self.states["cold"]

        self.logger.info("[+] State Machine shutdown")

