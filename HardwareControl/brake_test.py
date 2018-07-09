import sys
import time

try:
    import RPi.GPIO as hd
except RuntimeError:
    print("Run this on the PI as root only you dummy")
    sys.exit(1)

class Brakes(object): # ALWAYS RUN THESE FUNCTIONS ON A SEPARATE THREAD THAN THE HEALTH MONITOR
    # pin definitions
    DFR = 6
    DFL = 13
    DBR = 19
    DBL = 26
    
    PFR = 12
    PFL = 16
    PBR = 20
    PBL = 21

    # error definitions
    E_EARLY_CONVERGENCE = 1 # Brake converging earlier than expected.
    E_LATE_CONVERGENCE = 2 # Brake converging later than expected. (May indicate old brake pad)
    E_ILLEGAL_MOVEMENT = 4 # Brake moved when it wasn't supposed to. 
    E_UNRESPONSIVE_SAFETY = 8 # Safety determined to be cause of error because of incorrect response (A.K.A.: "A FUSE CAN AND WILL FAIL")
    E_DESTROYED_CLOSED = 16 # Fuse failure determined to be cause of error and pad closed
    E_DESTROYED_OPEN = 32 # Fuse failure determined to be cause of error and pad NOT closed
    
    E_UNCERTAIN = 128 # A failure may have occured, need more info (run selftest() to determine)

    status = {"front_left":0, "front_right":0, "back_left":0, "back_right":0, "last_action":"unknown"}

    def __init__(s, pd):
        """
        initializer
        """
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

        s.status["last_action"] = "init"

    def safety(s, safe):
        """
        Engages safety line, verifies signal integrity and functionality
        Also resets directionality and speed
        """
        #reset directionality and speed
        s.pwmfl.stop()
        s.pwmfr.stop()
        s.pwmbl.stop()
        s.pwmbr.stop()

        hd.output(s.DFL, hd.LOW)
        hd.output(s.DFR, hd.LOW)
        hd.output(s.DBL, hd.LOW)
        hd.output(s.DBR, hd.LOW)

        lastfl = s.position["front_left"]
        lastfr = s.position["front_right"]
        lastbl = s.position["back_left"]
        lastbr = s.position["back_right"]

        s.status["front_left"] = 0
        s.status["front_right"] = 0
        s.status["back_left"] = 0
        s.status["back_right"] = 0

        if safe == True:
            # engage safety line
            hd.output(s.SAFETY, hd.HIGH)
            s.status["last_action"] = "engage_safety"
            time.sleep(.01) #--------------------------------------------------------------------------------------- Replace "0.01" with approx. time of two sensor readings
            # test feedback and function
            if abs(s.current["front"] - s.nominal_f) > 0.06: #------------------------------------------------------ Replace "0.06" with 1% of expected max current
                if (s.position["front_left"] - lastfl) > 3: #------------------------------------------------------- Replace "3" with V/LSB of expected position error
                    s.status["front_left"] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT

                if (s.position["front_right"] - lastfr) > 3: #------------------------------------------------------ Replace "3" with V/LSB of expected position error
                    s.status["front_right"] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT
            else:
                if ((s.position["front_left"] + s.position["front_right"]) - 42) >= 0: # attempt to catch a probable fuse failure event
                    s.status["front_left"] |= E_UNCERTAIN
                    s.status["front_right"] |= E_UNCERTAIN
                else:
                    if (s.position["front_left"] - 21) >= 0:
                        s.status["front_left"] |= E_UNCERTAIN
                    elif (s.position["front_right"] - 21) >= 0:
                        s.status["front_right"] |= E_UNCERTAIN
            
            if abs(s.current["back"] - s.nominal_b) > 0.06: #------------------------------------------------------- Replace "0.06" with 1% of expected max current
                if (s.position["back_left"] - lastbl) > 3: #-------------------------------------------------------- Replace "3" with V/LSB of expected position error
                    s.status["back_left"] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT

                if (s.position["back_right"] - lastbr) > 3: #------------------------------------------------------- Replace "3" with V/LSB of expected position error
                    s.status["back_right"] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT
            else:
                if ((s.position["back_left"] + s.position["back_right"]) - 42) >= 0: # attempt to catch a probable fuse failure event
                    s.status["back_left"] |= E_UNCERTAIN
                    s.status["back_right"] |= E_UNCERTAIN
                else:
                    if (s.position["back_left"] - 21) >= 0:
                        s.status["back_left"] |= E_UNCERTAIN
                    elif (s.position["back_right"] - 21) >= 0:
                        s.status["back_right"] |= E_UNCERTAIN

        else: # safe == True
            # disengage safety line.
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            hd.output(s.SAFETY, hd.LOW)
            s.status["last_action"] = "disengage_safety"
            time.sleep(.01) #--------------------------------------------------------------------------------------- Replace "0.01" with approx. time of two sensor readings
            # test feedback and function
            if abs(s.current["front"] - s.nominal_f) <= 6.3: #------------------------------------------------------ Replace "6.3" with 105% of expected max current
                # front brake undercurrent
                
                # front left
                if (s.position["front_left"] - lastfl) <= 3: #------------------------------------------------------ Replace "3" with V/LSB of expected position error
                    s.status["front_left"] |= E_ILLEGAL_MOVEMENT # brake didn't move (it's supposed to)
                
                if (s.position["front_left"] - 21) < 0:
                    s.status["front_left"] |= E_UNCERTAIN # middle of throw, may be dead
                else:
                    s.status["front_left"] |= E_DESTROYED_CLOSED # end of throw, assume dead

                # front right
                if (s.position["front_right"] - lastfr) <= 3: #----------------------------------------------------- Replace "3" with V/LSB of expected position error
                    s.status["front_right"] |= E_ILLEGAL_MOVEMENT # brake didn't move (it's supposed to)
                
                if (s.position["front_right"] - 21) < 0:
                    s.status["front_right"] |= E_UNCERTAIN # middle of throw, may be dead
                else:
                    s.status["front_right"] |= E_DESTROYED_CLOSED # end of throw, assume dead
            
            if abs(s.current["back"] - s.nominal_b) <= 6.3: #------------------------------------------------------- Replace "6.3" with 105% of expected max current
                # back brake undercurrent
                
                # back left
                if (s.position["back_left"] - lastbl) <= 3: #------------------------------------------------------ Replace "3" with V/LSB of expected position error
                    s.status["back_left"] |= E_ILLEGAL_MOVEMENT # brake didn't move (it's supposed to)
                
                if (s.position["back_left"] - 21) < 0:
                    s.status["back_left"] |= E_UNCERTAIN # middle of throw, may be dead
                else:
                    s.status["back_left"] |= E_DESTROYED_CLOSED # end of throw, assume dead

                # back right
                if (s.position["back_right"] - lastbr) <= 3: #----------------------------------------------------- Replace "3" with V/LSB of expected position error
                    s.status["back_right"] |= E_ILLEGAL_MOVEMENT # brake didn't move (it's supposed to)
                
                if (s.position["back_right"] - 21) < 0:
                    s.status["back_right"] |= E_UNCERTAIN # middle of throw, may be dead
                else:
                    s.status["back_right"] |= E_DESTROYED_CLOSED # end of throw, assume dead
            
    def selftest(s):
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
                if fcnow < 1.6: #----------------------------------------------------------------------------------- Replace "1.6" with minimum expected current draw in Amperes
                    # Brakes not pulling proper current for engagement
                    return E_FL_UNDER
                elif fcnow < 2: #----------------------------------------------------------------------------------- Replace "2" with maximum expected current draw in Amperes
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
                        if ((s.brakePosition["front_left"] - 20) > 0): #-------------------------------------------- Replace "0" with maximum tolerance for brake retraction
                            brakefl = False
                            s.pwmfl.stop()
                        else:
                            # Error on front_left: overdrawing current
                            s.pwmfl.stop()
                            s.pwmfr.stop()
                    if brakefr == True:
                        if ((s.brakePosition["front_right"] - 20) > 0): #------------------------------------------- Replace "0" with maximum tolerance for brake retraction
                            brakefr = False
                            s.pwmfr.stop()
                        else:
                            # Error on front_right: overdrawing current
                            s.pwmfr.stop()
                            s.pwmfl.stop()

            if (s.current["back"] - s.nominal_b) < 2: #------------------------------------------------------------- Replace "2" with expected current draw in Amperes
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
