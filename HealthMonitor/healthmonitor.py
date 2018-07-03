"""
    Improvements that need to be made:
    Instead of providing exact numbers, we need ranges of values for necessary data (Add number or ranges to config.ini!)
"""

    # Checked
    def battery_temp_check(self, battery_temperature):
        if battery_temperature >= 112:
            self.logger.info("[!!!] battery temperature good")
        elif battery_temperature <= 122:
            self.logger.info("[!!!] max battery temperature reached")
        else:
            self.logger.info("[!!!] battery temperature too high")
            self.sm.estop_signal = True

    # Checked
    def motor_temp_check(self, motor_temperature):
        if motor_temperature >= 165:
            self.logger.info("[!!!] motor temp good")
        elif motor_temperature <=175:
            self.logger.info("[!!!] max motor temperature reached")
        else:
            self.logger.info("[!!!] motor temp too high")
            self.sm.estop_signal = True

    # Checked
    def motor_controller_temp_check(self, motor_controller):
        if motor_controller >= 184:
            self.logger.info("[!!!] controller temp good")
        elif motor_controller <= 194:
            self.logger.info("[!!!] controller reached max temp")
        else:
            self.logger.info("[!!!] controller temp too high")
            self.sm.estop_signal = True

    # Checked
    def high_battery_check(self, voltage, current):
        if voltage <= 90.8 and self.current <= 465:
            self.logger.info("[!!!] high power battery and voltage are fine")
        else:
            self.logger.info("[!!!] high power battery voltage or current too high")
            if voltage >= 90.8:
                self.logger.info("[!!!] voltage nearing max")
            elif voltage == 100.8:
                self.logger.info("[!!!] voltage at maximum")
            else:
                self.logger.info("[!!!] voltage too high")
                self.sm.estop_signal = True
            if current >= 465:
                self.logger.info("[!!!] current nearing max")
            elif current == 475:
                self.logger.info("[!!!] current at max")
            else:
                self.logger.info ("current too high")
                self.sm.estop_signal = True

    # Checked
    def low_one_battery_check(self, voltage, current):
        if voltage <= 50.4 and self.current <= 3:
            self.logger.info("[!!!] low power systems good")
        else:
            self.logger.info("[!!!] low power critical")
            if voltage > 50.4:
                self.logger.info("[!!!] voltage too high")
                self.sm.estop_signal = True
            if current >= 3:
                self.logger.info("[!!!] current too high")
                self.sm.estop_signal = True

        # Checked
        def low_2A_battery_check(self, voltage, current):
            if voltage <= 12.6 and self.current <= 4:
                self.logger.info("[!!!] brake power good")
            else:
                self.logger.info("[!!!] brake systems critical")
                if voltage > 12.6:
                    self.logger.info("[!!!] voltage too high")
                    self.sm.estop_signal = True
                if current > 4:
                    self.logger.info("[!!!] current too high")
                    self.sm.estop_signal = True

        # Checked
        def low_2B_battery_check(self, voltage, current):
            if voltage <= 12.6 and self.current <= 4:
                self.logger.info("[!!!] brake power good")
            else:
                self.logger.info("[!!!] brake systems critical")
                if voltage > 12.6:
                    self.logger.info("[!!!] voltage too high")
                   self.sm.estop_signal = True
                if current > 4:
                    self.logger.info("[!!!] current too high")
                   self.sm.estop_signal = True
    # Checked
    def brake_potentiometer_check(self, voltage, current):
        if voltage <= 1 and self.current <= 3:
            self.logger.info("[!!!] potentiometer average good")
        else:
            self.logger.info("[!!!] potentiometer average too much voltage or current")
            if voltage >= 12.6:
                self.logger.info("[!!!] voltage too high")
               self.sm.estop_signal = True
            if current >= 4:
                self.logger.info("[!!!] current too high")
               self.sm.estop_signal = True
#        Change Values

    # Checked
    def pod_distance_from_track(self,time):
        if time <=17.08:
            acceleration = 4.5
            distance = acceleration * time**2
        else:
            acceleration = -21.5
            distance = acceleration * time**2

    # Checked
    def HPS_check(self,hpsone,hpstwo,hpsthree,hpsfour, hpsfailcount):
        hpsfailcount = 0
        while True:
            try:
                packet1 = self.comm.controller1.get(timeout=2)
            except:
                "Emergency Stop the Pod"
                hpsfailcount += 1

            if packet1["horizontal"]["error"] == 0:
                hpsone = 1
            else:
                hpsone = 0
                hpsfailcount += 1
                self.logger.info("[!!!] Error with HPS #1")

            try:
                packet2 = self.comm.controller2.get(timeout=2)
            except:
                "Emergency Stop the Pod"
                hpsfailcount += 1
            if packet2["horizontal"]["error"] == 0:
                hpstwo = 1
            else:
                hpstwo = 0
                hpsfailcount += 1
                self.logger.info("[!!!] Error with HPS #2")

            try:
                packet3 = self.comm.controller3.get(timeout=2)
            except:
                "Emergency Stop the Pod"
                self.hpsfailcount = self.hpsfailcount + 1
                return 1
            if packet3["horizontal"]["error"] == 0:
                self.hpsthree = 1
            else:
                self.hpsthree = 0
                self.hpsfailcount = self.hpsfailcount + 1
                self.logger.info("[!!!] Error with HPS #3")

            try:
                packet4 = self.comm.controller4.get(timeout=2)
            except:
                "Emergency Stop the Pod"
                self.hpsfailcount = self.hpsfailcount + 1
            if packet4["horizontal"]["error"] == 0:
                self.hpsfour = 1
            else:
                self.hpsfour = 0
                self.hpsfailcount = self.hpsfailcount + 1
                self.logger.info("[!!!] Error with HPS #3")

            if self.hpsfailcount >= 2:
                self.sm.estop_signal = True

    # Checked
    def VPS_check(self,vpsone,vpstwo,vpsthree,vpsfour, vpsfailcount):
        vpsfailcount = 0
        while True:

            packet1 = comm.controller1.get(timeout=2)
            if self.comm.microcontroller[1]["vertical"]["error"] == 0:
                vpsone = 1
            else:
                vpsone = 0
                vpsfailcount = self.vpsfailcount + 1
                self.logger.info("[!!!] Error with VPS #1")

            packet2 = comm.controller2.get(timeout=2)
            if self.comm.microcontroller[2]["vertical"]["error"] == 0:
                vpstwo = 1
            else:
                vpstwo = 0
                vpsfailcount = self.vpsfailcount + 1
                self.logger.info("[!!!] Error with VPS #2")

            packet3 = comm.controller3.get(timeout=2)
            if self.comm.microcontroller[3]["vertical"]["error"] == 0:
                vpsthree = 1
            else:
                vpsthree = 0
                vpsfailcount = self.vpsfailcount + 1
                self.logger.info("[!!!] Error with VPS #3")

            packet4 = comm.controller4.get(timeout=2)
            if self.comm.microcontroller[4]["vertical"]["error"] == 0:
                vpsfour = 1
            else:
                vpsfour = 0
                vpsfailcount = self.vpsfailcount + 1
                self.logger.info("[!!!] Error with VPS #4")

            if self.vpsfailcount >= 2:
                self.sm.estop_signal = True

    # Checked
    def IMU_check(self,imuone,imutwo,imuthree,imufour, imufailcount):
        imufailcount = 0
        sensorcondition = True
        while sensorcondition:

            packet1 = comm.controller1.get(timeout=2)
            if self.comm.microcontroller[1]["accelerometer"]["error"] == 0:
               imuone = 1
            else:
                imuone = 0
                self.imufailcount = self.imufailcount + 1
                self.logger.info("[!!!] Error with IMU #1")

            packet2 = comm.controller2.get(timeout=2)
            if self.comm.microcontroller[2]["accelerometer"]["error"] == 0:
                imutwo = 1
            else:
                imutwo = 0
                imufailcount = self.imufailcount + 1
                self.logger.info("[!!!] Error with IMU #2")

            packet3 = comm.controller3.get(timeout=2)
            if self.comm.microcontroller[3]["accelerometer"]["error"] == 0:
                imuthree = 1
            else:
                imuthree = 0
                imufailcount = self.imufailcount + 1
                self.logger.info("[!!!] Error with IMU #3")

            packet4 = comm.controller4.get(timeout=2)
            if self.comm.microcontroller[4]["accelerometer"]["error"] == 0:
                imufour = 1
            else:
                imufour = 0
                imufailcount = self.imufailcount + 1
                self.logger.info("[!!!] Error with IMU #4")

            if imufailcount >= 2:
                sensorcondition = False

                self.sm.estop_signal = True

    # Checked
    def BMS_check(self, bmsone, bmstwo,bmsthree,bmsfour, bmsfive, bmssix, bmsseven, bmseight, bmsnine, bmsten, bmseleven, bmstwelve, bmsthirteen, bmsfourteen, bmsifteen,bmsfailcount):
            # while Something
            #if data exist
                self.bmsone = 1
            #else
                self.bmsone = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #1")
            #if data exists
                self.bmstwo = 1
            #else
                self.bmstwo = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #2")
            #if data exists
                self.bmsthree = 1
            #else
                self.bmsthree = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #3")
            #if data exists
                self.bmsfour = 1
            #else
                self.bmsfour = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #4")
            #if data exists
                self.bmsfive = 1
            #else
                self.bmsfive = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #5")
            #if data exists
                self.bmssix = 1
            #else
                self.bmssix = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #6")
            #if data exists
                self.bmsseven = 1
            #else
                self.bmsseven = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #7")
            #if data exists
                self.bmseight = 1
            #else
                self.bmseight = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #8")
            #if data exists
                self.bmsnine = 1
            #else
                self.bmsnine = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #9")
            #if data exists
                self.bmsten = 1
            #else
                self.bmsten = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #10")
            #if data exists
                self.bmseleven = 1
            #else
                self.bmseleven = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #11")
            #if data exists
                self.bmstwelve = 1
            #else
                self.bmstwelve = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #12")
            #if data exists
                self.bmsthirteen = 1
            #else
                self.bmsthirteen = 0
                self.bmsfailcount    1
                self.logger.info("[!!!] Error with BMS #13")
            #if data exists
                self.bmsfourteen = 1
            #else
                self.bmsfourteen = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #14")
            #if data exists
                self.bmsfifteen = 1
            #else
                self.bmsfifteen = 0
                self.bmsfailcount += 1
                self.logger.info("[!!!] Error with BMS #15")
            if self.bmsfailcount >= 4:
                self.sm.estop_signal = True

class HealthMonitor(object):

    def __init__(self, comm, sm, pod):
        self.comm = comm
        self.sm = sm

        self.logger = logging.getLogger('TCP')

        self.logger.info("[!!!] [+] Initializing Health Monitoring")

        self.stop_signal = False

        self.config = ConfigParser()
        self.config.read('config.ini')
        
        self.frames = 0
        self.frame_rate = self.config['Health'].getint('frame_rate')

        self.timeout = self.config['Health'].getint('controller_timeout')

    def run(self):
            while not self.stop_signal:
                self.update()
                sleep(1/self.frame_rate)
                self.frames += 1

    def update(self):    
        """
        Any threshold values that may need to be adjusted should be added to
        the config.ini file in the root of the program directory. 
        """
        
        if sm.state == sm.states["pre-operational"]:
            # Add checks for pre-operational
            return

        elif sm.state == sm.states["operational"]:
            # Add checks for operational
            return

        elif sm.state == sm.states["accelerating"]:
            """
            1.)
                Compare sensor values from each queue in the tcpserver.py
                module. If one sensor is a certain deviation away from all the
                rest or there is an error marked by the microcontroller on the
                packet then discard it.

            2.) 
                If a critical sensor has been discarded then stop the pod

            3.) 
                Average all the non-discarded sensor values and update the
                global Pod class in the pod_structure.py module. 
            """

            try:
                # Check to make sure none of the sensors have stopped sending data
                packet1 = self.comm.controller1.get(timeout=self.timeout)
                packet2 = self.comm.controller2.get(timeout=self.timeout)
                packet3 = self.comm.controller3.get(timeout=self.timeout)
                packet4 = self.comm.controller4.get(timeout=self.timeout)
                packet5 = self.comm.controller5.get(timeout=self.timeout)
            except: # queue.Empty exception
                self.logger.critical("[+] Microcontroller timed out!")
                self.sm.estop_signal = True
                return

            

            # (NOT syntactally correct at all but getting there)

            # Temperature Checks 
            battery_temp_check(battery_temperature)
            motor_temp_check(motor_temperature)
            motor_controller_temp_check(motor_controller_temp)

            # Coltage and current checks
            high_battery_check(voltage, current)
            low_one_battery_check(voltage, current)
            low_2A_battery_check(voltage, current)
            low_2B_battery_check(voltage, current)
            brake_potentiometer_check(voltage, current)

            # Distance Check
            pod_distance_from_track(time)

            # More system checks
            HPS_check(hpsone,hpstwo,hpsthree,hpsfour, hpsfailcount)
            VPS_check(vpsone,vpstwo,vpsthree,vpsfour, vpsfailcount)
            IMU_check(imuone,imutwo,imuthree,imufour, imufailcount)
            BMS_check(bmsone, bmstwo,bmsthree,bmsfour, bmsfive, bmssix, bmsseven, bmseight, bmsnine, bmsten, bmseleven, bmstwelve, bmsthirteen, bmsfourteen, bmsifteen,bmsfailcount)


            return

        elif sm.state == sm.states["stopping"]:
            # Add checks for stopping
            return

