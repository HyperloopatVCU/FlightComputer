
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! Try using 'sudo' to run your script")


class Brakes(object):
    """
    TODO: Use RPi GPIO pins to control brakes
    """

    def __init__(self):
        pass

    def engage_brakes(self):
        pass

    def disengage_brakes(self):
        pass


class MotorController(object):
    """
    TODO: Use RS485 (Or whatever the protocol is) to manipulate the motor
    """

    def __init__(self):
        pass

    def accelerate(self):
        pass

    def idle(self):
        pass
