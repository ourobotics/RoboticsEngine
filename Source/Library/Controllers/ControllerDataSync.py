# ||==============================================================||
# ||
# ||  Program/File:     DataSync.py
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
from threading import Thread
import traceback
import ast
# ||=======================||
# Global Variables
# ||=======================||
# Notes
# ||=======================||
# ||=======================================================================||

class ControllerDataSync:
	def __init__(self, networkClient):
		self.type = "ControllerDataSync"

		self.active = False

		# ||=======================||
		# Program Classes
		self.networkClient = networkClient

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
		# self.networkClientPipe = None
		# self.engineDataControllerPipe = None

		# ||=======================||
		# Config <bool>
		self.debug = self.config["Debug"]
		self.log = self.config["Log"]

		# ||=======================||
		# Defaults
		self.duty = "Inactive"
		self.childPipes = []

# ||=======================================================================||

	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

# ||=======================================================================||

	# def initializeengineDataControllerPipe(self, pipe):
	# 	self.engineDataControllerPipe = pipe
	# 	return 0
	def pushChildPipe(self, _class, pipe):
		self.childPipes.append((_class, pipe))


# ||=======================================================================||

	# def pipeEngineDataControllerData(self, data):
	# 	if (self.engineDataControllerPipe != ""):
	# 		# data = ["isOnline"]
	# 		self.engineDataControllerPipe.send(data)
	# 		returnData = "Empty"
	# 		for i in range(10):
	# 			self.engineDataControllerPipe.poll(0.5)
	# 			returnData = self.engineDataControllerPipe.recv()
	# 			return returnData
	# 		if (returnData == "Empty"):
	# 			returnData = None

	# 			logMessage = "Failed To Recieve Data From The engineDataControllerPipe"
	# 			self.debugLogger.log("Error", self.type, logMessage)

# ||=======================================================================||

	def syncLiveData(self):
		while (1):
			self.active = self.networkClient.isOnline()
			# print(self.active)
			while (self.active):
			# 	# gpsControllerData = EngineData.GpsController.getLiveData()
			# 	# if (gpsControllerData != None):
			# 	# 	self.networkClient.sendJson("#40001", gpsControllerData)

			# 	# thermoControllerData = EngineData.ThermoController.getLiveData()
			# 	# if (thermoControllerData != None):
			# 	# 	self.networkClient.sendJson("#40005", thermoControllerData)

			# 	# energyControllerData = EngineData.EnergyController.getLiveData()
			# 	# if (energyControllerData != None):
			# 	# 	self.networkClient.sendJson("#40007", energyControllerData)
				self.active = self.networkClient.isOnline()
				sleep(5)
			sleep(5)

# ||=======================================================================||