"""
    Improvements that need to be made:
    Instead of providing exact numbers, we need ranges of values for necessary data (Add number or ranges to config.ini!)
"""

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


        if sm.state == "Pre_Operational":
            # Add checks for pre-operational
            return

        elif sm.state == "Operational":
            # TODO: If the pod is clear to launch
            # sm.on_event('launch-clear') or drift-clear
            return

        elif sm.state == "Accelerating":
            return

        elif sm.state == "Decelerating":
            # Add checks for decelerating
            return

        elif sm.state == "Stop":
            # Add checks for stopping
            return

        elif sm.state == "Estop":
            # Add checks for estopping (If we need any)
            return

        else:
            self.logger.critical("[!!!] State Machine in unknown state %s", \
                                 sm.state)
            sm.on_event('estop')

    def battery_temp_check(self, battery_temperature):
        if self.battery_temperature < self.max_battery_temp:
            self.logger.debug("[+] battery temperature good")
        elif self.battery_temperature >= self.estop_battery_temp:
            self.logger.debug("[*] max battery temperature reached")
            self.sm.on_event('estop')

    def motor_temp_check(self, motor_temperature):
        if self.motor_temperature < self.max_motor_temp:
            self.logger.info("[+] motor temp good")
        elif self.motor_temperature >= self.estop_motor_temp:
            self.logger.info("[*] max motor temperature reached")
            self.sm.on_event('estop')


    def motor_controller_temp_check(self, motor_controller):
        if self.motor_controller < self.max_motor_controller_temp:
            self.logger.debug("[+] controller temp good")
        elif self.motor_controller >= self.estop_motor_controller_temp:
            self.logger.debug("[*] controller reached max temp")
            self.sm.on_event('estop')


    def high_battery_check(self, highPowerVoltage, highPowerCurrent):
        if self.highPowerVoltage >= 101:
            self.logger.info("[!!!] voltage too high")
        elif self.highPowerVoltage < 101 and self.highPowerVoltage >= 60:
            self.logger.info("[!!!] voltage within nominal range")
        elif self.highPowerVoltage < 60 and self.highPowerVoltage >= 50:
            self.logger.info("[!!!] voltage below recommended range")
        elif self.highPowerVoltage < 50:
            self.sm.on_event('estop')

        if self.highPowerCurrent > 400 and self.highPowerCurrent <= 465:
            self.logger.info("[!!!] current nearing max limit")
        elif self.highPowerCurrent > 465 and self.highPowerCurrent <= 480:
            self.logger.info("[!!!] current reached max limit")
        elif self.highPowerCurrent > 480:
            self.logger.info("[!!!] motor drawing greater than allowed current")
            self.sm.on_event('estop')



    def low_battery_check(self, lowPowerVoltage, lowPowerCurrent):
        if self.lowPowerVoltage >= 51.6:
            self.logger.info("[!!!] low battery voltage too high")
        elif self.lowPowerVoltage < 51.6 and self.lowPowerVoltage >= 49:
            self.logger.info("[!!!] low battery voltage within nominal range")
        elif self.lowPowerVoltage < 49 and self.lowPowerVoltage >= 48.5:
            self.logger.info("[!!!] low battery voltage below recommended range")
        elif self.lowPowerVoltage < 48.5:
            self.sm.on_event('estop')

        if self.lowPowerCurrent > 2.50 and self.lowPowerCurrent <= 2.75:
            self.logger.info("[!!!] current nearing max limit")
        elif self.lowPowerCurrent > 2.75 and self.lowPowerCurrent <= 3:
            self.logger.info("[!!!] current reached max limit")
        elif self.lowPowerCurrent > 3:
            self.logger.info("[!!!] low power drawing greater than allowed current")
            self.sm.on_event('estop')

    def front_brake_check(self, frontBrakeVoltage, frontBrakeCurrent):
        if self.frontBrakeVoltage >= 13:
            self.logger.info("[!!!] front brake voltage too high")
        elif self.frontBrakeVoltage < 13 and self.frontBrakeVoltage >= 9:
            self.logger.info("[!!!] front brake voltage within nominal range")
        elif self.frontBrakeVoltage < 9 and self.frontBrakeVoltage >= 6:
            self.logger.info("[!!!] front brake voltage very low")
            #flag for inspection
            #monitor for next couple of seconds
        elif self.frontBrakeVoltage < 6:
            self.sm.on_event('estop')
"""
    def brake_potentiometer_check(self, voltage, current):
    # Some values need to be changed here
        if voltage <= 1 and self.current <= 3:
            self.logger.info("[!!!] potentiometer average good")
        else:
            self.logger.info("[!!!] potentiometer average too much voltage or current")
            if voltage >= 12.6:
                self.logger.info("[!!!] voltage too high")
                self.sm.on_event('estop')
            if current >= 4:
                self.logger.info("[!!!] current too high")
                self.sm.on_event('estop')
"""

    def HPS_check(self, packet1, packet2, packet3, packet4):
        """
        HPS error checking
        """
        self.hpsfailcount = 0
        if packet1["horizontal"]["error"] != 0:
            self.hpsfailcount += 1
            self.logger.info("[!!!] Error with HPS #1")

        if packet2["horizontal"]["error"] != 0:
            self.hpsfailcount += 1
            self.logger.info("[!!!] Error with HPS #2")

        if packet3["horizontal"]["error"] != 0:
            self.hpsfailcount += 1
            self.logger.info("[!!!] Error with HPS #3")

        if packet4["horizontal"]["error"] != 0:
            self.hpsfailcount += 1
            self.logger.info("[!!!] Error with HPS #3")

        if self.hpsfailcount >= 2:
            self.sm.on_event('estop')

    def VPS_check(self, packet1, packet2, packet3, packet4):
        """
        VPS error checking
        """
        self.vpsfailcount = 0

        if packet1["vertical"]["error"] != 0:
            self.vpsfailcount += 1
            self.logger.info("[!!!] Error with VPS #1")

        if packet2["vertical"]["error"] != 0:
            self.vpsfailcount += 1
            self.logger.info("[!!!] Error with VPS #2")

        if packet3["vertical"]["error"] != 0:
            self.vpsfailcount += 1
            self.logger.info("[!!!] Error with VPS #3")

        if packet4["vertical"]["error"] != 0:
            self.vpsfailcount += 1
            self.logger.info("[!!!] Error with VPS #4")

        if self.vpsfailcount >= 2:
            self.sm.on_event('estop')

    def IMU_check(self, packet1, packet2, packet3, packet4):
        """
        IMU error checking
        """
        self.imufailcount = 0
        if packet1["accelerometer"]["error"] != 0:
            self.imufailcount += 1
            self.logger.info("[!!!] Error with IMU #1")

        if packet2["accelerometer"]["error"] != 0:
            self.imufailcount += 1
            self.logger.info("[!!!] Error with IMU #2")

        if packet3["accelerometer"]["error"] != 0:
            self.imufailcount += 1
            self.logger.info("[!!!] Error with IMU #3")

        if packet4["accelerometer"]["error"] != 0:
            self.imufailcount += 1
            self.logger.info("[!!!] Error with IMU #4")

        if self.imufailcount >= 2:
            self.sm.on_event('estop')

    def BMS_check(self, BMS_packet):
        """
        BMS error checking (This needs to be changed a bit because the for loop won't work)
        """
        if packet5["error"] != 0:
            self.logger.critical("[+] Microcontroller five, error code: %d", packet4["error"])
            self.sm.on_event('estop')
            return

        self.bms_failcount = 0
        for k1, v1 in packet5.items():
            for k2, v2 in v1.items():
                if v2["error"] != 0:
                    self.bms_failcount += 1
                    self.logger.critical("[+] Microcontroller five, error: %s", k2)

        if self.bms_failcount >= self.bms_allowed_errors:
            self.logger.critical("[+] Microcontroller five error. Too many errors")
            self.sm.on_event('estop')
            return

    def motor_controller(self, speed,RMS_current):
            self.speed = int("motor speed",0x2010_01)
            if self.speed <= 6000:
                print("motor good")
            else:
                print("motor too fast")
            self.RMS_current = int("Current", 0x2010_05)
