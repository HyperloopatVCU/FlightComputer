
import logging
from time import sleep, time
from configparser import ConfigParser
from State import Pre_Operational, Operational, Accelerating, Decelerating, \
Stop, Estop

class MainSM(object):

    def __init__(self, pod, *hardware):

        self.logger = logging.getLogger('SM')

        self.logger.info("[+] Initializing State Machine")

        self.pod = pod
        
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.frame_rate = self.config['State'].getint('frame_rate')

        hardware = {
            "brakes": hardware[0],
            "motor" : hardware[1]
        }
        
        self.state = Pre_Operational(hardware)
        self.on_event('state-up')

    def on_event(self, event):
        self.state = self.state.on_event(event)

