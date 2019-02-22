# ||==============================================================||
# ||
# ||  Program/File:     DataSync.py
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
from NetworkClient import NetworkClient
# Services
# Controllers
# Tools
# Test
# Data
from EngineData import EngineData
# Premades
from time import sleep, time, strftime, localtime
from threading import Thread
import traceback
# ||=======================||
# Global Variables
# ||=======================||
# Notes
# ||=======================||
# ||===============================================================||

class DataSyncController:
	def __init__(self, networkClient):
		self.type = "DataSyncController"
		self.duty = "Inactive"
		self.networkClient = networkClient
	
	# @classmethod
	def syncLiveData(self):
		while (1):
			while self.networkClient.connectionStatus:
				if (self.networkClient.isOnline()):
					gpsControllerData = EngineData.GpsController.getLiveData()
					if (gpsControllerData != None):
						self.networkClient.sendJson("#40001", gpsControllerData)

					thermoControllerData = EngineData.ThermoController.getLiveData()
					if (thermoControllerData != None):
						self.networkClient.sendJson("#40005", thermoControllerData)

					energyControllerData = EngineData.EnergyController.getLiveData()
					if (energyControllerData != None):
						self.networkClient.sendJson("#40007", energyControllerData)

				sleep(1)

	# def jsonify(self, message = "Null", time = -1, function = "jsonify"):
	# 	return {
	# 		"Generic Information": {
	# 			"_Class": self.type,
	# 			"_Function": function,
	# 			"Duty": self.duty,
	# 			"Return Status": True,
	# 			"Activity": self.active,
	# 			"Message": message,
	# 			"Time": time
	# 		},
	# 		"Specific Information": {
	# 		}
	# 	}

	# def updateCurrentDutyLog(self, duty, function = "updateCurrentDutyLog"):
	# 	self.duty = duty
	# 	EngineData.GpsController.pushInternalLog(self.jsonify(
	# 		"Duty Update: " + self.duty,
	# 		str(strftime("%Y-%m-%d %H:%M:%S", localtime())),
	# 		function)
	# 	)

	# def updateCurrentDuty(self, duty):
	# 	self.duty = duty
	# 	return 0