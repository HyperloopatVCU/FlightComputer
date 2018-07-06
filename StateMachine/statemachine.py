
import logging
from time import sleep, time
from threading import Thread
from configparser import ConfigParser

class MainSM(object):

    def __init__(self, pod, *hardware):

        self.logger = logging.getLogger('SM')

        self.logger.info("[+] Initializing State Machine")

        self.estop_signal = False
        self.nstop_signal = False

        self.frames = 0

        self.pod = pod

        self.hardware = {
            "brakes": hardware[0],
            "motor" : hardware[1]
        }

        self.states = {
            "pre-operational"     : 0x01,  # pod is off, This is the safe state
            "operational"         : 0x02,  # Preparing pod for flight
            "accelerating"        : 0x03,  # pod is in flight
            "stopping"            : 0x05   # Normal stopping
            "broken-stopping"     : 0x06   # Braking with one set off brakes
        }

        self.state_str = {
            0x01: "pre-operational",
            0x02: "operational",
            0x03: "accelerating",
            0x05: "stopping",
            0x06: "broken-stopping"
        }

        self.pre-operational()

        self.config = ConfigParser()
        self.config.read('config.ini')
        
        self.frame_rate = self.config['State'].getint('frame_rate')

    def pre_operational(self):
        self.logger.info("[+] State set to 'pre-operational'")
        self.state = self.states["pre-operational"]

    def operational(self):
        """
        Disengage Breaks, microcontrollers should zero sensors
        """
        if self.state != self.states["pre-operational"]:
            self.logger.warn("[*] Pod must be pre-operational in order to be operational")
            return

        self.logger.info("[+] State set to 'operational'")
        self.state = self.states["operational"]

        self.hardware["brakes"].disengage()


    def launch(self, mode):
        if self.state != self.states["operational"]:
            self.logger.warn("[*] pod must be operational to move")
            return

        # Create seperate execution thread for comm
        tcp_thread = Thread(target=self.tcp.connect, name='TCPThread')
        tcp_thread.start()

        self.logger.info("[+] State set to accelerating")
        self.logger.info("[+] Launch Clock Started")
        t0 = time()
        self.state = self.states["accelerating"]

        # Turn the motor on at the apppropriate rpm 
        self.hardware["motor"].accelerate(mode)

        self.nstop_signal = False

        while True:
            if self.update(mode): break
            sleep(1/self.frame_rate)
            self.frames += 1

        self.stop()
        self.pre-operational()

        self.logger.info("[+] Flight time {:.2f} seconds".format(time() - t0))

        # Join thread after launch finished
        self.tcp.stop_signal = True
        tcp_thread.join()

    def update(self, mode):
        """
        if at max speed || at max distance
            stop
        """

        if self.nstop_signal:
            return 1

        if self.estop_signal:
            return 1

        return 0

    def stop(self):
        
        self.hardware["motor"].idle()

        # If the pod is still acclerating forwards the program will wait one
        # second before it engages the brakes to the give the motor time to
        # stop running
        if pod.acceleration > 0.5:
            self.logger.debug("[+] pod still accelerating when trying to brake")
            time.sleep(0.5)

        # TODO: Activate reply to force stop the motor if still accelerating
        
        self.logger.info("[+] State set to 'stopping'")
        self.state = self.states["stopping"]

        self.hardware["brakes"].engage()

        # TODO: block until stopped



