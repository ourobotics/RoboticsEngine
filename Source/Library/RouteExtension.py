# ||=======================================================================||
# ||
# ||  Program/File:		RouteExtension.py
# ||
# ||  Description:		Manages adding system paths
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:	21 November 2018 | Logan Wilkovich
# ||=======================================================================||
# ||=======================||
# Premades
import sys
# ||=======================||
# Global Variables

# ||=======================||
# Notes

# ||=======================||
# ||=======================================================================||

class RouteExtension(object):

	def __init__(self):
		self.initializeRoutes()

	def initializeRoutes(self):
		for line in open('../Settings/System/' + 'Routes.sys'):
			sys.path.insert(0, line.replace('\n',''))

RouteExtension()

# ||=======================================================================||