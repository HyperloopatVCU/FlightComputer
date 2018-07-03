
import logging
from time import sleep, time
from threading import Thread
from configparser import ConfigParser


class MainSM(object):

    def __init__(self, Pod, *hardware):

        self.logger = logging.getLogger('SM')

        self.logger.info("[+] Initializing State Machine")

        self.estop_signal = False
        self.nstop_signal = False

        self.frames = 0

        self.Pod = Pod

        self.hardware = {
            "brakes": hardware[0],
            "motor": hardware[1]
        }

        self.states = {
            "cold"     : 0x01,  # Pod is off, This is the safe state
            "ready"     : 0x02,  # Preparing pod for flight
            "accelerating"      : 0x03,  # Pod is in flight
            "stopping"     : 0x05   # Emergency stop
        }

        self.state_str = {
            0x01: "cold",
            0x02: "ready",
            0x03: "accelerating",
            0x05: "stopping"
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
            self.logger.warn("[*] Pod must be cold in order to be ready")
            return

        self.logger.info("[+] State set to 'ready'")
        self.state = self.states["ready"]

        self.hardware["brakes"].disengage()


    def launch(self, mode):
        if self.state != self.states["ready"]:
            self.logger.warn("[*] Pod must be warm to move")
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
        self.cold()

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
        if Pod.acceleration > 0.5:
            self.logger.debug("[+] Pod still accelerating when trying to brake")
            time.sleep(0.5)
        
        self.logger.info("[+] State set to 'stopping'")
        self.state = self.states["stopping"]

        self.hardware["brakes"].engage()

        # TODO: block until stopped



