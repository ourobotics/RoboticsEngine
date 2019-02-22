# |===============================================================|
# ||
# ||  Program/File:		DebugLogger.py
# ||
# ||  Description:		
# ||
# ||  Author:           Logan Wilkovich
# ||  Email:            LWilkovich@gmail.com
# ||  Creation Date:	5 Feburary 2019 | Logan Wilkovich
# |===============================================================|
# ||=======================||
# Premades
from time import strftime, localtime
import traceback
# from time import gmtime, strftime
# ||=======================||
# Global Variables

# ||=======================||
# Notes
# strftime("%a, %d %b %Y %H:%M:%S", localtime())
# ||=======================||
# |============================================================================|
class DebugLogger(object):

	def __init__(self, _class):
		self.type = "DebugLogger"
		
		# ||=======================||
		self.forceDumpSize = 50
		self.messageBuffer = []
		self.messageTypes = ["Standard", "Warning ", "Error   "]
		self.messageSettings = {
			"Standard": 0,
			"Warning": 0,
			"Error": 0
		}

		# ||=======================||
		# Parent Information
		self.pType = _class
		self.pCreatedTime = strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())
		self.pCreatedIndex = 0

	def setMessageSettings(self, stardard, warning, error):
		self.messageSettings[self.messageTypes[0]] = stardard
		self.messageSettings[self.messageTypes[1]] = warning
		self.messageSettings[self.messageTypes[2]] = error

	def setStandard(self, boolean):
		self.messageSettings[self.messageTypes[0]] = boolean

	def setWarning(self, boolean):
		self.messageSettings[self.messageTypes[1]] = boolean

	def setError(self, boolean):
		self.messageSettings[self.messageTypes[1]] = boolean

	def dumpMessageBuffer(self):
		with open('../Logs/'+self.pType+';'+str(self.pCreatedIndex)+';'+self.pCreatedTime+'.log', 'w') as f:
			for item in self.messageBuffer:
				f.write("%s\n" % item)    
		self.messageBuffer = []
		self.pCreatedIndex += 1
		self.pCreatedTime = strftime("%a;%d-%m-%Y;%H:%M:%S", localtime())

	def addMessageBuffer(self, message):
		self.messageBuffer.append(message)
		if (len(self.messageBuffer) > 50):
			self.dumpMessageBuffer()

	def log(self, messageType, message, forcePrint = 0):
		printBool = self.messageSettings[messageType]
		self.addMessageBuffer(message)
		if (printBool or forcePrint):
			print(strftime("%d-%m-%Y | %H:%M:%S", localtime()) + " | " + messageType + ' | ' + message)

# ||============================================================================||