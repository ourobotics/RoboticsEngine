# ||=======================================================================||
# ||
# ||  File:          	NetworkClientModule.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Last Date:        5 March 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Tools
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
from NetworkClient import NetworkClient
from ControllerDataSync import ControllerDataSync
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
# ||=======================||
# Notes
#
# ||=======================||
# Global Variables

# ||=======================||
# ||==============================================================================||

class NetworkClientModule(NetworkClient):
	def __init__(self):
		self.type = "NetworkClient"

		# ||=======================||
		# Program Classes
		self.networkClient = NetworkClient()
		self.controllerDataSync = ControllerDataSync(self.networkClient)

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

# ||=======================================================================||

	def createProcess(self):
		logMessage = "Process Started"
		self.debugLogger.log("Standard", self.type, logMessage)

		# ||=======================||
		self.communicationThread = Thread(target = self.networkClient.communicationModule)
		self.communicationThread.setDaemon(True)
		self.communicationThread.start()
		
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
				# logMessage = "Running"
				# self.debugLogger.log("Standard", self.type, logMessage)
				# sleep(10)
				continue
		except KeyboardInterrupt as e:
			logMessage = "Process Joined"
			self.debugLogger.log("Standard", self.type, logMessage)
			return 0
		return 0

# ||=======================================================================||