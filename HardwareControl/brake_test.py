import sys
import time

try:
    import RPi.GPIO as hd
except RuntimeError:
    print("Run this on the PI as root only you dummy")
    sys.exit(1)

class Brakes(object):
    DFR = 6
    DFL = 13
    DBR = 19
    DBL = 26
    
    PFR = 12
    PFL = 16
    PBR = 20
    PBL = 21

    status = "UNKNOWN"

    def __init__(s, pd):
        
        s.current = pd.current #this has to be a reference, not a value
        s.brakeposition = pd.sensors.brakes.position #need to know how this works

        hd.setup(s.DFR, hd.OUT)
        hd.setup(s.DFL, hd.OUT)
        hd.setup(s.DBR, hd.OUT)
        hd.setup(s.DBL, hd.OUT)
        
        s.nominal_f = s.current["front"]
        s.nominal_b = s.current["back"]

        s.pwm_fr = hd.pwm(s.PFR, 490)
        s.pwm_fl = hd.pwm(s.PFL, 490)
        s.pwm_br = hd.pwm(s.PBR, 490)
        s.pwm_bl = hd.pwm(s.PBL, 490)
        
        s.status = "UNKNOWN"
        
        s.disengage()


    def engage(s):
        #if s.status == "EXTENDED"
        #   return

        hd.output(s.DFR, hd.LOW)
        hd.output(s.DFL, hd.LOW)
        hd.output(s.DBR, hd.LOW)
        hd.output(s.DBL, hd.LOW)
        
        s.pwm_fr.start(90)
        s.pwm_fl.start(90)
        s.pwm_br.start(90)
        s.pwm_bl.start(90)

        time.sleep(4)
        
        #These values MUST increase to verify proper activation of brake actuators

        #s.current["front"]
        #s.current["back"]

        #THIS MUST BE REGULATED FOR PRESSURE
        #need a current -> pressure reading to do this

        #this ends when current touches "regulated value"

        s.pwm1.stop()
        s.pwm2.stop()
        s.pwm3.stop()
        s.pwm4.stop()

        #s.status = "EXTENDED"


    def disengage(s):
        #if s.status == "RETRACTED"
        #   return
        
        hd.output(s.DFR, hd.HIGH)
        hd.output(s.DFL, hd.HIGH)
        hd.output(s.DBR, hd.HIGH)
        hd.output(s.DBL, hd.HIGH)

        s.pwm1.start(90)
        s.pwm2.start(90)
        s.pwm3.start(90)
        s.pwm4.start(90)

        time.sleep(4)
        
        #These values MUST increase to verify proper activation of brake actuators

        #s.current["front"]
        #s.current["back"]

        #This ends when current drops to 0

        s.pwm1.stop()
        s.pwm2.stop()
        s.pwm3.stop()
        s.pwm4.stop()

        #s.status = "RETRACTED"
