# ||===============================================================||
# ||
# ||  Program/File:     RoboticsEngine.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    21 November 2018 | Logan Wilkovich
# ||===============================================================||
# ||============================================================================||
# ||=======================||
# Routes
from Library.RouteExtension import RouteExtension
# Controllers
from DataSyncController import DataSyncController
from EngineDataController import EngineDataController
from GpsController import GpsController
from ThermoController import ThermoController
from EnergyController import EnergyController
# Server
from NetworkClient import NetworkClient
# Tools
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Test
# Cache
# Premades
from multiprocessing import Process, Pipe
from threading import Thread
from time import sleep, time, strftime, localtime
import traceback
import os
import ast
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# ||============================================================================||

class RoboticsEngine(object):
	def __init__(self):
		self.type = "RoboticsEngine"

		self.active = False

		# ||=======================||
		# Program Config Varaibles
		self.useNetworkClient = True
		self.useDataSyncController = True
		self.useEngineDataController = True

		# ||=======================||
		# Program Classes
		self.networkClient = NetworkClient()
		self.dataSyncController = DataSyncController()
		self.engineDataController = EngineDataController()

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

	# |============================================================================|

	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

	# |============================================================================|

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

	# |============================================================================|

	def main(self):
		# ||=======================||
		# Pipes
		# ||=======================||
		# NetworkClient Pipes
		# NetworkClient <-> DataSyncController Pipe
		self.NC_DSC_ppipe, self.NC_DSC_cpipe = Pipe()
		# NetworkClient <-> EngineDataController Pipe
		self.NC_EDC_ppipe, self.NC_EDC_cpipe = Pipe()
		
		# ||=======================||
		# EngineDataController Pipes
		# EngineDataController <-> DataSyncController Pipe
		self.EDC_DSC_ppipe, self.EDC_DSC_cpipe = Pipe()


		# ||=======================||
		# Program Setup
		if (self.useNetworkClient):
			# ||=======================||
			# Parent Pipes
			self.networkClient.pushChildPipe(self.NC_DSC_ppipe)
			self.networkClient.pushChildPipe(self.NC_EDC_ppipe)
			# ||=======================||

			self.networkClientProcess = Process(target = self.networkClient.createProcess)
			self.networkClientProcess.daemon = True
			self.networkClientProcess.start()


			if (self.useDataSyncController):
				# ||=======================||
				# Child Pipes
				self.dataSyncController.initializeNetworkClientPipe(self.NC_DSC_cpipe)
				self.dataSyncController.initializeengineDataControllerPipe(self.EDC_DSC_cpipe)
				# ||=======================||
				
				self.dataSyncControllerProcess = Process(target = self.dataSyncController.createProcess)
				self.dataSyncControllerProcess.daemon = True
				self.dataSyncControllerProcess.start()
				
		if (self.useEngineDataController):
			# ||=======================||
			# Parent Pipes
			self.engineDataController.pushChildPipe(self.EDC_DSC_ppipe)
			# ||=======================||
			# Child Pipes
			self.engineDataController.initializeNetworkClientPipe(self.NC_EDC_cpipe)
			# ||=======================||

			self.engineDataControllerProcess = Process(target = self.engineDataController.createProcess)
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

	# |============================================================================|

if __name__ == '__main__':
	re = RoboticsEngine()
	re.main()

# |============================================================================|