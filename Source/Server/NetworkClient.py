# ||===============================================================||
# ||
# ||  File:          	NetworkSniffer.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Last Date:        21 November 2018 | Logan Wilkovich
# ||===============================================================||
# ||=======================||
# Import Modules
from time import time, sleep
import socket
from socket import timeout
from socket import error
from socket import create_connection
import traceback
import pickle
from ConfigLoader import ConfigLoader
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
		print(self.config)

		self.active = False
		self.debug = self.config["Debug"]
		self.host = self.config[self.checkDebug() + "Address"]
		self.port = self.config[self.checkDebug() + "Port"]
		self.connectionStatus = False
		self.connectionHolder = socket.socket()
		self.socketTimeout = 1

	# @classmethod
	def loadConfig(self, configName):
		configLoader = ConfigLoader()
		config = configLoader.getConfig(configName)
		return config

	def checkDebug(self):
		if (self.debug == True):
			return "Debug"
		return ""

	# @classmethod
	def jsonify(self, message = "Null", time = -1, function = "jsonify"):
		return {
			"Generic Information": {
				"_Class": self.type,
				"_Function": function,
				"Return Status": True,
				"Activity": self.active,
				"Message": message,
				"Time": time
			},
			"Specific Information": {
				"Host": self.host,
				"Port": self.port,
				"Connection Status": self.connectionStatus,
				"Timeout": self.socketTimeout
			}
		}

	# //=======================//
	# Handles ini establishing Conection
	# @classmethod
	def establishConnection(self):
		self.active = True
		WATCH = time()
		# command = "#00000 - Requesting Connection Creation"
		command = ("#00000", "Requesting Connection Creation")
		while (self.active == True):
			try:
				self.connectionHolder = create_connection((self.host, self.port))
				print("Connection Successful")
				self.connectionStatus = True
				self.connectionHolder.send(str(command).encode())
				recieveddata = self.connectionHolder.recv(1024).decode()
				
				if (recieveddata != "Echo - Connection Successful"):
					raise Exception("Request: (" + command + ") Failed")

				while ((self.connectionStatus == True) and (self.active == True)):
					self.pingServer()
					sleep(1)
			except Exception as e:
				print("Attempting To Establish Connection")

	# @classmethod
	def pingServer(self):
		command = ("#00001", "Requesting Connection Time Test")
		if (self.connectionStatus == True):
			print("Pinging Server")
			try:
				self.connectionHolder.send(str(command).encode())
				recieveddata = self.connectionHolder.recv(1024).decode()
				print(recieveddata)
			except Exception as e:
				print(e)
				self.connectionStatus = False
				self.establishConnection()
				return self.jsonify(
					"Failure To Ping The Server.",
					-1, 
					"pingServer"
				)

	# @classmethod
	def isOnline(self):
		if ((self.connectionStatus == True) and (self.active == True)):
			return True
		else:
			return False

	# @classmethod
	def sendJson(self, code, json):
		command = (code, pickle.dumps(json))
		if (self.connectionStatus == True):
			print("Sending Json Data: " + str(code))
			try:
				self.connectionHolder.send(str(command).encode())
			except Exception as e:
				return self.jsonify(
					"Failure Send Json Data",
					-1, 
					"sendJson"
				)

	# @classmethod
	def closeConnection(self):
		WATCH = time()
		# command = "#99999 - Requesting Connection Closure"
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
				return {	
					"Status": True,
					"_Class": self.type,
					"Message": "Connection Close",
					"Time": (time() - WATCH)
				}
			except Exception as e:
				return {	
					"Status": False,
					"Error": e,
					"_Class": self.type,
					"Message": "Connection Closure - Fail",
					"Time": (time() - WATCH)
				}