# ||=======================================================================||
# ||
# ||  File:          	NetworkClient.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Last Date:        21 November 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Library
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Library/Controllers
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

class NetworkClient:
	def __init__(self):
		self.type = "NetworkClient"

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
		# Config <bool>
		self.debug = self.config["Debug"]
		self.log = self.config["Log"]

		# ||=======================||
		# Config <string>
		self.host = self.config["Address"]
		self.port = self.config["Port"]

		# ||=======================||
		# Defaults
		self.duty = "Inactive"
		self.connectionStatus = False
		self.connectionHolder = socket.socket()
		self.socketTimeout = 1
		self.parentPipes = []

		# ||=======================||
		# Inheritance
		

# ||=======================================================================||

	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

# ||=======================================================================||

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

# ||=======================================================================||

	def pushParentPipe(self, pipe):
		self.parentPipes.append(pipe)	

# ||=======================================================================||

	def communicationModule(self):
		while (1):
			if (len(self.parentPipes) != 0):
				dataRecv = None
				while (dataRecv == None):
					for i in range(len(self.parentPipes)):
						pipe = self.parentPipes[i]
						# print("Pipe:",i)
						try:
							if (pipe.poll(0.5)):
								dataRecv = pipe.recv() * 3
								break
						except Exception as e:
							print(e)

				logMessage = "Reading From Pipe: " + str(dataRecv)
				self.debugLogger.log("Debug", self.type, logMessage)

				interactionAccess = {
					"pingServer": partial(self.pingServer),
					"jsonify": partial(self.jsonify),
					"sendJson": partial(self.sendJson, dataRecv[1], dataRecv[2]),
					"closeConnection": partial(self.closeConnection),
					"updateDuty": partial(self.updateCurrentDuty, dataRecv[1]),
					"isOnline": partial(self.isOnline)
				}
				returnData = interactionAccess[dataRecv[0]]()
				# print(returnData)

				logMessage = "Executing Pipe Command: " + str([dataRecv[0]])
				self.debugLogger.log("Debug", self.type, logMessage)

				pipe.send(returnData)

# ||=======================================================================||

	def establishConnection(self):
		self.active = True
		WATCH = time()
		command = ("#00000", "Requesting Connection Creation")
		while (self.active == True):
			try:
				self.connectionHolder = create_connection((self.host, self.port))
				logMessage = "Connection Successful"
				self.debugLogger.log("Standard", self.type, logMessage)
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
				self.debugLogger.log("Warning", self.type, logMessage)
				sleep(5)
		return 0

# ||=======================================================================||

	def pingServer(self):
		command = ("#00001", "Requesting Connection Time Test")
		if (self.connectionStatus == True):
			logMessage = "Pinging Server"
			self.debugLogger.log("Standard", self.type, logMessage)
			try:
				self.connectionHolder.send(str(command).encode())
				recieveddata = self.connectionHolder.recv(1024).decode()
				logMessage = recieveddata
				self.debugLogger.log("Standard", self.type, logMessage)
			except Exception as e:
				logMessage = e
				self.debugLogger.log("Error", self.type, str(logMessage))
				self.connectionStatus = False
				self.establishConnection()
				return self.jsonify(
					"Failure To Ping The Server.",
					str(strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())), 
					"pingServer"
				)
		return 0

# ||=======================================================================||

	def isOnline(self):
		if ((self.connectionStatus == True) and (self.active == True)):
			return True
		else:
			return False

# ||=======================================================================||

	def sendJson(self, code, json):
		command = (code, pickle.dumps(json))
		if (self.connectionStatus == True):
			logMessage = "Sending Json Data: " + str(code) + " " + str(json)
			self.debugLogger.log("Standard", self.type, logMessage)
			try:
				self.connectionHolder.send(str(command).encode())
			except Exception as e:
				return self.jsonify(
					"Failure Send Json Data",
					str(strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())), 
					"sendJson"
				)
		return 0

# ||=======================================================================||

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
					"closeConnection"
				)
			except Exception as e:
				return self.jsonify(
					"Connection Closure - Fail",
					str(strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())), 
					"closeConnection"
				)
		return 0

# ||=======================================================================||