# ||=======================================================================||
# ||
# ||  File:          	NetworkClientModule.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:	5 March 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Library
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Library/Network
from NetworkClient import NetworkClient
# Library/Controllers
from ControllerDataSync import ControllerDataSync
from CommunicationController import CommunicationController
# Import Modules
from time import sleep, time, strftime, localtime
from socket import timeout
from socket import error
from socket import create_connection
from threading import Thread
from functools import partial
import socket
import traceback
import pickle
import ast
import sys
import psutil
import os
# ||=======================||
# Notes
process = psutil.Process(os.getpid())
# ||=======================||
# Global Variables

# ||=======================||
# ||==============================================================================||

class NetworkClientModule(NetworkClient):
	def __init__(self):
		self.type = "NetworkClientModule"

		# ||=======================||
		# Program Classes
		self.networkClient = NetworkClient()
		self.controllerDataSync = ControllerDataSync(self.networkClient)
		self.communicationController = CommunicationController(self.type)

		# ||=======================||

		configLoader = ConfigLoader()
		self.config = configLoader.getConfig(self.type)

		# ||=======================||

		self.debugLogger = DebugLogger(self.type)
		self.debugLogger.setMessageSettings(
			ast.literal_eval(self.config["Debug"]),
			ast.literal_eval(self.config["Standard"]),
			ast.literal_eval(self.config["Warning"]),
			ast.literal_eval(self.config["Error"]))

		# ||=======================||
		# Defaults
		self.pipes = {}

# ||=======================================================================||

	def updateProcessMemorySize(self):
		self.processMemorySize = int(int(process.memory_info().rss) / 1000000)

# ||=======================================================================||

	def updatePipes(self, type, pipe):
		self.pipes[type] = pipe

# ||=======================================================================||

	def createProcess(self):
		logMessage = "Process Started"
		self.debugLogger.log("Standard", self.type, logMessage)

		# ||=======================||
		# CommunicationController
		self.communicationController.updateConnectionList(("NetworkClient", self.networkClient))
		self.communicationController.updateConnectionList(("ControllerDataSync", self.controllerDataSync))
		self.communicationController.updatePipes(self.pipes)

		self.communicationControllerThread = Thread(target = self.communicationController.runAPI)
		self.communicationControllerThread.setDaemon(True)
		self.communicationControllerThread.start()

		logMessage = "communicationThread Started"
		self.debugLogger.log("Standard", self.type, logMessage)

		# ||=======================||
		self.connectionThread = Thread(target = self.networkClient.establishConnection)
		self.connectionThread.setDaemon(True)
		self.connectionThread.start()

		logMessage = "connectionThread Started"
		self.debugLogger.log("Standard", self.type, logMessage)

		# ||=======================||

		self.syncLiveDataThread = Thread(target = self.controllerDataSync.syncLiveData)
		self.syncLiveDataThread.setDaemon(True)
		self.syncLiveDataThread.start()

		logMessage = "syncLiveDataThread Started"
		self.debugLogger.log("Standard", self.type, logMessage)
		
		# ||=======================||
		
		try:
			while (1):
				self.updateProcessMemorySize()
				logMessage = "Current Size In Megabytes: " + str(self.processMemorySize)
				self.debugLogger.log("Debug", self.type, logMessage)
				sleep(10)
		except KeyboardInterrupt as e:
			print('\r', end='')
			logMessage = "Process Joined"
			self.debugLogger.log("Standard", self.type, logMessage)
			return 0
		return 0

# ||=======================================================================||