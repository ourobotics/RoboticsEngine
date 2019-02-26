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
# Services
# Controllers
# Tools
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Test
# Data
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
# ||===============================================================||

class DataSyncController:
	def __init__(self):
		self.type = "DataSyncController"

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
		self.networkClientPipe = None
		self.EngineDataControllerPipe = None

		# ||=======================||
		# Config <bool>
		self.debug = self.config["Debug"]
		self.log = self.config["Log"]

		# ||=======================||
		# Defaults
		self.duty = "Inactive"

	# |============================================================================|

	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

	# |============================================================================|

	def initializeNetworkClientPipe(self, pipe):
		self.networkClientPipe = pipe
		return 0

	# |============================================================================|

	def initializeEngineDataControllerPipe(self, pipe):
		self.EngineDataControllerPipe = pipe
		return 0



	# |============================================================================|

	def pipeData(self, data):
		if (self.networkClientPipe != ""):
			# ["isOnline"]
			self.networkClientPipe.send(data)
			returnData = self.networkClientPipe.recv()
			return returnData

	# |============================================================================|

	def createProcess(self):
		# self.syncLiveData()
		self.syncLiveDataThread = Thread(target = self.streamData)
		self.syncLiveDataThread.setDaemon(True)
		self.syncLiveDataThread.start()

		logMessage = "syncLiveDataThread Started"
		self.debugLogger.log("Standard", self.type + ': ' + logMessage)

		try:
			while(1):
				# logMessage = "Running"
				# self.debugLogger.log("Standard", self.type + ': ' + logMessage)
				# sleep(10)
				continue
		except KeyboardInterrupt as e:
			logMessage = "Joined"
			self.debugLogger.log("Standard", self.type + ': ' + logMessage)
			return 0
		return 0

	# |============================================================================|

	def streamData(self):
		while (1):
			while (self.active):
				# gpsControllerData = EngineData.GpsController.getLiveData()
				# if (gpsControllerData != None):
				# 	self.networkClient.sendJson("#40001", gpsControllerData)

				# thermoControllerData = EngineData.ThermoController.getLiveData()
				# if (thermoControllerData != None):
				# 	self.networkClient.sendJson("#40005", thermoControllerData)

				# energyControllerData = EngineData.EnergyController.getLiveData()
				# if (energyControllerData != None):
				# 	self.networkClient.sendJson("#40007", energyControllerData)
				self.active = self.pipeData(onlineTest)

				sleep(5)
			onlineTest = ["isOnline"]
			self.active = self.pipeData(onlineTest)
			sleep(5)

# |============================================================================|