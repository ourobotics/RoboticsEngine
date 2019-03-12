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
from Library.RouteExtension import RouteExtension
# Server
from NetworkClientModule import NetworkClientModule
# Library
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Library/Modules
from EngineDataModule import EngineDataModule
# Premades
from multiprocessing import Process, Pipe
from time import sleep, time, strftime, localtime
import traceback
import os
import ast
# ||=======================||
# Global Variables

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

# ||=======================================================================||

	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

# ||=======================================================================||

	def jsonify(self, message = "Null", time = -1, function = "jsonify"):
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
			}
		}

# ||=======================================================================||

	def main(self):
		# ||=======================||
		# Pipes
		# ||=======================||
		# NetworkClient Pipes
		# NetworkClient <-> ControllerDataSync Pipe
		self.NC_DSC_ppipe, self.NC_DSC_cpipe = Pipe()
		# NetworkClient <-> EngineDataController Pipe
		self.NC_EDC_ppipe, self.NC_EDC_cpipe = Pipe()
		
		# ||=======================||
		# EngineDataController Pipes
		# EngineDataController <-> ControllerDataSync Pipe
		self.EDC_DSC_ppipe, self.EDC_DSC_cpipe = Pipe()


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
			# ||=======================||

			self.engineDataControllerProcess = Process(target = self.engineDataModule.createProcess)
			self.engineDataControllerProcess.daemon = True
			self.engineDataControllerProcess.start()
		
		
		try:
			while(1):
				# logMessage = "Running"
				# self.debugLogger.log("Standard", logMessage)
				# self.networkClientProcessppipe.send(["jsonify"])
				# print(self.networkClientProcessppipe.recv())
				sleep(10)
				# continue
		except KeyboardInterrupt as e:
			if (self.useNetworkClient):
				logMessage = "Process Joined"
				self.debugLogger.log("Standard", self.type, logMessage)
				self.networkClientProcess.join()
			return

# ||=======================================================================||

if __name__ == '__main__':
	re = RoboticsEngine()
	re.main()

# ||=======================================================================||