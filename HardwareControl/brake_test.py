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

    E_FL_UNDER = -1
    E_FL_EARLY = -5

    E_FR_UNDER = -2
    E_FR_EARLY = -6
    
    E_BL_UNDER = -3
    E_BL_EARLY = -7

    E_BR_UNDER = -4
    E_BR_EARLY = -8

    E_ENGAGED = -128
    E_DISENGAGED = -129

    failure = 0
    status = "UNKNOWN"

    def __init__(s, pd):
        """
        initializer
        """
        s.failure = s.safety(True)
        if s.failure != 0:
            # Notify state machine of failure
            return

        # Get object instance of necessary data

        s.current = pd.current
        s.position = pd.position

        # Setup pin positions
        hd.setup(s.DFR, hd.OUT)
        hd.setup(s.DFL, hd.OUT)
        hd.setup(s.DBR, hd.OUT)
        hd.setup(s.DBL, hd.OUT)
        
        s.pwmfr = hd.pwm(s.PFR, 490)
        s.pwmfl = hd.pwm(s.PFL, 490)
        s.pwmbr = hd.pwm(s.PBR, 490)
        s.pwmbl = hd.pwm(s.PBL, 490)
        
        # Calculate quiescent sensor values
        s.nominal_f = s.current["front"]
        s.nominal_b = s.current["back"]

    def safety(s, safe):
        """
        Engages safety line, verifies signal integrity and functionality
        """
        if safe == True:
            #engage safety line
            #test feedback and function
            #pass or fail
            return 0
        #disengage safety line
        #test feedback and function
        #pass or fail
        return 0

    def testsystem(s):
        """
        Runs a prelim test on brake system, verifies signal integrity and functionality
        """
        if s.engage() != 0:
            # brakes have failed on extension
            return E_EXTENSION
        elif s.disengage() != 0:
            # brakes have failed on retraction
            return E_RETRACTION
        return 0


    def engage(s):
        if s.status == "EXTENDED"
           return

        # Set directionality
        hd.output(s.DFR, hd.LOW)
        hd.output(s.DFL, hd.LOW)
        hd.output(s.DBR, hd.LOW)
        hd.output(s.DBL, hd.LOW)
        
        s.pwmfl.start(90)
        s.pwmfr.start(90)
        s.pwmbl.start(90)
        s.pwmbr.start(90)

        time.sleep(4)
        
        #These values MUST increase to verify proper activation of brake actuators

        #s.current["front"]
        #s.current["back"]

        #THIS MUST BE REGULATED FOR PRESSURE
        #need a current -> pressure reading to do this

        #this ends when current touches "regulated value"

        s.pwmfl.stop()
        s.pwmfr.stop()
        s.pwmbl.stop()
        s.pwmbr.stop()

        #s.status = "EXTENDED"


    def disengage(s):
        brakefl = True
        brakefr = True
        brakebl = True
        brakebr = True

        if s.status == "RETRACTED"
           return E_RETRACTED
        
        # Set directionality
        hd.output(s.DFR, hd.HIGH)
        hd.output(s.DFL, hd.HIGH)
        hd.output(s.DBR, hd.HIGH)
        hd.output(s.DBL, hd.HIGH)

        # Set speed
        s.pwmfl.start(90)
        s.pwmfr.start(90)
        s.pwmbl.start(90)
        s.pwmbr.start(90)
        
        # This ends when pads converged
        while True:
            if (brakefl or brakefr) == True:
                fcnow = s.current["front"] - s.qc_f
                if fcnow < 1.6: # Replace "1.6" with minimum expected current draw in Amperes
                    # Brakes not pulling proper current for engagement
                    return E_FL_UNDER
                elif fcnow < 2: # Replace "2" with maximum expected current draw in Amperes
                    # Brakes engaging properly
                    # Check front brake displacement
                    disp = s.brakePosition["front_left"] - s.brakePosition["front_right"]
                    if disp > 5:
                        # Front left pad too fast
                    elif disp < 5:
                        # Front right pad too fast
                else:
                    # Brakes drawing more current
                    # A pad may have converged or some other error
                    # Check front brake position sensor for proper range
                    if brakefl == True:
                        if ((s.brakePosition["front_left"] - 20) > 0):
                            brakefl = False
                            s.pwmfl.stop()
                        else:
                            # Error on front_left: overdrawing current
                            s.pwmfl.stop()
                            s.pwmfr.stop()
                    if brakefr == True:
                        if ((s.brakePosition["front_right"] - 20) > 0):
                            brakefr = False
                            s.pwmfr.stop()
                        else:
                            # Error on front_right: overdrawing current
                            s.pwmfr.stop()
                            s.pwmfl.stop()

            if (s.current["back"] - s.nominal_b) < 2: #replace "2" with expected current draw in Amperes
                # Check front brake displacement
            else:
                # A pad may have converged
                # Check back brake position sensor for proper range
                if ((s.brakePosition["back_left"] - 20) > 0) and (brakebl == True):
                    brakebr = False
                    s.pwmbl.stop()
                if ((s.brakePosition["back_right"] - 20) > 0) and (brakebr == True):
                    brakebr = False
                    s.pwmbr.stop()

            if (brakefl or brakefr or brakebl or brakebr) == False:
                # If deceleration is nominal, return success
                return 0

        #s.status = "RETRACTED"
