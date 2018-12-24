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

# Server
from NetworkClient import NetworkClient
# Tools

# Test

# Premades
from time import sleep
from threading import Thread
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# ||============================================================================||

class RoboticsEngine(object):
    def __init__(self):
        # ||=======================||
        # return
        self.networkclient = NetworkClient()
        self.networkclient.establishConnection()
        while 1:
            self.networkclient.pingServer()
            sleep(10)
        # self.networkclient.closeConnection()

re = RoboticsEngine()