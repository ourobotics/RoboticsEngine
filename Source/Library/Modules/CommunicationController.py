# ||=======================================================================||
# ||
# ||  Program/File:		CommunicationController.py
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

class CommunicationController():
	def __init__(self, _class):
		self.type = _class + "/CommunicationController"

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
		self.duty = "Inactive"
		self.parentPipes = []
		self.childPipes = []
		self.interactionAccess = {}

	def updateInteractionAccess(self, newAccess):
		self.interactionAccess = {**self.interactionAccess, **newAccess}

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
								print("read")
								dataRecv = pipe.recv() * 3
						except Exception as e:
							print(e)
				# print(dataRecv)

				logMessage = "Reading From Pipe"
				self.debugLogger.log("Debug", self.type, logMessage)

				# interactionAccess = {}

				returnData = interactionAccess[dataRecv[0]]

				logMessage = "Executing Pipe Command: " + str([dataRecv[0]])
				self.debugLogger.log("Debug", self.type, logMessage)

				pipe.send(returnData)