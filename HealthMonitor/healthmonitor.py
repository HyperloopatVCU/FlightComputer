"""
    Improvements that need to be made:
    Instead of providing exact numbers, we need ranges of values for necessary data (Add number or ranges to config.ini!)
"""

    # WHAT IS THIS?
    def pod_distance_from_track(self, time):
        if time <=17.08:
            acceleration = 4.5
            distance = acceleration * time**2
        else:
            acceleration = -21.5
            distance = acceleration * time**2

class HealthMonitor(object):

    def __init__(self, comm, sm, pod):
        self.comm = comm # Reference to tcp server
        self.sm = sm     # Reference to state machine

        self.logger = logging.getLogger('TCP')

        self.logger.info("[!!!] [+] Initializing Health Monitoring")

        self.stop_signal = False

        self.frames = 0

        self.config = ConfigParser()
        self.config.read('config.ini')
        
        self.frame_rate = self.config['Health'].getint('frame_rate')
        self.timeout = self.config['Health'].getint('controller_timeout')
        self.bms_allowed_errors = self.config['Health'].getint('bms_allowed_erros')

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


            # System checks (Parameters to this are going to be the packets)
            HPS_check(packet1, packet2, packet3, packet4)
            VPS_check(packet1, packet2, packet3, packet4)
            IMU_check(packet1, packet2, packet3, packet4)
            BMS_check(packet5)

            # Temperature Checks (Parameters not correct yet)
            battery_temp_check(battery_temperature)
            motor_temp_check(motor_temperature)
            motor_controller_temp_check(motor_controller_temp)

            # Voltage and current checks (Parameters not correct yet)
            high_battery_check(voltage, current)
            low_one_battery_check(voltage, current)
            low_2A_battery_check(voltage, current)
            low_2B_battery_check(voltage, current)
            brake_potentiometer_check(voltage, current)

            # Distance Check (Parameters not correct yet)
            pod_distance_from_track(time)

            return

        elif sm.state == sm.states["stopping"]:
            # Add checks for stopping
            return

    def battery_temp_check(self, battery_temperature):
        if battery_temperature <= self.max_battery_temp:
            self.logger.debug("[+] battery temperature good")
        elif battery_temperature <= self.estop_battery_temp:
            self.logger.debug("[*] max battery temperature reached")
        else:
            self.logger.critical("[!!!] battery temperature too high")
            self.sm.estop_signal = True

    def motor_temp_check(self, motor_temperature):
        if motor_temperature <= self.max_motor_temp:
            self.logger.info("[+] motor temp good")
        elif motor_temperature <=self.estop_motor_temp:
            self.logger.info("[*] max motor temperature reached")
        else:
            self.logger.critical("[!!!] motor temp too high")
            self.sm.estop_signal = True


    def motor_controller_temp_check(self, motor_controller):
        if motor_controller <= self.max_motor_controller_temp:
            self.logger.debug("[+] controller temp good")
        elif motor_controller <= self.estop_motor_controller_temp:
            self.logger.debug("[*] controller reached max temp")
        else:
            self.logger.critical("[!!!] controller temp too high")
            self.sm.estop_signal = True

    def high_battery_check(self, voltage, current):
        if voltage <= 90.8 and self.current <= 465:
            self.logger.info("[+] high power battery and voltage are fine")
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


    def low_1_battery_check(self, voltage, current):
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

    def brake_potentiometer_check(self, voltage, current):
    # Some values need to be changed here
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

    def HPS_check(self, packet1, packet2, packet3, packet4):
    """
    HPS error checking
    """
        hpsfailcount = 0
        if packet1["horizontal"]["error"] != 0:
            hpsfailcount += 1
            self.logger.info("[!!!] Error with HPS #1")

        if packet2["horizontal"]["error"] != 0:
            hpsfailcount += 1
            self.logger.info("[!!!] Error with HPS #2")

        if packet3["horizontal"]["error"] != 0:
            self.hpsfailcount += 1
            self.logger.info("[!!!] Error with HPS #3")

        if packet4["horizontal"]["error"] != 0:
            self.hpsfailcount += 1
            self.logger.info("[!!!] Error with HPS #3")

        if hpsfailcount >= 2:
            self.sm.estop_signal = True

    def VPS_check(self, packet1, packet2, packet3, packet4):
    """
    VPS error checking
    """
        vpsfailcount = 0

        if packet1["vertical"]["error"] != 0:
            vpsfailcount += 1
            self.logger.info("[!!!] Error with VPS #1")

        if packet2["vertical"]["error"] != 0:
            vpsfailcount += 1
            self.logger.info("[!!!] Error with VPS #2")

        if packet3["vertical"]["error"] != 0:
            vpsfailcount += 1
            self.logger.info("[!!!] Error with VPS #3")

        if packet4["vertical"]["error"] != 0:
            vpsfailcount += 1
            self.logger.info("[!!!] Error with VPS #4")

        if self.vpsfailcount >= 2:
            self.sm.estop_signal = True

    def IMU_check(self, packet1, packet2, packet3, packet4):
    """
    IMU error checking
    """
        imufailcount = 0
        if packet1["accelerometer"]["error"] != 0:
            self.imufailcount += 1
            self.logger.info("[!!!] Error with IMU #1")

        if packet2["accelerometer"]["error"] != 0:
            imufailcount += 1
            self.logger.info("[!!!] Error with IMU #2")

        if packet3["accelerometer"]["error"] != 0:
            imufailcount += 1
            self.logger.info("[!!!] Error with IMU #3")

        if packet4["accelerometer"]["error"] != 0:
            imufailcount += 1
            self.logger.info("[!!!] Error with IMU #4")

        if imufailcount >= 2:
            self.sm.estop_signal = True

    def BMS_check(self, BMS_packet):
    """
    BMS error checking (This needs to be changed a bit because the for loop won't work)
    """

        if packet5["error"] != 0:
            self.logger.critical("[+] Microcontroller five, error code: %d", packet4["error"])
            self.sm.estop_signal = True
            return
            
        bms_failcount = 0
        for k1, v1 in packet5.items():
            for k2, v2 in v1.items():
                if v2["error"] != 0:
                    bms_failcount += 1
                    self.logger.critical("[+] Microcontroller five, error: %s", k2)

        if bms_failcount >= self.bms_allowed_errors:
            self.logger.critical("[+] Microcontroller five error. Too many errors")
            self.sm.estop_signal = True
            return

