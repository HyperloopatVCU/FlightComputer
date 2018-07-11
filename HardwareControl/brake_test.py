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
    _DFR = 6
    _DFL = 12
    _DBR = 13
    _DBL = 19
    
    _PFR = 16
    _PFL = 26
    _PBR = 20
    _PBL = 21

    _SAFETY = 5

    # PWM duty cycles
    _E_JS = 70 # TODO
    _E_CR = 90
    _D_JS = 30 # TODO
    _D_CR = 10 # TODO

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
        hd.setup(s._DFR, hd.OUT)
        hd.setup(s._DFL, hd.OUT)
        hd.setup(s._DBR, hd.OUT)
        hd.setup(s._DBL, hd.OUT)
        hd.setup(s._SAFETY, hd.OUT)

        s._pwmfr = hd.pwm(s._PFR, 490) # 490 Hz to match Arduino Mega 2560
        s._pwmfl = hd.pwm(s._PFL, 490)
        s._pwmbr = hd.pwm(s._PBR, 490)
        s._pwmbl = hd.pwm(s._PBL, 490)
        
        # Calculate quiescent sensor values
        s.nominal_f = s.current[_FF]
        s.nominal_b = s.current[_BB]

        s.error["last_action"] = "init"

#------------------------------------------------------------------------------#
    
    def _rankposition(s):
        s.status[_BR] = s.status[_BL] = s.status[_FR] = s.status[_FL] = 0

        p = copy.deepcopy(s.position)
        pfront = (p[_FL] + p[_FR]) / 2
        pback = (p[_BL] + p[_BR]) / 2

        if ((p[_FL] + p[_FR]) - 42) >= 0:
            s.status[_FF] |= CLOSED
        else:
            s.status[_FF] |= OPEN
        
        if abs(p[_FL] - p[_FR]) > 3:
            if p[_FL] > p[_FR]:
                s.status[_FL] |= AHEAD
                s.status[_FR] |= BEHIND
            else:
                s.status[_FL] |= BEHIND
                s.status[_FR] |= AHEAD

        if ((p[_BL] + p[_BR]) - 42) >= 0:
            s.status[_BB] |= CLOSED
        else:
            s.status[_BB] |= OPEN

        if abs(p[_BL] - p[_BR]) > 3:
            if p[_BL] > p[_BR]:
                s.status[_BL] |= AHEAD
                s.status[_BR] |= BEHIND
            else:
                s.status[_BL] |= BEHIND
                s.status[_BR] |= AHEAD

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
        s._pwmfl.stop()
        s._pwmfr.stop()
        s._pwmbl.stop()
        s._pwmbr.stop()

        hd.output(s._DFL, hd.LOW)
        hd.output(s._DFR, hd.LOW)
        hd.output(s._DBL, hd.LOW)
        hd.output(s._DBR, hd.LOW)

        s.error[_BR] = s.error[_BL] = s.error[_FR] = s.error[_FL] = 0

        move = True

        if safe:
            # engage safety line
            s.error["last_action"] = "engage_safety"
            move = False
            hd.output(s._SAFETY, hd.HIGH)
        else:
            # disengage safety line
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            # !!!!!! THIS IS DESIGNED TO DESTROY BRAKE FUNCTIONALITY FOR THE REST OF THE RUN !!!!!!
            s.error["last_action"] = "disengage_safety"
            hd.output(s._SAFETY, hd.LOW)

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

        # determine functionality (set to True if dead)
        deadb = deadf = False

        # flag (used for sync)
        fbr = fbl = ffr = ffl = 0
        
        # determine convergence (set to True if converged)
        convb = convf = False
        
        speedbr = speedbl = speedfr = speedfl = s._E_CR # "Engage_CRuising"

        # Set directionality
        hd.output(s._DFR, hd.LOW)
        hd.output(s._DFL, hd.LOW)
        hd.output(s._DBR, hd.LOW)
        hd.output(s._DBL, hd.LOW)
        
        # Set FORWARD speed
        s._pwmfl.start(speedfl)
        s._pwmfr.start(speedfr)
        s._pwmbl.start(speedbl)
        s._pwmbr.start(speedbr)

        while not ((convf or deadf) and (convb or deadb)):
            time.sleep(0.005) #------------------------------------------------------------------------------------- Replace "0.005" with approx. time of one sensor reading
            _rankposition()
            if not (convf or deadf) and ((s.status[_FF] & CLOSED) or ((s.current[_FF] - s.nominal_f) > 6.4)):
                # overcurrent, brakes converging. This wouldn't (in normal circumstances) happen unless both brakes are binding.
                s._pwmfl.stop()
                s._pwmfr.stop()
                convf = True

            if not (convb or deadb) and ((s.status[_BB] & CLOSED) or ((s.current[_BB] - s.nominal_b) > 6.4)):
                s._pwmbl.stop()
                s._pwmbr.stop()
                convb = True

            if not (convf or deadf) and (s.status[_FL] & (AHEAD | BEHIND)):
                # make sure current is nominal
                if ((s.current[_FF] - s.nominal_f) - 3) < 1: # current reflects one or zero brakes moving
                    s._pwmfl.stop()
                    s._pwmfr.stop()
                    deadf = True
                else: # current should be nominal
                    if s.status[_FL] & AHEAD:
                        # take one from FL, add 2 to FR, flag FR
                        ffr++
                        s._pwmfl.start(--speedfl)
                        s._pwmfr.start((speedfr += 2))
                    else:
                        # take one from FR, add 2 to FL, flag FL
                        ffl++
                        s._pwmfl.start((speedfl += 2))
                        s._pwmfr.start(--speedfr)
            else: # do magic to sync the speeds or whatever
                if ffl:
                    s._pwmfl.start((speedfl -= (2 * ffl) -1))
                    s._pwmfr.start((speedfr += ffl))
                    ffl = 0
                if ffr:
                    s._pwmfl.start((speedfl += ffr))
                    s._pwmfr.start((speedfr -= (2 * ffr) -1))
                    ffr = 0

            if not (convb or deadb) and (s.status[_BL] & (AHEAD | BEHIND)):
                if ((s.current[_BB] - nominal_b) - 3) < 1:
                    s._pwmbl.stop()
                    s._pwmbr.stop()
                    deadb = True
                else:
                    if s.status[_BL] & AHEAD:
                        fbr++
                        s._pwmbl.start(--speedbl)
                        s._pwmbr.start((speedbr += 2))
                    else:
                        fbl++
                        s._pwmbl.start((speedbl += 2))
                        s._pwmbr.start(--speedbr)
            else:
                if fbl:
                    s._pwmbl.start((speedbl -= (2 * fbl) -1))
                    s._pwmbr.start((speedbr += fbl))
                    fbl = 0
                if fbr:
                    s._pwmbl.start((speedbl += fbr))
                    s._pwmbr.start((speedbr -= (2 * fbr) -1))
                    fbr = 0

            if (ffl == ffr) and ffl:
                s._pwmfl.start((speedfl = s.E_CR))
                s._pwmfr.start((speedfr = s.E_CR))
                ffr = ffl = 0

            if (fbl == fbr) and fbl:
                s._pwmbl.start((speedbl = s.E_CR))
                s._pwmbr.start((speedbr = s.E_CR))
                fbr = fbl = 0
            
        # fill in errors, if any.
        if deadf: # assume destroyed
            if s.status[_FF] & CLOSED:
                s.error[_FL] |= E_DESTROYED_CLOSED # assume fuse fails (that's what this function is designed to do)
                s.error[_FR] |= E_DESTROYED_CLOSED
                if s.status[_FR] & (AHEAD | BEHIND): # try to catch offset clamp
                    s.status[_FL] |= E_OFFSET_CLAMP
                    s.status[_FR] |= E_OFFSET_CLAMP
            elif s.status[_FF] & OPEN:
                s.error[_FL] |= E_DESTROYED_OPEN
                s.error[_FR] |= E_DESTROYED_OPEN
        
        if s.status[_FF] & OPEN:
            s.error[_FL] |= E_EARLY_CONVERGENCE
            s.error[_FR] |= E_EARLY_CONVERGENCE

        if deadb:
            if s.status[_BB] & CLOSED:
                s.error[_BL] |= E_DESTROYED_CLOSED
                s.error[_BR] |= E_DESTROYED_CLOSED
                if s.status[_BR] & (AHEAD | BEHIND):
                    s.status[_BL] |= E_OFFSET_CLAMP
                    s.status[_BR] |= E_OFFSET_CLAMP
            elif s.status[_BB] & OPEN:
                s.error[_BL] |= E_DESTROYED_OPEN
                s.error[_BR] |= E_DESTROYED_OPEN
        
        if s.status[_BB] & OPEN:
            s.error[_BL] |= E_EARLY_CONVERGENCE
            s.error[_BR] |= E_EARLY_CONVERGENCE

        # (directionality already set to engage, skip this step)

#------------------------------------------------------------------------------#

    def disengage(s): #TODO
