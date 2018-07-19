# import rpi.GPIO as GPIO
from motor import *

class startShut:
    def Startup(self):
        cont_pull_in_volt = int("volt", x4655sub08)
        key_switch = False
        forward_switch = False
        if cont_pull_in_volt >= 12:
            print("Motor status: Start")
            key_switch = True
            forward_switch = False
        else:
            print("Motor status: Dead")
            key_switch = False
            forward_switch = False
