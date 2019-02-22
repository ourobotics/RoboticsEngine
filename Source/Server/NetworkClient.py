# ||===============================================================||
# ||
# ||  File:          	NetworkClient.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Last Date:        21 November 2018 | Logan Wilkovich
# ||===============================================================||
# ||=======================||
# Tools
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Import Modules
from time import time, sleep
import socket
from socket import timeout
from socket import error
from socket import create_connection
import traceback
import pickle
import ast
from threading import Thread
# ||=======================||
# Notes
#
# ||=======================||
# Global Variables

# ||=======================||
# ||==============================================================================||

class NetworkClient:
	def __init__(self):
		self.type = "NetworkClient"
		
		self.config = self.loadConfig(self.type)

		self.active = False

		# ||=======================||
		# Config <bool>
		self.debug = self.config["Debug"]
		self.log = self.config["Log"]

		# ||=======================||
		# Config <string>
		self.host = self.config[self.checkDebug() + "Address"]
		self.port = self.config[self.checkDebug() + "Port"]

		# ||=======================||
		# Defaults
		self.duty = "Inactive"
		self.connectionStatus = False
		self.connectionHolder = socket.socket()
		self.socketTimeout = 1

		self.debugLogger = DebugLogger(self.type)
		self.debugLogger.setMessageSettings(
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
				"Host": self.host,
				"Port": self.port,
				"Connection Status": self.connectionStatus,
				"Timeout": self.socketTimeout,
				"Debug": self.debug
			}
		}

	# |============================================================================|

	def communicationModule(self, comPipe):
		while (1):
			dataRecv = comPipe.recv() * 3

			logMessage = "Reading From Pipe"
			self.debugLogger.log("Standard", self.type + ': ' + logMessage)

			interactionAccess = {
				"pingServer": self.pingServer(),
				"jsonify": self.jsonify(),
				"reLoadConfig": self.loadConfig(self.type),
				"sendJson": self.sendJson(dataRecv[1], dataRecv[2]),
				"closeConnection": self.closeConnection(),
				"updateDuty": self.updateCurrentDuty(dataRecv[1])
			}
			returnData = interactionAccess[dataRecv[0]]

			logMessage = "Executing Pipe Command"
			self.debugLogger.log("Standard", self.type + ': ' + logMessage)

			comPipe.send(returnData)

	# |============================================================================|

	def createProcess(self, comPipe):
		# ||=======================||
		self.communicationThread = Thread(target = self.communicationModule, args=(comPipe,))
		self.communicationThread.setDaemon(True)
		self.communicationThread.start()
		
		logMessage = "communicationThread Started"
		self.debugLogger.log("Standard", self.type + ': ' + logMessage)

		# ||=======================||
		self.connectionThread = Thread(target = self.establishConnection)
		self.connectionThread.setDaemon(True)
		self.connectionThread.start()

		logMessage = "connectionThread Started"
		self.debugLogger.log("Standard", self.type + ': ' + logMessage)
		
		try:
			while (1):
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

	def establishConnection(self):
		self.active = True
		WATCH = time()
		command = ("#00000", "Requesting Connection Creation")
		while (self.active == True):
			try:
				self.connectionHolder = create_connection((self.host, self.port))
				logMessage = "Connection Successful"
				self.debugLogger.log("Standard", self.type + ': ' + logMessage)
				self.connectionStatus = True
				self.connectionHolder.send(str(command).encode())
				recieveddata = self.connectionHolder.recv(1024).decode()
				
				if (recieveddata != "Echo - Connection Successful"):
					raise Exception("Request: (" + command + ") Failed")

				while ((self.connectionStatus == True) and (self.active == True)):
					# self.pingServer()
					sleep(1)
			except Exception as e:
				logMessage = "Attempting To Establish Connection"
				self.debugLogger.log("Warning", self.type + ': ' + logMessage)
		return 0

	# |============================================================================|

	def pingServer(self):
		command = ("#00001", "Requesting Connection Time Test")
		if (self.connectionStatus == True):
			logMessage = "Pinging Server"
			self.debugLogger.log("Standard", self.type + ': ' + logMessage)
			try:
				self.connectionHolder.send(str(command).encode())
				recieveddata = self.connectionHolder.recv(1024).decode()
				logMessage = recieveddata
				self.debugLogger.log("Standard", self.type + ': ' + logMessage)
			except Exception as e:
				logMessage = e
				self.debugLogger.log("Error", self.type + ': ' + logMessage)
				self.connectionStatus = False
				self.establishConnection()
				return self.jsonify(
					"Failure To Ping The Server.",
					str(strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())), 
					"pingServer"
				)
		return 0

	# |============================================================================|

	def isOnline(self):
		if ((self.connectionStatus == True) and (self.active == True)):
			return True
		else:
			return False

	# |============================================================================|

	def sendJson(self, code, json):
		command = (code, pickle.dumps(json))
		if (self.connectionStatus == True):
			logMessage = "Sending Json Data: " + str(code)
			self.debugLogger.log("Standard", self.type + ': ' + logMessage)
			try:
				self.connectionHolder.send(str(command).encode())
			except Exception as e:
				return self.jsonify(
					"Failure Send Json Data",
					str(strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())), 
					"sendJson"
				)
		return 0

	# |============================================================================|

	def closeConnection(self):
		WATCH = time()
		command = ("#99999", "Requesting Connection Closure")
		if (self.active and self.connectionStatus):
			try:
				self.connectionHolder.send(str(command).encode())
				recieveddata = self.connectionHolder.recv(1024).decode()
				if (recieveddata != "Success"):
					raise Exception("Request: (" + command + ") Failed")
				self.active = False
				self.connectionStatus = False
				self.connectionHolder.close()
				return self.jsonify(
					"Connection Close",
					str(strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())), 
					"sendJson"
				)
			except Exception as e:
				return self.jsonify(
					"Connection Closure - Fail",
					str(strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())), 
					"sendJson"
				)
		return 0

# |===============================================================|