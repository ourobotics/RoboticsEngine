# ||==============================================================||
# ||
# ||  Program/File:     ThermoController.py
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

class ThermoController:
	# def __init__(cls):
	type = "ThermoController"
	duty = "Inactive"
	active = False
	temperature = 40
	degreeUnit = "Fahrenheit"

	@classmethod
	def jsonify(cls, message = "Null", time = -1, function = "jsonify"):
		return {
			"Generic Information": {
				"_Class": cls.type,
				"_Function": function,
				"Duty": cls.duty,
				"Return Status": True,
				"Activity": cls.active,
				"Message": message,
				"Time": time
			},
			"Specific Information": {
				"Temperature": cls.temperature,
				"Degree Unit": cls.degreeUnit
			}
		}

	@classmethod
	def updateCurrentDutyLog(cls, duty, function = "updateCurrentDutyLog"):
		cls.duty = duty
		EngineData.ThermoController.pushInternalLog(cls.jsonify(
			"Duty Update: " + cls.duty,
			str(strftime("%Y-%m-%d %H:%M:%S", localtime())),
			function)
		)

	@classmethod
	def updateCurrentDuty(cls, duty):
		cls.duty = duty
		return 0

	@classmethod
	def testTemperature(cls):
		cls.active = True
		cls.updateCurrentDutyLog("Testing Temperature")
		while cls.active:
			cls.updateCurrentDuty("Testing Temperature")
			for i in range(10):
				cls.temperature += 1
				sleep(1)
			for i in range(10):
				cls.temperature -= 1
				sleep(1)
		cls.updateCurrentDutyLog("Stopping Temperature Tests")
			