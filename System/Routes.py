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
		for line in open('./Config/' + 'Routes.sys'):
			sys.path.insert(0, line.replace('\n',''))

Routes()

# |============================================================================|