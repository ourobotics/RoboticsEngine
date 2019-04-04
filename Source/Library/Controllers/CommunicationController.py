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
		self.type = _class + ".CommunicationController"

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
		self.pipes = {}
		self.connectionList = {}

	def updatePipes(self, newPipes):
		# print("test")
		# print(self.pipes)
		self.pipes = {**self.pipes, **newPipes}
		# print(newPipes)

	def updateConnectionList(self, newConnection):
		self.connectionList[newConnection[0]] = newConnection[1]

	def requestSubscription(self, command):
		self.pipes["RoboticsEngine"].send(["subscribe", "EngineDataModule", "NetworkClientModule"])
		# print("t: ",self.pipes["RoboticsEngine"].recv()) 

	def runAPI(self):
		while (1):
			if (len(self.pipes) != 0):
				dataRecv = None
				while (dataRecv == None):
					for i in range(len(self.pipes)):
						pipe = list(self.pipes.values())[i]
						# print("Pipe:",i)
						try:
							if (pipe.poll(0.5)):
								logMessage = "Reading From Pipe"
								self.debugLogger.log("Debug", self.type, logMessage)
								dataRecv = pipe.recv()
						except Exception as e:
							print(e)
				if ((dataRecv != True) and (dataRecv != False)):
					# print(dataRecv)
					logMessage = "Attempting To Execute Command"
					self.debugLogger.log("Debug", self.type, logMessage)

					commandTemplate = dataRecv[0].split('.')
					controllerName = commandTemplate[0]
					command = ['.'.join(commandTemplate[1:])]

					returnedData = False
					if ((controllerName == "CommunicationController") and (command[0] == "updatePipes")):
						param = dataRecv[1]
						self.updatePipes(param)
						returnedData = True
					else:
						returnedData = self.connectionList[controllerName].APICommand(command)
					
					logMessage = "Piping Returned Data Back: " + str([dataRecv[0]])
					self.debugLogger.log("Debug", self.type, logMessage)

					pipe.send(returnedData)
