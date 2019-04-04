# ||=======================================================================||
# ||
# ||  Program/File:     MultiRoboticsEngine.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    21 November 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Routes
from Library.Utils.RouteExtension import RouteExtension
# Library
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Library/Modules
from NetworkClientModule import NetworkClientModule
from EngineDataModule import EngineDataModule
# Premades
from multiprocessing import Process, Pipe
from threading import Thread
from time import sleep, time, strftime, localtime
from functools import partial
import traceback
import os
import ast
import sys
import psutil
import os
# ||=======================||
# Global Variables
process = psutil.Process(os.getpid())
# ||=======================||
# Notes

# ||=======================||
# ||=======================================================================||

class RoboticsEngine(object):
	def __init__(self):
		self.type = "RoboticsEngine"

		self.active = False

		# ||=======================||
		# Program Config Varaibles
		self.useNetworkClient = True
		self.useControllerDataSync = True
		self.useEngineDataController = True

		# ||=======================||
		# Program Classes
		self.networkClientModule = NetworkClientModule()
		self.engineDataModule = EngineDataModule()

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
		# Defaults
		self.duty = "Inactive"
		self.pipes = {}
		self.subscriptions = {}

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
				"useNetworkClient": self.useNetworkClient,
				"useControllerDataSync": self.useControllerDataSync,
				"useEngineDataController": self.useEngineDataController,
				"Memory Size": self.processMemorySize
			}
		}

# ||=======================================================================||

	def updateProcessMemorySize(self):
		self.processMemorySize = int(int(process.memory_info().rss) / 1000000)

# ||=======================================================================||

	def communicationModule(self):
		while (1):
			if (len(self.pipes) != 0):
				dataRecv = None
				while (dataRecv == None):
					for i in range(len(self.pipes)):
						pipe = list(self.pipes.values())[i][0]
						# print(pipe)
						# print("Pipe:",i)
						try:
							if (pipe.poll(0.5)):
								dataRecv = pipe.recv() * 3
								break
						except Exception as e:
							print(e)

				logMessage = "Reading From Pipe: " + str(dataRecv)
				self.debugLogger.log("Debug", self.type, logMessage)
				# print(dataRecv)
				interactionAccess = {
					"jsonify": partial(self.jsonify),
					"subscribe": partial(self.subscribe, dataRecv[1], dataRecv[2])
				}
				returnData = interactionAccess[dataRecv[0]]()
				# print(returnData)

				logMessage = "Executing Pipe Command: " + str([dataRecv[0]])
				self.debugLogger.log("Debug", self.type, logMessage)
				
				pipe.send(returnData)

# ||=======================================================================||

	def subscribe(self, originalModule, otherModule):
		pipe1, pipe2 = Pipe()
		self.subscriptions[originalModule] = {
			otherModule: pipe1
		}
		self.subscriptions[otherModule] = {
			originalModule: pipe2
		}
		self.pipes[originalModule][0].send(["CommunicationController.updatePipes", {otherModule: pipe1}])
		self.pipes[originalModule][0].recv()
		self.pipes[otherModule][0].send(["CommunicationController.updatePipes", {originalModule: pipe2}])
		self.pipes[otherModule][0].recv()
		return True

# ||=======================================================================||

	def main(self):
		logMessage = "Process Started"
		self.debugLogger.log("Standard", self.type, logMessage)

		# ||=======================||
		# Pipes


		# ||=======================||
		# Program Setup
		if (self.useNetworkClient):
			# ||=======================||
			# Pipes
			self.pipes["NetworkClientModule"] = Pipe()
			self.networkClientModule.updatePipes("RoboticsEngine", self.pipes["NetworkClientModule"][1])

			# ||=======================||

			self.networkClientProcess = Process(target = self.networkClientModule.createProcess)
			self.networkClientProcess.daemon = True
			self.networkClientProcess.start()
				
			# self.pipes["NetworkClientModule"][0].send(["NetworkClient.isOnline"])
			# print(self.pipes["NetworkClientModule"][0].recv())

		if (self.useEngineDataController):
			# ||=======================||
			# Pipes
			self.pipes["EngineDataModule"] = Pipe()
			self.engineDataModule.updatePipes("RoboticsEngine", self.pipes["EngineDataModule"][1])

			# ||=======================||

			self.engineDataControllerProcess = Process(target = self.engineDataModule.createProcess)
			self.engineDataControllerProcess.daemon = True
			self.engineDataControllerProcess.start()

			# self.pipes["EngineDataModule"][0].send(["EngineDataController.NetworkClient.getLiveData"])
			# print(self.pipes["EngineDataModule"][0].recv())
		
		# ||=======================||

		self.communicationThread = Thread(target = self.communicationModule)
		self.communicationThread.setDaemon(True)
		self.communicationThread.start()

		logMessage = "communicationThread Started"
		self.debugLogger.log("Standard", self.type, logMessage)

		# self.subscribe("test1", "test2")
		# print(self.subscriptions)

		try:
			while(1):
				self.updateProcessMemorySize()
				logMessage = "Current Size In Megabytes: " + str(self.processMemorySize)
				self.debugLogger.log("Debug", self.type, logMessage)
				sleep(10)
		except KeyboardInterrupt as e:
			print('\r', end='')
			logMessage = "Process Joined"
			self.debugLogger.log("Standard", self.type, logMessage)
			return

# ||=======================================================================||

if __name__ == '__main__':
	re = RoboticsEngine()
	re.main()

# ||=======================================================================||