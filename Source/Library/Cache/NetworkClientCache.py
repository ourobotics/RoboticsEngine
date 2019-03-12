# ||==============================================================||
# ||
# ||  Program/File:     NetworkClientCache.py
# ||
# ||  Description:      
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    27 December 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Library
from ConfigLoader import ConfigLoader
from DebugLogger import DebugLogger
# Premades
from time import sleep, time, strftime, localtime
import ast
# ||=======================||
# Global Variables
# ||=======================||
# Notes
# ||=======================||
# ||=======================================================================||

class NetworkClientCache(object):

    def __init__(self):
        self.type = "NetworkClientCache"

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
        self.clientCache = {
            "LiveData": None,
            "InternalLog": []
        }

    # ||=======================||
    # LiveData Helpers
    def getLiveData(self):
        return self.clientCache["LiveData"]

    def setLiveData(self, data):
        self.clientCache["LiveData"] = data
        self.pushInternalLog(data)

    # ||=======================||
    # InteralLog Helpers
    def pushInternalLog(self, data):
        self.clientCache["InternalLog"].append(data)

    def getInternalLog(self, i):
        
        if (isinstance(i, int) == False):
            return self.clientCache["InternalLog"]
        else:
            return self.clientCache["InternalLog"][int(i)]