# |===============================================================|
# ||
# ||  Program/File:		ConfigLoader.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:	23 July 2018 | Logan Wilkovich
# |===============================================================|
# ||=======================||
# Routes

# Controllers

# Tools
# from LoggingTool import LoggingTool
# Test

# Premades
from time import strftime, localtime
import traceback
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# |============================================================================|
class ConfigLoader(object):

	def __init__(self):
		return

	def getConfig(self, filename):
		if (filename.find('.conf')) == -1:
			filename = filename + '.conf'
		try:
			config = dict(line.strip().split('=') for line in open('../Config/' + filename))   
			return config   
		except Exception as e:
			return {"Error": e}

# ||============================================================================||