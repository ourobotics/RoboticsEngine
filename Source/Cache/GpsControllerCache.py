# ||==============================================================||
# ||
# ||  Program/File:     GpsControllerCache.py
# ||
# ||  Description:      
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    27 December 2018 | Logan Wilkovich
# ||===============================================================||
# ||===============================================================||
# ||=======================||
# Routes
# Server
# Services
# Controllers
# Tools
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Test
# Data
# Premades
from time import sleep, time, strftime, localtime
# ||=======================||
# Global Variables
# ||=======================||
# Notes
# ||=======================||
# ||===============================================================||

class GpsControllerCache:
    def __init__(self):
        self.type = "EnergyControllerCache"

        # self.active = False

        # ||=======================||
        # Program Classes
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
        self.controllerCache = {
            "LiveData": None,
            "InternalLog": []
        }

    # ||=======================||
    # LiveData Helpers
    def getLiveData(self):
        return self.controllerCache["LiveData"]

    def setLiveData(self, data):
        self.GpsConcontrollerCachetroller["LiveData"] = data

    # ||=======================||
    # InteralLog Helpers
    def pushInternalLog(self, data):
        self.controllerCache["InternalLog"].append(data)

    def getInternalLog(self, i):
        if (i == None):
            return self.controllerCache["InternalLog"]
        else:
            return self.controllerCache["InternalLog"][int(i)]