import motor.py as motor
import rpi.GPIO as GPIO

cont_pull_in_volt = int("volt",0x4655_08)

class Motor_shutdown:
    from motor import _setThrottle
    self.percent = 0.0
    
    from motor import _safety:
    key_switch = 09
    forward_switch = 15
    def voltage(self):
        if cont_pull_in_volt < 12:
        key_switch = False
        forward_switch = False
        print("Motor dead")
        else:
        print("Motor still on")

