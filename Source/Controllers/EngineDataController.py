# |===============================================================|
# ||
# ||  Program/File:		EngineDataController.py
# ||
# ||  Description:		Singleton To Represent Current Data Model
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:	24 December 2018 | Logan Wilkovich
# |===============================================================|
# |===============================================================|
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
from NetworkClientCache import NetworkClientCache
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
# |===============================================================|

class EngineDataController(object):

	def __init__(self):
		self.type = "EngineDataController"

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

		# ||=======================||
		# Config <bool>
		self.debug = self.config["Debug"]
		self.log = self.config["Log"]
		self.useNetworkClientCache = self.config["useNetworkClientCache"]

		# ||=======================||
		# Defaults
		self.duty = "Inactive"
		self.childPipes = []

	# |============================================================================|

	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

	# |============================================================================|

	def jsonify(self, message = "Null", time = strftime("%a;%d-%m-%Y;%H:%M:%S", localtime()), function = "jsonify"):
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
				"Debug": self.debug
			}
		}
		
	# |============================================================================|

	def initializeNetworkClientPipe(self, pipe):
		self.networkClientPipe = pipe
		return 0

	# |============================================================================|

	def pipeNetworkClientData(self, data):
		if (self.networkClientPipe != ""):
			# data = ["isOnline"]
			self.networkClientPipe.send(data)
			returnData = "Empty"
			for i in range(10):
				if (self.networkClientPipe.poll(0.5)):
					returnData = self.networkClientPipe.recv()
					return returnData
			if (returnData == "Empty"):
				returnData = None
				
				logMessage = "Failed To Recieve Data From The networkClientPipe"
				self.debugLogger.log("Error", self.type, logMessage)

	# |============================================================================|

	def pushChildPipe(self, pipe):
		self.childPipes.append(pipe)	

	# |============================================================================|

	def communicationModule(self):
		while (1):
			if (len(self.childPipes) != 0):
				dataRecv = None
				while (dataRecv == None):
					for i in range(len(self.childPipes)):
						pipe = self.childPipes[i]
						# print("Pipe:",i)
						try:
							if (pipe.poll(0.5)):
								dataRecv = pipe.recv() * 3
						except Exception as e:
							print(e)
				# print(dataRecv)

				logMessage = "Reading From Pipe"
				self.debugLogger.log("Debug", self.type, logMessage)

				interactionAccess = {
					"NetworkClientCache.getLiveData": partial(self.networkClientCache.getLiveData),
					"NetworkClientCache.setLiveData": partial(self.networkClientCache.setLiveData, dataRecv[1]),
					"NetworkClientCache.getInternalLog": partial(self.networkClientCache.getInternalLog, dataRecv[1]),
					"NetworkClientCache.pushInternalLog": partial(self.networkClientCache.pushInternalLog, dataRecv[1])
				}
				denyCode = False
				if (dataRecv[0].find("NetworkClientCache") != -1):
					if (self.useNetworkClientCache == False):
						denyCode = True

				if (denyCode == True):
					logMessage = "Pipe Command Denied: " + str(dataRecv)
					self.debugLogger.log("Error", self.type, logMessage)
					comPipe.send("Denied")
					return 0
				else:
					returnData = interactionAccess[dataRecv[0]]()

					logMessage = "Executing Pipe Command: " + str(dataRecv)
					self.debugLogger.log("Debug", self.type, logMessage)

					comPipe.send(returnData)
					return 0
				return 0

	# |============================================================================|

	def createProcess(self):
		logMessage = "Process Started"
		self.debugLogger.log("Standard", self.type, logMessage)

		self.networkClientCache = NetworkClientCache()

		# ||=======================||

		self.communicationThread = Thread(target = self.communicationModule)
		self.communicationThread.setDaemon(True)
		self.communicationThread.start()

		logMessage = "communicationThread Started"
		self.debugLogger.log("Standard", self.type, logMessage)
		
		# ||=======================||

		self.syncEngineDataThread = Thread(target = self.syncEngineData)
		self.syncEngineDataThread.setDaemon(True)
		self.syncEngineDataThread.start()

		logMessage = "syncEngineDataThread Started"
		self.debugLogger.log("Standard", self.type, logMessage)

		try:
			while(1):
				# logMessage = "Running"
				# self.debugLogger.log("Standard", self.type, logMessage)
				# sleep(10)
				continue
		except KeyboardInterrupt as e:
			logMessage = "Process Joined"
			self.debugLogger.log("Standard", self.type, logMessage)
			return 0
		return 0


	# |============================================================================|

	def syncEngineData(self):
		while (1):
			if (self.useNetworkClientCache):
				command = ["jsonify"]
				currentData = self.pipeNetworkClientData(command)
				self.networkClientCache.setLiveData(currentData)

				logMessage = "NetworkClient Data Successfully Synced"
				self.debugLogger.log("Debug", self.type, logMessage)

			sleep(1)


			logMessage = "Engine Data Successfully Synced"
			self.debugLogger.log("Debug", self.type, logMessage)

# |===============================================================|