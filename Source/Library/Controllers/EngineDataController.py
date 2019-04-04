# ||=======================================================================||
# ||
# ||  Program/File:		EngineDataController.py
# ||
# ||  Description:		Singleton To Represent Current Data Model
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:	24 December 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Library
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Data
# from NetworkClientCache import NetworkClientCache
from CacheModule import CacheModule
# Premades
from time import sleep, time, strftime, localtime
from threading import Thread
import traceback
import ast
from functools import partial
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# ||=======================================================================||

class EngineDataController(object):

	def __init__(self):
		self.type = "EngineDataController"

		self.active = False

		# ||=======================||
		# Data Storage Types
		self.dataStorage = {
			"NetworkClient": CacheModule(),
			"RoboticsEngine": CacheModule()
		}
		# self.networkClientCache = NetworkClientCache()
		
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
		self.useCache = {
			"NetworkClient": self.config["useNetworkClientCache"],
			"RoboticsEngine": self.config["useRoboticsEngineCache"]
		}

		# ||=======================||
		# Defaults
		self.duty = "Inactive"
		
# ||=======================================================================||

	def APICommand(self, data):
		newData = data *3
		command = newData[0]
		params = newData[1:]

		try:
			interactionExecution = {
				"NetworkClient.getLiveData": partial(self.dataStorage["NetworkClient"].getLiveData),
				"NetworkClient.setLiveData": partial(self.dataStorage["NetworkClient"].setLiveData, params[1]),
				"NetworkClient.getInternalLog": partial(self.dataStorage["NetworkClient"].getInternalLog, params[1]),
				"NetworkClient.pushInternalLog": partial(self.dataStorage["NetworkClient"].pushInternalLog, params[1]),
				"RoboticsEngine.getLiveData": partial(self.dataStorage["RoboticsEngine"].getLiveData),
				"RoboticsEngine.setLiveData": partial(self.dataStorage["RoboticsEngine"].setLiveData, params[1]),
				"RoboticsEngine.getInternalLog": partial(self.dataStorage["RoboticsEngine"].getInternalLog, params[1]),
				"RoboticsEngine.pushInternalLog": partial(self.dataStorage["RoboticsEngine"].pushInternalLog, params[1])
			}

			executeCommand = interactionExecution[command]
			executeData = executeCommand()
		except Exception as e:
			logMessage = "Failure To Execute Command" + str(data)
			self.debugLogger.log("Debug", self.type, logMessage)
			return False

		logMessage = "Pipe Command Executed: " + str(data)
		self.debugLogger.log("Debug", self.type, logMessage)

		return executeData

# ||=======================================================================||

	def updateCurrentDuty(self, duty):
		self.duty = duty

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
				"Debug": self.debug
			}
		}
		
# ||=======================================================================||

	def syncEngineData(self):
		while (1):
			# for i in range(len(self.childPipes)):
			# 	curPipe = self.childPipes[i]
			# 	# print(self.useCache[curPipe[0]])
			# 	if (self.useCache[curPipe[0]]):
			# 		command = ["jsonify"]
			# 		currentData = self.pipeCommand(command, curPipe[1])
			# 		# print(currentData)
			# 		self.dataStorage[curPipe[0]].setLiveData(currentData)

			# 	logMessage = curPipe[0] + " Data Successfully Synced"
			# 	self.debugLogger.log("Debug", self.type, logMessage)

			sleep(1)

			logMessage = "Engine Data Successfully Synced"
			self.debugLogger.log("Debug", self.type, logMessage)

# ||=======================================================================||