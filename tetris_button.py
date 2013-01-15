from PyQt4.QtCore import *

# Button class that inform the programm when a button or a key is pressed
class Button(QThread):
	def __init__(self, g):
		# thread init
		QThread.__init__(self)
		
		# link to graphgics and its buttons
		self.graphics = g
		
	def run(self):
		while True:
			if self.graphics.ui.start.isEnabled():
				print 'enable'
			else:
				print 'disable'
			self.thread().sleep(1)