# |===============================================================|
# ||
# ||  Program/File:		Routes.py
# ||
# ||  Description:		Manages adding system paths
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:	21 November 2018 | Logan Wilkovich
# |===============================================================|
# ||=======================||
# Routes

# Controllers

# Tools

# Test

# Premades
import sys
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# |============================================================================|

class Routes(object):

	def __init__(self):
		self.initializeRoutes()

	def initializeRoutes(self):
		sys.path.insert(0, './Config/')
		sys.path.insert(0, './Controllers/')
		sys.path.insert(0, './Server/')
		sys.path.insert(0, './Tools/')
		sys.path.insert(0, './Test/')
		sys.path.insert(0, './Test/TestLibrary/')

Routes()

# |============================================================================|