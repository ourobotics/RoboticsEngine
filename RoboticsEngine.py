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
# Test
# Cache
from EngineData import EngineData
# Premades
from time import sleep, time, strftime, localtime
from threading import Thread
import traceback
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# ||============================================================================||

class RoboticsEngine(object):
    def __init__(self):
        # ||=======================||
        # Program Config Varaibles
        self.useNetworkClient = True
        self.useGpsController = True
        self.useThermoController = True
        self.useEnergyController = True
        self.useDataSyncController = True

        # ||=======================||
		# Program Classes
        # self.networkClient = NetworkClient()
        # self.gpsController = GpsController()

    def main(self):
        # ||=======================||
		# Program Setup
        if (self.useNetworkClient):
            self.networkClientThread = Thread(target =  NetworkClient.establishConnection)
            self.networkClientThread.setDaemon(True)
            self.networkClientThread.start()
        if (self.useDataSyncController):
            self.dataSyncControllerThread = Thread(target = DataSyncController.syncLiveData)
            self.dataSyncControllerThread.setDaemon(True)
            self.dataSyncControllerThread.start()
        if (self.useGpsController):
            self.gpsControllerThread = Thread(target = GpsController.testMovement)
            self.gpsControllerThread.setDaemon(True)
            self.gpsControllerThread.start()
        if (self.useThermoController):
            self.thermoControllerThread = Thread(target = ThermoController.testTemperature)
            self.thermoControllerThread.setDaemon(True)
            self.thermoControllerThread.start()
        if (self.useEnergyController):
            self.energyControllerThread = Thread(target = EnergyController.testEnergy)
            self.energyControllerThread.setDaemon(True)
            self.energyControllerThread.start()
            
        try:
            while True:
                if (self.useGpsController):
                    gpsControllerData = GpsController.jsonify(
                        "Requesting Current Cache", 
                        str(strftime("%Y-%m-%d %H:%M:%S", localtime())))
                    EngineData.GpsController.setLiveData(gpsControllerData) 
                        
                if (self.useThermoController):
                    thermoControllerData = ThermoController.jsonify(
                        "Requesting Current Cache", 
                        str(strftime("%Y-%m-%d %H:%M:%S", localtime())))
                    EngineData.ThermoController.setLiveData(thermoControllerData)
                
                if(self.useEnergyController):
                    energyControllerData = EnergyController.jsonify(
                        "Requesting Current Cache", 
                        str(strftime("%Y-%m-%d %H:%M:%S", localtime())))
                    EngineData.EnergyController.setLiveData(energyControllerData)


        except KeyboardInterrupt as e:
            NetworkClient.closeConnection()
            # print(str(traceback.format_exc()))
            return

re = RoboticsEngine()
re.main()