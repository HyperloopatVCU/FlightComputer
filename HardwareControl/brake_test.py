import sys
import time
import copy

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

    # id definitions
    _FF = "front"
    _FL = "front_left"
    _FR = "front_right"
    _BB = "back"
    _BL = "back_left"
    _BR = "back_right"

    # status definitions (individual)
    UNKNOWN = 0
    AHEAD = 1
    BEHIND = 2
    # status definitions (couplet)
    CLOSED = 4
    OPEN = 8

    # error definitions
    E_NONE = 0
    E_EARLY_CONVERGENCE = 1 # Brake converging earlier than expected.
    E_LATE_CONVERGENCE = 2 # Brake converging later than expected. (May indicate old brake pad)
    E_ILLEGAL_MOVEMENT = 4 # Brake moved when it wasn't supposed to. 
    E_UNRESPONSIVE_SAFETY = 8 # Safety determined to be cause of error because of incorrect response (A.K.A.: "A FUSE CAN AND WILL FAIL")
    E_DESTROYED_CLOSED = 16 # Fuse failure determined to be cause of error and pad closed
    E_DESTROYED_OPEN = 32 # Fuse failure determined to be cause of error and pad NOT closed
    E_OFFSET_CLAMP = 64 # Brakes have closed on improper median
    E_UNCERTAIN = 128 # A failure may have occured, need more info (run selftest() to determine)

    error = {_FL:E_NONE, _FR:E_NONE, _BL:E_NONE, _BR:E_NONE, "last_action":"unknown"}
    status = {_FL:UNKNOWN, _FR:UNKNOWN, _BL:UNKNOWN, _BR:UNKNOWN, _FF:UNKNOWN, _BB:UNKNOWN}

#------------------------------------------------------------------------------#

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
        s.nominal_f = s.current[_FF]
        s.nominal_b = s.current[_BB]

        s.error["last_action"] = "init"

#------------------------------------------------------------------------------#
    
    def _rankposition(s):
        s.status[FL] = 0
        s.status[FR] = 0
        s.status[BL] = 0
        s.status[BR] = 0

        p = copy.deepcopy(s.position)
        pfront = (p[FL] + p[FR]) / 2
        pback = (p[BL] + p[BR]) / 2

        if ((p[FL] + p[FR]) - 42) >= 0:
            s.status[_FF] |= CLOSED
        else:
            s.status[_FF] |= OPEN
        
        if abs(p[FL] - p[FR]) > 3:
            if p[FL] > p[FR]:
                s.status[FL] |= AHEAD
                s.status[FR] |= BEHIND
            else:
                s.status[FL] |= BEHIND
                s.status[FR] |= AHEAD

        if ((p[BL] + p[BR]) - 42) >= 0:
            s.status[_BB] |= CLOSED
        else:
            s.status[_BB] |= OPEN

        if abs(p[BL] - p[BR]) > 3:
            if p[BL] > p[BR]:
                s.status[BL] |= AHEAD
                s.status[BR] |= BEHIND
            else:
                s.status[BL] |= BEHIND
                s.status[BR] |= AHEAD

        if abs(pfront + pback) > 3:
            if pfront > pback:
                s.status[_FF] |= AHEAD
                s.status[_BB] |= BEHIND
            else:
                s.status[_FF] |= BEHIND
                s.status[_BB] |= AHEAD

#------------------------------------------------------------------------------#
            
    def selftest(s): # TODO
        """
        Runs a prelim test on brake system, verifies signal integrity and functionality
        """
        #if s.engage() != 0:
        #    # brakes have failed on extension
        #    return E_EXTENSION
        #elif s.disengage() != 0:
        #    # brakes have failed on retraction
        #    return E_RETRACTION
        #return 0

#------------------------------------------------------------------------------#

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

        s.error[_FL] = 0
        s.error[_FR] = 0
        s.error[_BL] = 0
        s.error[_BR] = 0

        move = True

        if safe:
            # engage safety line
            s.error["last_action"] = "engage_safety"
            move = False
            hd.output(s.SAFETY, hd.HIGH)
        else:
            # disengage safety line
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            s.error["last_action"] = "disengage_safety"
            hd.output(s.SAFETY, hd.HIGH)

        lastfl = s.position[_FL]
        lastfr = s.position[_FR]
        lastbl = s.position[_BL]
        lastbr = s.position[_BR]
            
        time.sleep(.01) #------------------------------------------------------------------------------------------- Replace "0.01" with approx. time of two sensor readings
            
        _rankposition()

        if (s.status[_FF] & CLOSED) or ((s.current[_FF] - s.nominal_b) > 6.4): # if brakes in closed position or over current, assume failure
            s.error[_FL] |= E_DESTROYED_CLOSED
            s.error[_FR] |= E_DESTROYED_CLOSED
            if safe:
                s.error[_FL] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT
                s.error[_FR] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT
        elif move and (abs(s.current[_FF] - s.nominal_f) < 5.6):
            # brake current reflects something not moving
            if abs(s.position[_FL] - lastfl) <= 2: # brake didn't move (it's supposed to) #------------------------- Replace "2" with brake velocity * "0.01" seconds (see above)
                s.error[_FL] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT | E_DESTROYED_OPEN
            else:
                s.error[_FL] |= E_UNCERTAIN # can't actually decide what happened yet
            
            if abs(s.position[_FR] - lastfr) <= 2: #---------------------------------------------------------------- Replace "2" with brake velocity * "0.01" seconds (see above)
                s.error[_FR] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT | E_DESTROYED_OPEN
            else:
                s.error[_FR] |= E_UNCERTAIN
        elif abs(s.current[_FF] - s.nominal_f) > 0.06: #------------------------------------------------------------ Replace "0.06" with 1% of expected max current
            # brake current reflects something moving
            if abs(s.position[_FL] - lastfl) > 2: # brake moved (it's not supposed to) #---------------------------- Replace "2" with brake velocity * "0.01" seconds (see above)
                s.error[_FL] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT | E_DESTROYED_CLOSED
            else:
                s.error[_FL] |= E_UNCERTAIN
            
            if abs(s.position[_FR] - lastfr) > 2: #----------------------------------------------------------------- Replace "2" with brake velocity * "0.01" seconds (see above)
                s.error[_FR] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT | E_DESTROYED_CLOSED
            else:
                s.error[_FR] |= E_UNCERTAIN

        
        if (s.status[_BB] & CLOSED) or ((s.current[_BB] - s.nominal_b) > 6.4):
            s.error[_BL] |= E_DESTROYED_CLOSED
            s.error[_BR] |= E_DESTROYED_CLOSED
            if safe:
                s.error[_BL] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT
                s.error[_BR] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT
        elif move and (abs(s.current[_BB] - s.nominal_f) < 5.6):
            if abs(s.position[_BL] - lastfl) <= 2: #---------------------------------------------------------------- Replace "2" with brake velocity * "0.01" seconds (see above)
                s.error[_BL] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT | E_DESTROYED_OPEN
            else:
                s.error[_BL] |= E_UNCERTAIN
            
            if abs(s.position[_BR] - lastfr) <= 2: #---------------------------------------------------------------- Replace "2" with brake velocity * "0.01" seconds (see above)
                s.error[_BR] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT | E_DESTROYED_OPEN
            else:
                s.error[_BR] |= E_UNCERTAIN
        elif abs(s.current[_BB] - s.nominal_f) > 0.06: #------------------------------------------------------------ Replace "0.06" with 1% of expected max current
            if abs(s.position[_BL] - lastfl) > 2: #----------------------------------------------------------------- Replace "2" with brake velocity * "0.01" seconds (see above)
                s.error[_BL] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT | E_DESTROYED_CLOSED
            else:
                s.error[_BL] |= E_UNCERTAIN
            
            if abs(s.position[_BR] - lastfr) > 2: #----------------------------------------------------------------- Replace "2" with brake velocity * "0.01" seconds (see above)
                s.error[_BR] |= E_UNRESPONSIVE_SAFETY | E_ILLEGAL_MOVEMENT | E_DESTROYED_CLOSED
            else:
                s.error[_BR] |= E_UNCERTAIN


        if s.status[_FL] & (AHEAD | BEHIND):
            s.error[_FL] |= E_OFFSET_CLAMP
            s.error[_FR] |= E_OFFSET_CLAMP 
        

        if s.status[_BL] & (AHEAD | BEHIND):
            s.error[_BL] |= E_OFFSET_CLAMP
            s.error[_BR] |= E_OFFSET_CLAMP

#------------------------------------------------------------------------------#
    
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
            if deadf: # assume destroyed
                if ((s.position["front_left"] + s.position["front_right"]) - 42) >= 0:
                    s.status["front_left"] |= E_DESTROYED_CLOSED # assume fuse fails (that's what this function is designed to do)
                    s.status["front_right"] |= E_DESTROYED_CLOSED
                    if (abs(s.position["front_left"] - 21) > 4) and (abs(s.position["front_right"] - 21) > 4): # try to catch offset clamp
                        s.status["front_left"] |= E_OFFSET_CLAMP
                        s.status["front_right"] |= E_OFFSET_CLAMP

        if strikeoutb: # determined an error

        # (directionality already set to engage, skip this step)

#------------------------------------------------------------------------------#

    def disengage(s): #TODO
