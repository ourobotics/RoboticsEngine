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
		self.messageTypes = ["Debug", "Standard", "Warning", "Error"]
		self.messageSettings = {
			"Debug": False,
			"Standard": False,
			"Warning": False,
			"Error": False
		}

		# ||=======================||
		# Parent Information
		self.pType = _class
		self.pCreatedTime = strftime("%a;%d-%m-%Y;%H-%M-%S", localtime())
		self.pCreatedIndex = 0
		self.logSize = 50

	def setMessageSettings(self, debug, stardard, warning, error):
		self.messageSettings[self.messageTypes[0]] = debug
		self.messageSettings[self.messageTypes[1]] = stardard
		self.messageSettings[self.messageTypes[2]] = warning
		self.messageSettings[self.messageTypes[3]] = error

	def setDebug(self, boolean):
		self.messageSettings[self.messageTypes[0]] = boolean

	def setStandard(self, boolean):
		self.messageSettings[self.messageTypes[1]] = boolean

	def setWarning(self, boolean):
		self.messageSettings[self.messageTypes[2]] = boolean

	def setError(self, boolean):
		self.messageSettings[self.messageTypes[3]] = boolean

	def setLogSize(self, size):
		self.logSize = size

	def dumpMessageBuffer(self):
		with open('../Logs/' + self.pType + ';' + str(self.pCreatedIndex) + ';' + str(self.logSize) + ';' + self.pCreatedTime + '.log', 'w') as f:
			for item in self.messageBuffer:
				f.write("%s\n" % item)    
		self.messageBuffer = []
		self.pCreatedIndex += 1

	def addMessageBuffer(self, message):
		self.messageBuffer.append(message)
		if (len(self.messageBuffer) > self.logSize):
			self.dumpMessageBuffer()

	def log(self, messageType, message, forcePrint = 0):
		printBool = self.messageSettings[messageType]
		updatedMessage = strftime("%d-%m-%Y | %H:%M:%S", localtime()) + " | " + messageType.ljust(8) + ' | ' + message
		self.addMessageBuffer(updatedMessage)
		if (printBool or forcePrint):
			print(updatedMessage)

# ||============================================================================||