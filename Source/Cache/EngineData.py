# |===============================================================|
# ||
# ||  Program/File:		EngineData.py
# ||
# ||  Description:		Singleton To Represent Current Data Model
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:	24 December 2018 | Logan Wilkovich
# |===============================================================|
# |===============================================================|
# ||=======================||
# Routes
# Controllers
# Tools
# Test
# Premades
from time import time
import traceback
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# |===============================================================|

class EngineData:

    # |===============================================================|
    class EnergyController:
        EnergyController = {
            "LiveData": None,
            "InternalLog": []
        }

        # ||=======================||
        # LiveData Helpers
        @classmethod
        def getLiveData(cls):
            return cls.EnergyController["LiveData"]

        @classmethod
        def setLiveData(cls, data):
            cls.EnergyController["LiveData"] = data

        # ||=======================||
        # InteralLog Helpers
        @classmethod
        def pushInternalLog(cls, data):
            cls.EnergyController["InternalLog"].append(data)

        @classmethod
        def getInternalLog(cls, i):
            if (i == None):
                return cls.EnergyController["InternalLog"]
            else:
                return cls.EnergyController["InternalLog"][int(i)]

    # |===============================================================|
    class ThermoController:
        ThermoController = {
            "LiveData": None,
            "InternalLog": []
        }

        # ||=======================||
        # LiveData Helpers
        @classmethod
        def getLiveData(cls):
            return cls.ThermoController["LiveData"]

        @classmethod
        def setLiveData(cls, data):
            cls.ThermoController["LiveData"] = data

        # ||=======================||
        # InteralLog Helpers
        @classmethod
        def pushInternalLog(cls, data):
            cls.ThermoController["InternalLog"].append(data)

        @classmethod
        def getInternalLog(cls, i):
            if (i == None):
                return cls.ThermoController["InternalLog"]
            else:
                return cls.ThermoController["InternalLog"][int(i)]

    # |===============================================================|
    class mechanicalData:
        mechanicalData = {
            "LiveData": None,
            "InternalLog": []
        }

        # ||=======================||
        # LiveData Helpers
        @classmethod
        def getLiveData(cls):
            return cls.mechanicalData["LiveData"]

        @classmethod
        def setLiveData(cls, type, data):
            cls.mechanicalData["LiveData"] = data

        # ||=======================||
        # InteralLog Helpers
        @classmethod
        def pushInternalLog(cls, data):
            cls.mechanicalData["InternalLog"].append(data)

        @classmethod
        def getInternalLog(cls, i):
            if (i == None):
                return cls.mechanicalData["InternalLog"]
            else:
                return cls.mechanicalData["InternalLog"][int(i)]

    # |===============================================================|
    class GpsController:
        GpsController = {
            "LiveData": None,
            "InternalLog": []
        }

        # ||=======================||
        # LiveData Helpers
        @classmethod
        def getLiveData(cls):
            return cls.GpsController["LiveData"]

        @classmethod
        def setLiveData(cls, data):
            cls.GpsController["LiveData"] = data

        # ||=======================||
        # InteralLog Helpers
        @classmethod
        def pushInternalLog(cls, data):
            cls.GpsController["InternalLog"].append(data)

        @classmethod
        def getInternalLog(cls, i):
            if (i == None):
                return cls.GpsController["InternalLog"]
            else:
                return cls.GpsController["InternalLog"][int(i)]

    # |===============================================================|
    class NetworkClient:
        NetworkClient = {
            "LiveData": None,
            "InternalLog": []
        }

        # ||=======================||
        # LiveData Helpers
        @classmethod
        def getLiveData(cls):
            return cls.NetworkClient["LiveData"]

        @classmethod
        def setLiveData(cls, type, data):
            cls.NetworkClient["LiveData"] = data

        # ||=======================||
        # InteralLog Helpers
        @classmethod
        def pushInternalLog(cls, data):
            cls.NetworkClient["InternalLog"].append(data)

        @classmethod
        def getInternalLog(cls, i):
            if (i == None):
                return cls.NetworkServer["InternalLog"]
            else:
                return cls.NetworkServer["InternalLog"][int(i)]
        
# |===============================================================|