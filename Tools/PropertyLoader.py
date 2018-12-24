# |===============================================================|
# ||
# ||  Program/File:		PropertyLoaderTool.py
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
from LoggingTool import LoggingTool
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
class PropertyLoaderTool(object):

	def __init__(self):
		self.LoggingTool = LoggingTool()

	def getProperties(self, filename):
		if (filename.find('.prop')) == -1:
			filename = filename + '.prop'
		try:
			properties = dict(line.strip().split('=') for line in open('./Config/' + filename))   
			return properties   
		except Exception as e:
			self.LoggingTool.printLog(str(traceback.format_exc()))

# ||============================================================================||