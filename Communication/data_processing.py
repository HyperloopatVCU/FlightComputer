
import logging
from configparser import ConfigParser

class Data_Processing(object):

	def __init__(self, tcp):
		self.logger = logging.getLogger('COMM')
		self.logger.info("[+] Initializing Data Processor")

		self.config = ConfigParser()
		self.config.read('config.ini')

		self.frame_rate = self.config['DataProc'].getint('frame_rate')

	def run(self):
		while True:
			self.update()

	def update(self):
		"""
		Do the averaging and deviation checking in this function
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
			self.sm.on_event('estop')
			return


		# System checks (Parameters to this are going to be the packets)
		HPS_check(packet1, packet2, packet3, packet4)
		VPS_check(packet1, packet2, packet3, packet4)
		IMU_check(packet1, packet2, packet3, packet4)
		BMS_check(packet5)

		sum_of_diffs = 0
		mean_of_diffs = 0
		new_sum = 0
		sum_count = 0
		
		
		original_mean_imu_accel_x = 0
		standard_dev_imu_accel_x = 0
		nominal_mean_imu_accel_x = 0
		
		original_mean_imu_accel_x = packet1["accelerometer"]["acceleration"]["x"] + packet2["accelerometer"]["acceleration"]["x"] + packet3["accelerometer"]["acceleration"]["x"] + packet4["accelerometer"]["acceleration"]["x"]
		
		diff_1 = (original_mean_imu_accel_x - packet1["accelerometer"]["acceleration"]["x"])*(original_mean_imu_accel_x - packet1["accelerometer"]["acceleration"]["x"])
		diff_2 = (original_mean_imu_accel_x - packet2["accelerometer"]["acceleration"]["x"])*(original_mean_imu_accel_x - packet2["accelerometer"]["acceleration"]["x"])
		diff_3 = (original_mean_imu_accel_x - packet3["accelerometer"]["acceleration"]["x"])*(original_mean_imu_accel_x - packet3["accelerometer"]["acceleration"]["x"])
		diff_4 = (original_mean_imu_accel_x - packet4["accelerometer"]["acceleration"]["x"])*(original_mean_imu_accel_x - packet4["accelerometer"]["acceleration"]["x"])
		
		sum_of_diffs = diff_1 + diff_2 + diff_3 + diff_4
		mean_of_diffs = sum_of_diffs / 4
		standard_dev_imu_accel_x = sqrt(mean_of_diffs)
		
		if packet1["accelerometer"]["acceleration"]["x"] < (original_mean_imu_accel_x - standard_dev_imu_accel_x) or packet1["accelerometer"]["acceleration"]["x"] > (original_mean_imu_accel_x + standard_dev_imu_accel_x):
			""" calc new mean if nums are out of 1 SD """
			packet1["accelerometer"]["acceleration"]["x"] = False
		else:
			new_sum = new_sum + packet1["accelerometer"]["acceleration"]["x"]
			sum_count = sum_count + 1
		if packet2["accelerometer"]["acceleration"]["x"] < (original_mean_imu_accel_x - standard_dev_imu_accel_x) or packet2["accelerometer"]["acceleration"]["x"] > (original_mean_imu_accel_x + standard_dev_imu_accel_x):
			""" calc new mean if nums are out of 1 SD """
			packet2["accelerometer"]["acceleration"]["x"] = False
		else:
			new_sum = new_sum + packet2["accelerometer"]["acceleration"]["x"]
			sum_count = sum_count + 1
		if packet3["accelerometer"]["acceleration"]["x"] < (original_mean_imu_accel_x - standard_dev_imu_accel_x) or packet3["accelerometer"]["acceleration"]["x"] > (original_mean_imu_accel_x + standard_dev_imu_accel_x):
			""" calc new mean if nums are out of 1 SD """
			packet3["accelerometer"]["acceleration"]["x"] = False
		else:
			new_sum = new_sum + packet3["accelerometer"]["acceleration"]["x"]
			sum_count = sum_count + 1
		if packet4["accelerometer"]["acceleration"]["x"] < (original_mean_imu_accel_x - standard_dev_imu_accel_x) or packet4["accelerometer"]["acceleration"]["x"] > (original_mean_imu_accel_x + standard_dev_imu_accel_x):
			""" calc new mean if nums are out of 1 SD """
			packet["accelerometer"]["acceleration"]["x"] = False
		else:
			""" calc new mean when no nums are out of 1 SD """
			new_sum = new_sum + packet4["accelerometer"]["acceleration"]["x"]
			sum_count = sum_count + 1
			
		nominal_mean_imu_accel_x = new_sum / sum_count
		
		

""" ------------------------------------------------------------------------------------------------------ """		
		original_mean_imu_accel_y = 0
		standard_dev_imu_accel_y = 0
		nominal_mean_imu_accel_y = 0
		
		original_mean_imu_accel_y = packet1["accelerometer"]["acceleration"]["y"] + packet2["accelerometer"]["acceleration"]["y"] + packet3["accelerometer"]["acceleration"]["y"] + packet4["accelerometer"]["acceleration"]["y"]
		
		diff_1 = (original_mean_imu_accel_y - packet1["accelerometer"]["acceleration"]["y"])*(original_mean_imu_accel_y - packet1["accelerometer"]["acceleration"]["y"])
		diff_2 = (original_mean_imu_accel_y - packet2["accelerometer"]["acceleration"]["y"])*(original_mean_imu_accel_y - packet2["accelerometer"]["acceleration"]["y"])
		diff_3 = (original_mean_imu_accel_y - packet3["accelerometer"]["acceleration"]["y"])*(original_mean_imu_accel_y - packet3["accelerometer"]["acceleration"]["y"])
		diff_4 = (original_mean_imu_accel_y - packet4["accelerometer"]["acceleration"]["y"])*(original_mean_imu_accel_y - packet4["accelerometer"]["acceleration"]["y"])
		
		sum_of_diffs = diff_1 + diff_2 + diff_3 + diff_4
		mean_of_diffs = sum_of_diffs / 4
		standard_dev_imu_accel_y = sqrt(mean_of_diffs)
		
		if packet1["accelerometer"]["acceleration"]["y"] < (original_mean_imu_accel_y - standard_dev_imu_accel_y) or packet1["accelerometer"]["acceleration"]["y"] > (original_mean_imu_accel_y + standard_dev_imu_accel_y):
			""" calc new mean if nums are out of 1 SD """
			packet1["accelerometer"]["acceleration"]["y"] = False
		else:
			new_sum = new_sum + packet1["accelerometer"]["acceleration"]["y"]
			sum_count = sum_count + 1
		if packet2["accelerometer"]["acceleration"]["y"] < (original_mean_imu_accel_y - standard_dev_imu_accel_y) or packet2["accelerometer"]["acceleration"]["y"] > (original_mean_imu_accel_y + standard_dev_imu_accel_y):
			""" calc new mean if nums are out of 1 SD """
			packet2["accelerometer"]["acceleration"]["y"] = False
		else:
			new_sum = new_sum + packet2["accelerometer"]["acceleration"]["y"]
			sum_count = sum_count + 1
		if packet3["accelerometer"]["acceleration"]["y"] < (original_mean_imu_accel_y - standard_dev_imu_accel_y) or packet3["accelerometer"]["acceleration"]["y"] > (original_mean_imu_accel_y + standard_dev_imu_accel_y):
			""" calc new mean if nums are out of 1 SD """
			packet3["accelerometer"]["acceleration"]["y"] = False
		else:
			new_sum = new_sum + packet3["accelerometer"]["acceleration"]["y"]
			sum_count = sum_count + 1
		if packet4["accelerometer"]["acceleration"]["y"] < (original_mean_imu_accel_y - standard_dev_imu_accel_y) or packet4["accelerometer"]["acceleration"]["y"] > (original_mean_imu_accel_y + standard_dev_imu_accel_y):
			""" calc new mean if nums are out of 1 SD """
			packet["accelerometer"]["acceleration"]["y"] = False
		else:
			""" calc new mean when no nums are out of 1 SD """
			new_sum = new_sum + packet4["accelerometer"]["acceleration"]["y"]
			sum_count = sum_count + 1
			
		nominal_mean_imu_accel_y = new_sum / sum_count
		
		
		
""" ------------------------------------------------------------------------------------------------------ """
		original_mean_imu_accel_z = 0
		standard_dev_imu_accel_z = 0
		nominal_mean_imu_accel_z = 0
		
		original_mean_imu_accel_z = packet1["accelerometer"]["acceleration"]["z"] + packet2["accelerometer"]["acceleration"]["z"] + packet3["accelerometer"]["acceleration"]["z"] + packet4["accelerometer"]["acceleration"]["z"]
		
		diff_1 = (original_mean_imu_accel_z - packet1["accelerometer"]["acceleration"]["z"])*(original_mean_imu_accel_z - packet1["accelerometer"]["acceleration"]["z"])
		diff_2 = (original_mean_imu_accel_z - packet2["accelerometer"]["acceleration"]["z"])*(original_mean_imu_accel_z - packet2["accelerometer"]["acceleration"]["z"])
		diff_3 = (original_mean_imu_accel_z - packet3["accelerometer"]["acceleration"]["z"])*(original_mean_imu_accel_z - packet3["accelerometer"]["acceleration"]["z"])
		diff_4 = (original_mean_imu_accel_z - packet4["accelerometer"]["acceleration"]["z"])*(original_mean_imu_accel_z - packet4["accelerometer"]["acceleration"]["z"])
		
		sum_of_diffs = diff_1 + diff_2 + diff_3 + diff_4
		mean_of_diffs = sum_of_diffs / 4
		standard_dev_imu_accel_z = sqrt(mean_of_diffs)
		
		if packet1["accelerometer"]["acceleration"]["z"] < (original_mean_imu_accel_z - standard_dev_imu_accel_z) or packet1["accelerometer"]["acceleration"]["z"] > (original_mean_imu_accel_z + standard_dev_imu_accel_z):
			""" calc new mean if nums are out of 1 SD """
			packet1["accelerometer"]["acceleration"]["z"] = False
		else:
			new_sum = new_sum + packet1["accelerometer"]["acceleration"]["z"]
			sum_count = sum_count + 1
		if packet2["accelerometer"]["acceleration"]["z"] < (original_mean_imu_accel_z - standard_dev_imu_accel_z) or packet2["accelerometer"]["acceleration"]["z"] > (original_mean_imu_accel_z + standard_dev_imu_accel_z):
			""" calc new mean if nums are out of 1 SD """
			packet2["accelerometer"]["acceleration"]["z"] = False
		else:
			new_sum = new_sum + packet2["accelerometer"]["acceleration"]["z"]
			sum_count = sum_count + 1
		if packet3["accelerometer"]["acceleration"]["z"] < (original_mean_imu_accel_z - standard_dev_imu_accel_z) or packet3["accelerometer"]["acceleration"]["z"] > (original_mean_imu_accel_z + standard_dev_imu_accel_z):
			""" calc new mean if nums are out of 1 SD """
			packet3["accelerometer"]["acceleration"]["z"] = False
		else:
			new_sum = new_sum + packet3["accelerometer"]["acceleration"]["z"]
			sum_count = sum_count + 1
		if packet4["accelerometer"]["acceleration"]["z"] < (original_mean_imu_accel_z - standard_dev_imu_accel_z) or packet4["accelerometer"]["acceleration"]["z"] > (original_mean_imu_accel_z + standard_dev_imu_accel_z):
			""" calc new mean if nums are out of 1 SD """
			packet["accelerometer"]["speed"]["z"] = False
		else:
			""" calc new mean when no nums are out of 1 SD """
			new_sum = new_sum + packet4["accelerometer"]["speed"]["z"]
			sum_count = sum_count + 1
			
		nominal_mean_imu_accel_z = new_sum / sum_count
		
		
""" ------------------------------------------------------------------------------------------------------ """
		original_mean_imu_speed = 0
		standard_dev_imu_speed = 0
		nominal_mean_imu_speed = 0
		
		original_mean_imu_speed = (packet1["accelerometer"]["speed"]["x"] + packet2["accelerometer"]["speed"]["x"] + packet3["accelerometer"]["speed"]["x"] + packet4["accelerometer"]["speed"]["x"])/4
		
		diff_1 = (original_mean_imu_speed - packet1["accelerometer"]["speed"]["x"])*(original_mean_imu_speed - packet1["accelerometer"]["speed"]["x"])
		diff_2 = (original_mean_imu_speed - packet2["accelerometer"]["speed"]["x"])*(original_mean_imu_speed - packet2["accelerometer"]["speed"]["x"])
		diff_3 = (original_mean_imu_speed - packet3["accelerometer"]["speed"]["x"])*(original_mean_imu_speed - packet3["accelerometer"]["speed"]["x"])
		diff_4 = (original_mean_imu_speed - packet4["accelerometer"]["speed"]["x"])*(original_mean_imu_speed - packet4["accelerometer"]["speed"]["x"])
		
		sum_of_diffs = diff_1 + diff_2 + diff_3 + diff_4
		mean_of_diffs = sum_of_diffs / 4
		standard_dev_imu_speed = sqrt(mean_of_diffs)
		
		if packet1["accelerometer"]["speed"]["x"] < (original_mean_imu_speed - standard_dev_imu_speed) or packet1["accelerometer"]["speed"]["x"] > (original_mean_imu_speed + standard_dev_imu_speed)
			""" calc new mean if nums are out of 1 SD """
			packet1["accelerometer"]["speed"]["x"] = False
		else:
			new_sum = new_sum + packet1["accelerometer"]["speed"]["x"]
			sum_count = sum_count + 1
		if packet2["accelerometer"]["speed"]["x"] < (original_mean_imu_speed - standard_dev_imu_speed) or packet2["accelerometer"]["speed"]["x"] > (original_mean_imu_speed + standard_dev_imu_speed):
			""" calc new mean if nums are out of 1 SD """
			packet2["accelerometer"]["speed"]["x"] = False
		else:
			new_sum = new_sum + packet2["accelerometer"]["speed"]["x"]
			sum_count = sum_count + 1
		if packet3["accelerometer"]["speed"]["x"] < (original_mean_imu_speed - standard_dev_imu_speed) or packet3["accelerometer"]["speed"]["x"] > (original_mean_imu_speed + standard_dev_imu_speed):
			""" calc new mean if nums are out of 1 SD """
			packet3["accelerometer"]["speed"]["x"] = False
		else:
			new_sum = new_sum + packet3["accelerometer"]["speed"]["x"]
			sum_count = sum_count + 1
		if packet4["accelerometer"]["speed"]["x"] < (original_mean_imu_speed - standard_dev_imu_speed) or packet4["accelerometer"]["speed"]["x"] > (original_mean_imu_speed + standard_dev_imu_speed):
			""" calc new mean if nums are out of 1 SD """
			packet["accelerometer"]["speed"]["x"] = False
		else:
			""" calc new mean when no nums are out of 1 SD """
			new_sum = new_sum + packet4["accelerometer"]["speed"]["x"]
			sum_count = sum_count + 1
			
		nominal_mean_imu_speed = new_sum / sum_count
		
		
		
		
""" ------------------------------------------------------------------------------------------------------ """	
		original_mean_imu_pos = 0
		standard_dev_imu_pos = 0
		nominal_mean_imu_pos = 0
		
		original_mean_imu_pos = (packet1["accelerometer"]["position"]["x"] + packet2["accelerometer"]["position"]["x"] + packet3["accelerometer"]["position"]["x"] + packet4["accelerometer"]["position"]["x"])/4
		
		diff_1 = (original_mean_imu_pos - packet1["accelerometer"]["position"]["x"])*(original_mean_imu_pos - packet1["accelerometer"]["position"]["x"])
		diff_2 = (original_mean_imu_pos - packet2["accelerometer"]["position"]["x"])*(original_mean_imu_pos - packet2["accelerometer"]["position"]["x"])
		diff_3 = (original_mean_imu_pos - packet3["accelerometer"]["position"]["x"])*(original_mean_imu_pos - packet3["accelerometer"]["position"]["x"])
		diff_4 = (original_mean_imu_pos - packet4["accelerometer"]["position"]["x"])*(original_mean_imu_pos - packet4["accelerometer"]["position"]["x"])
		
		sum_of_diffs = diff_1 + diff_2 + diff_3 + diff_4
		mean_of_diffs = sum_of_diffs / 4
		standard_dev_imu_pos = sqrt(mean_of_diffs)
		
		if packet1["accelerometer"]["position"]["x"] < (original_mean_imu_pos - standard_dev_imu_pos) or packet1["accelerometer"]["position"]["x"] > (original_mean_imu_pos + standard_dev_imu_pos):
			""" calc new mean if nums are out of 1 SD """
			packet1["accelerometer"]["position"]["x"] = False
		else:
			new_sum = new_sum + packet1["accelerometer"]["position"]["x"]
			sum_count = sum_count + 1
		if packet2["accelerometer"]["position"]["x"] < (original_mean_imu_pos - standard_dev_imu_pos) or packet2["accelerometer"]["position"]["x"] > (original_mean_imu_pos + standard_dev_imu_pos):
			""" calc new mean if nums are out of 1 SD """
			packet2["accelerometer"]["position"]["x"] = False
		else:
			new_sum = new_sum + packet2["accelerometer"]["position"]["x"]
			sum_count = sum_count + 1
		if packet3["accelerometer"]["position"]["x"] < (original_mean_imu_pos - standard_dev_imu_pos) or packet3["accelerometer"]["position"]["x"] > (original_mean_imu_pos + standard_dev_imu_pos):
			""" calc new mean if nums are out of 1 SD """
			packet3["accelerometer"]["position"]["x"] = False
		else:
			new_sum = new_sum + packet3["accelerometer"]["position"]["x"]
			sum_count = sum_count + 1
		if packet4["accelerometer"]["position"]["x"] < (original_mean_imu_pos - standard_dev_imu_pos) or packet4["accelerometer"]["position"]["x"] > (original_mean_imu_pos + standard_dev_imu_pos):
			""" calc new mean if nums are out of 1 SD """
			packet["accelerometer"]["position"]["x"] = False
		else:
			""" calc new mean when no nums are out of 1 SD """
			new_sum = new_sum + packet4["accelerometer"]["position"]["x"]
			sum_count = sum_count + 1
			
		nominal_mean_imu_pos = new_sum / sum_count
		
		
""" ------------------------------------------------------------------------------------------------------ """
		original_mean_vps = 0
		standard_dev_vps = 0
		nominal_mean_vps = 0
		
		original_mean_vps = (packet1["vertical"]["position"]["y"] + packet2["vertical"]["position"]["y"] + packet3["vertical"]["position"]["y"] + packet4["vertical"]["position"]["y"])/4
		
		diff_1 = (original_mean_vps_pos - packet1["vertical"]["position"]["y"])*(original_mean_vps_pos - packet1["vertical"]["position"]["y"])
		diff_2 = (original_mean_vps_pos - packet2["vertical"]["position"]["y"])*(original_mean_vps_pos - packet2["vertical"]["position"]["y"])
		diff_3 = (original_mean_vps_pos - packet3["vertical"]["position"]["y"])*(original_mean_vps_pos - packet3["vertical"]["position"]["y"])
		diff_4 = (original_mean_vps_pos - packet4["vertical"]["position"]["y"])*(original_mean_vps_pos - packet4["vertical"]["position"]["y"])
		
		sum_of_diffs = diff_1 + diff_2 + diff_3 + diff_4
		mean_of_diffs = sum_of_diffs / 4
		standard_dev_vps_pos = sqrt(mean_of_diffs)
		
		if packet1["vertical"]["position"]["x"] < (original_mean_vps_pos - standard_dev_vps_pos) or packet1["vertical"]["position"]["x"] > (original_mean_vps_pos + standard_dev_vps_pos):
			""" calc new mean if nums are out of 1 SD """
			packet1["vertical"]["position"]["x"] = False
		else:
			new_sum = new_sum + packet1["vertical"]["position"]["x"]
			sum_count = sum_count + 1
		if packet2["vertical"]["position"]["x"] < (original_mean_vps_pos - standard_dev_vps_pos) or packet2["vertical"]["position"]["x"] > (original_mean_vps_pos + standard_dev_vps_pos):
			""" calc new mean if nums are out of 1 SD """
			packet2["vertical"]["position"]["x"] = False
		else:
			new_sum = new_sum + packet2["vertical"]["position"]["x"]
			sum_count = sum_count + 1
		if packet3["vertical"]["position"]["x"] < (original_mean_vps_pos - standard_dev_vps_pos) or packet3["vertical"]["position"]["x"] > (original_mean_vps_pos + standard_dev_vps_pos):
			""" calc new mean if nums are out of 1 SD """
			packet3["vertical"]["position"]["x"] = False
		else:
			new_sum = new_sum + packet3["vertical"]["position"]["x"]
			sum_count = sum_count + 1
		if packet4["vertical"]["position"]["x"] < (original_mean_vps_pos - standard_dev_vps_pos) or packet4["vertical"]["position"]["x"] > (original_mean_vps_pos + standard_dev_vps_pos):
			""" calc new mean if nums are out of 1 SD """
			packet["vertical"]["position"]["x"] = False
		else:
			""" calc new mean when no nums are out of 1 SD """
			new_sum = new_sum + packet4["vertical"]["position"]["x"]
			sum_count = sum_count + 1
			
		nominal_mean_vps_pos = new_sum / sum_count
		
		
		
		
""" ------------------------------------------------------------------------------------------------------ """
		original_mean_hps = 0
		standard_dev_hps = 0
		nominal_mean_hps = 0
		
		original_mean_hps = (packet1["horizontal"]["position"]["z"] + packet2["horizontal"]["position"]["z"] + packet3["horizontal"]["position"]["z"] + packet4["horizontal"]["position"]["z"])/4
		
		diff_1 = (original_mean_hps_pos - packet1["horizontal"]["position"]["y"])*(original_mean_hps_pos - packet1["horizontal"]["position"]["y"])
		diff_2 = (original_mean_hps_pos - packet2["horizontal"]["position"]["y"])*(original_mean_hps_pos - packet2["horizontal"]["position"]["y"])
		diff_3 = (original_mean_hps_pos - packet3["horizontal"]["position"]["y"])*(original_mean_hps_pos - packet3["horizontal"]["position"]["y"])
		diff_4 = (original_mean_hps_pos - packet4["horizontal"]["position"]["y"])*(original_mean_hps_pos - packet4["horizontal"]["position"]["y"])
		
		sum_of_diffs = diff_1 + diff_2 + diff_3 + diff_4
		mean_of_diffs = sum_of_diffs / 4
		standard_dev_hps_pos = sqrt(mean_of_diffs)
		
		if packet1["horizontal"]["position"]["x"] < (original_mean_hps_pos - standard_dev_hps_pos) or packet1["horizontal"]["position"]["x"] > (original_mean_hps_pos + standard_dev_hps_pos):
			""" calc new mean if nums are out of 1 SD """
			packet1["horizontal"]["position"]["x"] = False
		else:
			new_sum = new_sum + packet1["horizontal"]["position"]["x"]
			sum_count = sum_count + 1
		if packet2["horizontal"]["position"]["x"] < (original_mean_hps_pos - standard_dev_hps_pos) or packet2["horizontal"]["position"]["x"] > (original_mean_hps_pos + standard_dev_hps_pos):
			""" calc new mean if nums are out of 1 SD """
			packet2["horizontal"]["position"]["x"] = False
		else:
			new_sum = new_sum + packet2["horizontal"]["position"]["x"]
			sum_count = sum_count + 1
		if packet3["horizontal"]["position"]["x"] < (original_mean_hps_pos - standard_dev_hps_pos) or packet3["horizontal"]["position"]["x"] > (original_mean_hps_pos + standard_dev_hps_pos):
			""" calc new mean if nums are out of 1 SD """
			packet3["horizontal"]["position"]["x"] = False
		else:
			new_sum = new_sum + packet3["horizontal"]["position"]["x"]
			sum_count = sum_count + 1
		if packet4["horizontal"]["position"]["x"] < (original_mean_hps_pos - standard_dev_hps_pos) or packet4["horizontal"]["position"]["x"] > (original_mean_hps_pos + standard_dev_hps_pos):
			""" calc new mean if nums are out of 1 SD """
			packet["horizontal"]["position"]["x"] = False
		else:
			""" calc new mean when no nums are out of 1 SD """
			new_sum = new_sum + packet4["horizontal"]["position"]["x"]
			sum_count = sum_count + 1
			
		nominal_mean_hps_pos = new_sum / sum_count
		
