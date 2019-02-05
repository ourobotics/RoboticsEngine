# ||==============================================================||
# ||
# ||  Program/File:     GpsController.py
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

class GpsController:
	# def __init__(cls):
	type = "GpsController"
	duty = "Inactive"
	active = False
	latitude = 41.3507584
	longitude = -81.8814976

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
				"Latitude": cls.latitude,
				"Longitude": cls.longitude
			}
		}

	@classmethod
	def updateCurrentDutyLog(cls, duty, function = "updateCurrentDutyLog"):
		cls.duty = duty
		EngineData.GpsController.pushInternalLog(cls.jsonify(
			"Duty Update: " + cls.duty,
			str(strftime("%Y-%m-%d %H:%M:%S", localtime())),
			function)
		)

	@classmethod
	def updateCurrentDuty(cls, duty):
		cls.duty = duty
		return 0

	@classmethod
	def testMovement(cls):
		cls.active = True
		cls.updateCurrentDutyLog("Testing Gps Movement")
		while cls.active:
			cls.updateCurrentDuty("Testing Gps Movement")
			for i in range(10):
				cls.latitude -= 1
				cls.longitude -= 1
				# print(cls.latitude, cls.longitude)
				sleep(1)
			for i in range(10):
				cls.latitude += 1
				cls.longitude += 1
				# print(cls.latitude, cls.longitude)
				sleep(1)
		cls.updateCurrentDutyLog("Stopping Gps Movement Tests")
			