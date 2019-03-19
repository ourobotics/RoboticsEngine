# ||==============================================================||
# ||
# ||  Program/File:     EnergyController.py
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

class EnergyController:
	def __init__(self):
		self.type = "ThermoController"
		
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
		self.energy = 80
		self.batteryUnit = "Percentage"

# ||=======================================================================||

	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

# ||=======================================================================||

	def jsonify(self, message = "Null", time = strftime("%a;%d-%m-%Y;%H:%M:%S", localtime()), function = "jsonify"):
		return {
			"Generic Information": {
				"_Class": self.type,
				"_Function": function,
				"Duty": self.duty,
				"Activity": self.active,
				"Message": message,
				"Time": time,
				"Debug Logger": {
					"Debug": self.config["Debug"],
					"Standard": self.config["Standard"],
					"Warning": self.config["Warning"],
					"Error": self.config["Error"]
				}
			},
			"Specific Information": {
				"Energy": self.energy,
				"Battery Unit": self.batteryUnit
			}
		}

# ||=======================================================================||

	def testEnergy(self):
		self.active = True
		self.updateCurrentDutyLog("Testing Energy")
		while self.active:
			self.updateCurrentDuty("Testing Energy")
			for i in range(10):
				self.energy += 1
				sleep(1)
			for i in range(10):
				self.energy -= 1
				sleep(1)
		self.updateCurrentDutyLog("Stopping Energy Tests")
			
# ||=======================================================================||