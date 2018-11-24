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
from Routes.Routes import Routes
# Controllers

# Server
from NetworkClient import NetworkClient
# Tools

# Test

# Premades
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
        self.networkclient.closeConnection()

re = RoboticsEngine()