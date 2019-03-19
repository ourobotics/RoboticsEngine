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
		self.parentPipes = []

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
			if (len(self.parentPipes) != 0):
				dataRecv = None
				while (dataRecv == None):
					for i in range(len(self.parentPipes)):
						pipe = self.parentPipes[i]
						try:
							if (pipe.poll(0.5)):
								dataRecv = pipe.recv() * 3
								break
						except Exception as e:
							print(e)

				logMessage = "Reading From Pipe: " + str(dataRecv)
				self.debugLogger.log("Debug", self.type, logMessage)

				interactionAccess = {
					"jsonify": partial(self.jsonify)
				}
				returnData = interactionAccess[dataRecv[0]]()
				# print(returnData)

				logMessage = "Executing Pipe Command: " + str([dataRecv[0]])
				self.debugLogger.log("Debug", self.type, logMessage)

				pipe.send(returnData)

# ||=======================================================================||

	def main(self):
		logMessage = "Process Started"
		self.debugLogger.log("Standard", self.type, logMessage)

		# ||=======================||
		# Pipes
		# ||=======================||
		# NetworkClient Pipes
		# NetworkClient <- ControllerDataSync Pipe
		self.NC_DSC_ppipe, self.NC_DSC_cpipe = Pipe()
		# NetworkClient <- EngineDataController Pipe
		self.NC_EDC_ppipe, self.NC_EDC_cpipe = Pipe()
		
		# ||=======================||
		# EngineDataController Pipes
		# EngineDataController <- ControllerDataSync Pipe
		self.EDC_DSC_ppipe, self.EDC_DSC_cpipe = Pipe()

		# ||=======================||
		# RoboticsEngine Pipes
		# RoboticsEngine <- EngineDataController
		self.MRE_EDC_ppipe, self.MRE_EDC_cpipe = Pipe()
		self.parentPipes.append(self.MRE_EDC_ppipe)


		# ||=======================||
		# Program Setup
		if (self.useNetworkClient):
			# ||=======================||
			# Parent Pipes
			self.networkClientModule.networkClient.pushParentPipe(self.NC_DSC_ppipe)
			self.networkClientModule.networkClient.pushParentPipe(self.NC_EDC_ppipe)
			# ||=======================||
			# Child Pipes
			self.networkClientModule.controllerDataSync.pushChildPipe("EngineDataController", self.EDC_DSC_cpipe)

			self.networkClientProcess = Process(target = self.networkClientModule.createProcess)
			self.networkClientProcess.daemon = True
			self.networkClientProcess.start()
				
		if (self.useEngineDataController):
			# ||=======================||
			# Parent Pipes
			self.engineDataModule.engineDataController.pushParentPipe(self.EDC_DSC_ppipe)
			# ||=======================||
			# Child Pipes
			self.engineDataModule.engineDataController.pushChildPipe("NetworkClient",  self.NC_EDC_cpipe)
			self.engineDataModule.engineDataController.pushChildPipe("RoboticsEngine", self.MRE_EDC_cpipe)
			# ||=======================||

			self.engineDataControllerProcess = Process(target = self.engineDataModule.createProcess)
			self.engineDataControllerProcess.daemon = True
			self.engineDataControllerProcess.start()
		
		# ||=======================||

		self.communicationThread = Thread(target = self.communicationModule)
		self.communicationThread.setDaemon(True)
		self.communicationThread.start()

		logMessage = "communicationThread Started"
		self.debugLogger.log("Standard", self.type, logMessage)

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