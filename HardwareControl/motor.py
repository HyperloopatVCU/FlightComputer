import logging

class Motor(object):
    """
    Can bus protocol
    """

    def __init__(self):
        self.logger = logging.getLogger('Motor')

        self.frequency = 0
        self.temperature = 0

    def accelerate(self, rpm):
        self.logger.debug("[*] Accelerating")

    def idle(self):
        self.logger.debug("[*] Motor Idle")
