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
from System.Routes import Routes
# Controllers
from DataSyncController import DataSyncController
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
from EngineData import EngineData
# Premades
from time import sleep, time, strftime, localtime
from threading import Thread
import traceback
import os
from multiprocessing import Process, Pipe
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

		self.config = self.loadConfig(self.type)

		self.active = False

		# ||=======================||
		# Program Config Varaibles
		self.useNetworkClient = True

		# ||=======================||
		# Program Classes
		self.networkClient = NetworkClient()

		# ||=======================||
		# Config <bool>
		self.debug = self.config["Debug"]
		self.log = self.config["Log"]

		# ||=======================||
		# Defaults
		self.debugLogger = DebugLogger(self.type)
		self.debugLogger.setMessageSettings(
			ast.literal_eval(self.config["Standard"]),
			ast.literal_eval(self.config["Warning"]),
			ast.literal_eval(self.config["Error"]))

	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|

	def loadConfig(self, configName):
		configLoader = ConfigLoader()
		config = configLoader.getConfig(configName)
		return config

	# |============================================================================|

	def checkDebug(self):
		if (self.debug == True):
			return "Debug"
		return ""

	# |============================================================================|

	def updateCurrentDutyLog(self, duty, function = "updateCurrentDutyLog"):
		self.duty = duty
		DeviceData.NetworkServer.pushInternalLog(self.jsonify(
			"Duty Update: " + self.duty,
			str(strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())),
			function)
		)
		return 0

	# |============================================================================|

	def updateCurrentDuty(self, duty):
		self.duty = duty
		return 0

	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|
	# |============================================================================|


	def main(self):
		# ||=======================||
		# Program Setup
		if (self.useNetworkClient):
			self.networkClientProcessPPipe, self.networkClientProcessCPipe = Pipe()
			self.networkClientProcess = Process(target = self.networkClient.createProcess, args=(self.networkClientProcessCPipe,))
			self.networkClientProcess.daemon = True
			self.networkClientProcess.start()
		
		
		try:
			while(1):
				# logMessage = "Running"
				# self.debugLogger.log("Standard", logMessage)
				self.networkClientProcessPPipe.send(["jsonify"])
				# print(self.networkClientProcessPPipe.recv())
				sleep(10)
				# continue
		except KeyboardInterrupt as e:
			if (self.useNetworkClient):
				# self.networkClient.closeConnection()
				logMessage = "Joined"
				self.debugLogger.log("Standard", self.type + ': ' + logMessage)
				self.networkClientProcess.join()
			return

	# |============================================================================|

if __name__ == '__main__':
	re = RoboticsEngine()
	re.main()

# |============================================================================|