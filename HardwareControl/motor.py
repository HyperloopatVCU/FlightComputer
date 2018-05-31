import logging

class MotorController(object):
    
    # TODO: Use CAN protocol to manipulate the motor
    

    def __init__(self):
        self.logger = logging.getLogger('Motor')

    def accelerate(self):
        self.logger.debug("[*] Accelerating")

    def idle(self):
        self.logger.debug("[*] Motor Idle")
