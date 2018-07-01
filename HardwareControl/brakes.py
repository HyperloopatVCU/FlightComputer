import logging
import sys

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! Try using 'sudo' to run your script")
    sys.exit(1)


class Brakes(object):
    """
    CAN bus protocol with motor
    """

    def __init__(self):
        self.logger = logging.getLogger('Brakes')

    def engage(self):
        self.logger.debug("[*] Brakes engaged")
        
        # TODO: Be sure the pod isn't accelerating
        

    def disengage(self):
        self.logger.debug("[*] Brakes disengaged")

