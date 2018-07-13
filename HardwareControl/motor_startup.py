import rpi.GPIO as GPIO
import motor.py as motor

cont_pull_in_volt = int("volt",0x4655_08)

class Motor_startup:
    key_switch = 9
    forward_switch = 15
    if cont_pull_in_volt >= 12:
        key_switch = True
        forward_switch = True
        print("Motor Start")
    else:
        print("Motor dead")

    from motor import _setThrottle
        self.percent = 0.0
