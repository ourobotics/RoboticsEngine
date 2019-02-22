# ||==============================================================||
# ||
# ||  Program/File:     EnergyController.py
# ||
# ||  Description:      
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    27 December 2018 | Logan Wilkovich
# ||===============================================================||
# ||===============================================================||
# ||=======================||
# Routes
# Server
# Services
# Controllers
# Tools
from ConfigLoader import ConfigLoader
# Test
# Data
from EngineData import EngineData
# Premades
from time import sleep, time, strftime, localtime
# ||=======================||
# Global Variables
# ||=======================||
# Notes
# ||=======================||
# ||===============================================================||

class EnergyController:
	def __init__(self):
		self.type = "ThermoController"
		
		self.active = False

		# ||=======================||
		# Default Values
		self.duty = "Inactive"
		self.energy = 80
		self.batteryUnit = "Percentage"

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
				"Energy": self.energy,
				"Battery Unit": self.batteryUnit
			}
		}

	# @classmethod
	def updateCurrentDutyLog(self, duty, function = "updateCurrentDutyLog"):
		self.duty = duty
		EngineData.EnergyController.pushInternalLog(self.jsonify(
			"Duty Update: " + self.duty,
			str(strftime("%Y-%m-%d %H:%M:%S", localtime())),
			function)
		)

	# @classmethod
	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

	# @classmethod
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
			