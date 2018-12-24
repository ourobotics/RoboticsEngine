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
from time import time
import socket
from socket import timeout
from socket import error
from socket import create_connection
import traceback
# ||=======================||
# Notes
#
# ||=======================||
# Global Variables

# ||=======================||
# ||==============================================================================||

class NetworkClient(object):
	def __init__(self):
		self.active = False
		self.type = "NetworkSniffer"
		self.host = "localhost"
		self.port = 1024
		self.connectionStatus = False
		self.connectionHolder = socket.socket()

	# //=======================//
	# Handles ini establishing Conection
	def establishConnection(self):
		self.active = True
		WATCH = time()
		command = "#00000 - Requesting Connection Creation"
		while True:
			try:
				self.connectionHolder = create_connection((self.host, self.port))
				self.connectionStatus = True
				self.connectionHolder.send(str(command).encode())
				recieveddata = self.connectionHolder.recv(1024).decode()
				if (recieveddata != "Success"):
					raise Exception("Request: (" + command + ") Failed")
				return {	
					"Status": True,
					"_Class": self.type,
					"Message": "Connection Created",
					"Time": (time() - WATCH)
				}
			except Exception as e:
				self.port += 1
				return {	
					"Status": False,
					"Error": e,
					"_Class": self.type,
					"Message": "Connection Creation - Fail",
					"Time": (time() - WATCH)
				}

	def pingServer(self):
		command = "#00001 - Requesting Connection Time Test"
		self.connectionHolder.send(str(command).encode())
		recieveddata = self.connectionHolder.recv(1024).decode()
		print(recieveddata)

	def closeConnection(self):
		WATCH = time()
		command = "#99999 - Requesting Connection Closure"
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