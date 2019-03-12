# ||==============================================================||
# ||
# ||  Program/File:     GpsController.py
# ||
# ||  Description:      
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    27 December 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Library
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Premades
from time import sleep, time, strftime, localtime
# ||=======================||
# Global Variables
# ||=======================||
# Notes
# ||=======================||
# ||=======================================================================||

class GpsController:
	def __init__(self):
		self.type = "GpsController"
		
		self.active = False
		
		# ||=======================||
		# Program Classes
		configLoader = ConfigLoader()
		self.config = configLoader.getConfig(self.type)

		self.debugLogger = DebugLogger(self.type)
		self.debugLogger.setMessageSettings(
			ast.literal_eval(self.config["Debug"]),
			ast.literal_eval(self.config["Standard"]),
			ast.literal_eval(self.config["Warning"]),
			ast.literal_eval(self.config["Error"]))

		# ||=======================||
		# Communication Pipes

		# ||=======================||
		# Config <bool>
		self.debug = self.config["Debug"]
		self.log = self.config["Log"]

		# ||=======================||
		# Default Values
		self.duty = "Inactive"
		self.latitude = 41.3507584
		self.longitude = -81.8814976

	# @classmethod
	def jsonify(self, message = "Null", time = -1, function = "jsonify"):
		return {
			"Generic Information": {
				"_Class": self.type,
				"_Function": function,
				"Duty": self.duty,
				"Return Status": True,
				"Activity": self.active,
				"Message": message,
				"Time": time
			},
			"Specific Information": {
				"Latitude": self.latitude,
				"Longitude": self.longitude
			}
		}

	# @classmethod
	def updateCurrentDutyLog(self, duty, function = "updateCurrentDutyLog"):
		self.duty = duty
		EngineData.GpsController.pushInternalLog(self.jsonify(
			"Duty Update: " + self.duty,
			str(strftime("%Y-%m-%d %H:%M:%S", localtime())),
			function)
		)

	# @classmethod
	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

	# @classmethod
	def testMovement(self):
		self.active = True
		self.updateCurrentDutyLog("Testing Gps Movement")
		while self.active:
			self.updateCurrentDuty("Testing Gps Movement")
			for i in range(10):
				self.latitude -= 1
				self.longitude -= 1
				# print(self.latitude, self.longitude)
				sleep(1)
			for i in range(10):
				self.latitude += 1
				self.longitude += 1
				# print(self.latitude, self.longitude)
				sleep(1)
		self.updateCurrentDutyLog("Stopping Gps Movement Tests")
			