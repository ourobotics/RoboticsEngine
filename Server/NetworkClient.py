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
# ||=======================||
# Notes
#
# ||=======================||
# Global Variables

# ||=======================||
# ||==============================================================================||

class NetworkClient:
	# def __init__(cls):
	active = False
	type = "NetworkClient"
	host = "localhost"
	port = 1024
	connectionStatus = False
	connectionHolder = socket.socket()
	socketTimeout = 1

	@classmethod
	def jsonify(cls, message = "Null", time = -1, function = "jsonify"):
		return {
			"Generic Information": {
				"_Class": cls.type,
				"_Function": function,
				"Return Status": True,
				"Activity": cls.active,
				"Message": message,
				"Time": time
			},
			"Specific Information": {
				"Host": cls.host,
				"Port": cls.port,
				"Connection Status": cls.connectionStatus,
				"Timeout": cls.socketTimeout
			}
		}

	# //=======================//
	# Handles ini establishing Conection
	@classmethod
	def establishConnection(cls):
		cls.active = True
		WATCH = time()
		# command = "#00000 - Requesting Connection Creation"
		command = ("#00000", "Requesting Connection Creation")
		while (cls.active == True):
			try:
				cls.connectionHolder = create_connection((cls.host, cls.port))
				print("Connection Successful")
				cls.connectionStatus = True
				cls.connectionHolder.send(str(command).encode())
				recieveddata = cls.connectionHolder.recv(1024).decode()
				
				if (recieveddata != "Echo - Connection Successful"):
					raise Exception("Request: (" + command + ") Failed")

				while ((cls.connectionStatus == True) and (cls.active == True)):
					cls.pingServer()
					sleep(1)
			except Exception as e:
				print("Attempting To Establish Connection")

	@classmethod
	def pingServer(cls):
		command = ("#00001", "Requesting Connection Time Test")
		if (cls.connectionStatus == True):
			print("Pinging Server")
			try:
				cls.connectionHolder.send(str(command).encode())
				recieveddata = cls.connectionHolder.recv(1024).decode()
				print(recieveddata)
			except Exception as e:
				print(e)
				cls.connectionStatus = False
				cls.establishConnection()
				return cls.jsonify(
					"Failure To Ping The Server.",
					-1, 
					"pingServer"
				)

	@classmethod
	def isOnline(cls):
		if ((cls.connectionStatus == True) and (cls.active == True)):
			return True
		else:
			return False

	@classmethod
	def sendJson(cls, code, json):
		command = (code, pickle.dumps(json))
		if (cls.connectionStatus == True):
			print("Sending Json Data: " + str(code))
			try:
				cls.connectionHolder.send(str(command).encode())
			except Exception as e:
				return cls.jsonify(
					"Failure Send Json Data",
					-1, 
					"sendJson"
				)

	@classmethod
	def closeConnection(cls):
		WATCH = time()
		# command = "#99999 - Requesting Connection Closure"
		command = ("#99999", "Requesting Connection Closure")
		if (cls.active and cls.connectionStatus):
			try:
				cls.connectionHolder.send(str(command).encode())
				recieveddata = cls.connectionHolder.recv(1024).decode()
				if (recieveddata != "Success"):
					raise Exception("Request: (" + command + ") Failed")
				cls.active = False
				cls.connectionStatus = False
				cls.connectionHolder.close()
				return {	
					"Status": True,
					"_Class": cls.type,
					"Message": "Connection Close",
					"Time": (time() - WATCH)
				}
			except Exception as e:
				return {	
					"Status": False,
					"Error": e,
					"_Class": cls.type,
					"Message": "Connection Closure - Fail",
					"Time": (time() - WATCH)
				}