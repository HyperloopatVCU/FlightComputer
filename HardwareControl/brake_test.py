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

    # PWM duty cycles
    E_JS = 70 # TODO
    E_CR = 90
    D_JS = 30 # TODO
    D_CR = 10 # TODO

    # error definitions
    E_EARLY_CONVERGENCE = 1 # Brake converging earlier than expected.
    E_LATE_CONVERGENCE = 2 # Brake converging later than expected. (May indicate old brake pad)
    E_ILLEGAL_MOVEMENT = 4 # Brake moved when it wasn't supposed to. 
    E_UNRESPONSIVE_SAFETY = 8 # Safety determined to be cause of error because of incorrect response (A.K.A.: "A FUSE CAN AND WILL FAIL")
    E_DESTROYED_CLOSED = 16 # Fuse failure determined to be cause of error and pad closed
    E_DESTROYED_OPEN = 32 # Fuse failure determined to be cause of error and pad NOT closed
    E_OFFSET_CLAMP = 64 # Brakes have closed on improper median
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
                if abs(s.position["front_left"] - lastfl) > 2:
                    s.status["front_left"] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT

                if abs(s.position["front_right"] - lastfr) > 2:
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
                if abs(s.position["back_left"] - lastbl) > 2:
                    s.status["back_left"] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT

                if abs(s.position["back_right"] - lastbr) > 2:
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
            
            # did both reach end of throw? (or total of both throws, may be offset)
            if ((s.position["front_left"] + s.position["front_right"]) - 42) >= 0:
                s.status["front_left"] |= E_DESTROYED_CLOSED # assume fuse fails (that's what this function is designed to do)
                s.status["front_right"] |= E_DESTROYED_CLOSED
                if (abs(s.position["front_left"] - 21) > 4) and (abs(s.position["front_right"] - 21) > 4): # try to catch offset clamp
                    s.status["front_left"] |= E_OFFSET_CLAMP
                    s.status["front_right"] |= E_OFFSET_CLAMP
            else: # if total doesn't add up to total throw, both failed open
                if (s.current["front"] - s.nominal_f) < 5.6:
                    # front brake undercurrent, shouldn't assume a fuse failure (cause could be faulty signal)
                    # front left
                    if abs(s.position["front_left"] - lastfl) <= 2:
                        s.status["front_left"] |= E_ILLEGAL_MOVEMENT # brake didn't move (it's supposed to)
                    if (s.position["front_left"] - 21) < 0:
                        s.status["front_left"] |= E_UNCERTAIN # brake never converged, not sure what happened to it
                    # front right
                    if abs(s.position["front_right"] - lastfr) <= 2:
                        s.status["front_right"] |= E_ILLEGAL_MOVEMENT # brake didn't move (it's supposed to)
                    if (s.position["front_right"] - 21) < 0:
                        s.status["front_right"] |= E_UNCERTAIN # brake never converged, not sure what happened to it
                elif (s.current["front"] - s.nominal_f) > 6.4:
                    # front brake overcurrent caught, assume both brakes dead
                    s.status["front_left"] |= E_DESTROYED_OPEN

            # did both reach end of throw? (or total of both throws, may be offset)
            if ((s.position["back_left"] + s.position["back_right"]) - 42) >= 0:
                s.status["back_left"] |= E_DESTROYED_CLOSED # assume fuse fails (that's what this function is designed to do)
                s.status["back_right"] |= E_DESTROYED_CLOSED
                if (abs(s.position["back_left"] - 21) > 4) and (abs(s.position["back_right"] - 21) > 4): # try to catch offset clamp
                    s.status["back_left"] |= E_OFFSET_CLAMP
                    s.status["back_right"] |= E_OFFSET_CLAMP
            else: # if total doesn't add up to total throw, both failed open
                if (s.current["back"] - s.nominal_b) < 5.6:
                    # back brake undercurrent, shouldn't assume a fuse failure (cause could be faulty signal)
                    # back left
                    if abs(s.position["back_left"] - lastbl) <= 2:
                        s.status["back_left"] |= E_ILLEGAL_MOVEMENT # brake didn't move (it's supposed to)
                    if (s.position["back_left"] - 21) < 0:
                        s.status["back_left"] |= E_UNCERTAIN # brake never converged, not sure what happened to it
                    # back right
                    if abs(s.position["back_right"] - lastbr) <= 2:
                        s.status["back_right"] |= E_ILLEGAL_MOVEMENT # brake didn't move (it's supposed to)
                    if (s.position["back_right"] - 21) < 0:
                        s.status["back_right"] |= E_UNCERTAIN # brake never converged, not sure what happened to it
                elif (s.current["back"] - s.nominal_b) > 6.4:
                    # back brake overcurrent caught, assume both brakes dead
                    s.status["back_left"] |= E_DESTROYED_OPEN
                    s.status["back_right"] |= E_DESTROYED_OPEN
            
    def selftest(s): # TODO
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


    def engage(s): #TODO
        if s.status["last_action"] == "engage"
            return
        s.status["last_action"] = "engage"

        # resolution flags (set to True if resolved)
        strikeoutf = False
        strikeoutb = False

        # determine functionality (set to True if dead)
        deadf = False
        deadb = False

        # determine individual issue (set to True if issue)
        strikefl = False
        strikefr = False
        strikebl = False
        strikebr = False
        
        # determine convergence (set to True if converged)
        convf = False
        convb = False
        
        lastfl = 0
        lastfr = 0
        lastbl = 0
        lastbr = 0

        # Set directionality
        hd.output(s.DFR, hd.LOW)
        hd.output(s.DFL, hd.LOW)
        hd.output(s.DBR, hd.LOW)
        hd.output(s.DBL, hd.LOW)
        
        # Set FORWARD speed
        s.pwmfl.start(s.E_CR) # "Engage_CRuising"
        s.pwmfr.start(s.E_CR)
        s.pwmbl.start(s.E_CR)
        s.pwmbr.start(s.E_CR)

        while not (deadf and deadb) and not (convf and convb):
            if not deadf:
                if (s.current["front"] - s.nominal_f) > 6.4:
                    # overcurrent, brakes converging. This wouldn't (in normal circumstances) happen unless both brakes are binding.
                    s.pwmfl.stop()
                    s.pwmfr.stop()
                    convf = True
            
                if not strikeoutf and ((s.current["front"] - s.nominal_f) < 5.6):
                    # undercurrent, check for failure
                    if strikefl or strikefr:
                        if abs(s.position["front_left"] - lastfl) > 2:
                            strikefl = False        # false error
                        elif abs(s.position["front_right"] - lastfr) > 2:
                            strikefr = False        # false error
                        if strikefl or strikefr:
                            s.pwmfl.stop()
                            s.pwmfr.stop()
                            deadf = True
                        strikeoutf = True       # determined error
                    elif ((s.current["front"] - nominal_f) - 3) < .4: # current reflects one or zero brakes moving
                        strikefl = True
                        strikefr = True
                        lastfl = s.position["front_left"]
                        lastfr = s.position["front_right"]
                    # otherwise brakes are just slow

            if not deadb:
                if (s.current["back"] - s.nominal_b) > 6.4:
                    # overcurrent, brakes converging.
                    s.pwmbl.stop()
                    s.pwmbr.stop()
                    convb = True
            
                if not strikeoutb and ((current["back"] - s.nomainal_b) < 5.6):
                    # undercurrent, check for failure
                    if strikebl or strikebr:
                        if abs(s.position["back_left"] - lastbl) > 2:
                            strikebl = False        # false error
                        elif abs(s.position["back_right"] - lastbr) > 2:
                            strikebr = False        # false error
                        if strikebl or strikebr:
                            s.pwmbl.stop()
                            s.pwmbr.stop()
                            deadb = True
                        strikeoutb = True       # determined error
                    elif ((s.current["back"] - nominal_b) - 3) < .4: # current reflects one or zero brakes moving
                        strikebl = True
                        strikefr = True
                        lastbl = s.position["back_left"]
                        lastbr = s.position["back_right"]
                    # otherwise brakes are just slow

        # fill in errors, if any.
        if strikeoutf: # determined an error
        if strikeoutb: # determined an error

        # (directionality already set to engage, skip this step)


    def disengage(s): #TODO
