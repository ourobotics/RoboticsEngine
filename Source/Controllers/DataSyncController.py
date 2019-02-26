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
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Test
# Data
from EngineData import EngineData
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

		self.config = self.loadConfig(self.type)

		self.active = False

		# ||=======================||
		# Communication Pipes
		self.networkClientProcessPipe = None

		# ||=======================||
		# Config <bool>
		self.debug = self.config["Debug"]
		self.log = self.config["Log"]

		# ||=======================||
		# Defaults
		self.duty = "Inactive"
		self.debugLogger = DebugLogger(self.type)
		self.debugLogger.setMessageSettings(
			ast.literal_eval(self.config["Debug"]),
			ast.literal_eval(self.config["Standard"]),
			ast.literal_eval(self.config["Warning"]),
			ast.literal_eval(self.config["Error"]))

	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|

	def loadConfig(self, configName):
		configLoader = ConfigLoader()
		config = configLoader.getConfig(configName)
		return config

	# |============================================================================|

	def checkDebug(self):
		if (self.debug == True):
			return "Debug"
		return ""

	# |============================================================================|

	def updateCurrentDutyLog(self, duty, function = "updateCurrentDutyLog"):
		self.duty = duty
		DeviceData.NetworkServer.pushInternalLog(self.jsonify(
			"Duty Update: " + self.duty,
			str(strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())),
			function)
		)
		return 0

	# |============================================================================|

	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|

	def initializeNetworkClientPipe(self, pipe):
		self.networkClientProcessPipe = pipe
		return 0

	# |============================================================================|

	def pipeData(self, data):
		if (self.networkClientProcessPipe != ""):
			# ["isOnline"]
			self.networkClientProcessPipe.send(data)
			returnData = self.networkClientProcessPipe.recv()
			return returnData


	# |============================================================================|

	def createProcess(self):
		# self.syncLiveData()
		self.syncLiveDataThread = Thread(target = self.syncLiveData)
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

	def syncLiveData(self):
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