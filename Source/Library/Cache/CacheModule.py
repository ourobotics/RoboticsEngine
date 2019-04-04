# ||==============================================================||
# ||
# ||  Program/File:     CacheModule.py
# ||
# ||  Description:      
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:    27 December 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Library
# Premades
from time import sleep, time, strftime, localtime
# ||=======================||
# Global Variables
# ||=======================||
# Notes
# ||=======================||
# ||=======================================================================||

class CacheModule:
    def __init__(self):
        # ||=======================||
        # Defaults
        self.controllerCache = {
            "LiveData": None,
            "InternalLog": []
        }

    # ||=======================||
    # LiveData Helpers
    def getLiveData(self):
        return self.controllerCache["LiveData"]

    def setLiveData(self, data):
        self.controllerCache["LiveData"] = data
        return True

    # ||=======================||
    # InteralLog Helpers
    def pushInternalLog(self, data):
        self.controllerCache["InternalLog"].append(data)
        return True

    def getInternalLog(self, i):
        if (i == None):
            return self.controllerCache["InternalLog"]
        else:
            return self.controllerCache["InternalLog"][int(i)]