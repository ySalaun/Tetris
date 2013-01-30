from PyQt4.QtCore import *

# Button class that inform the programm when a button or a key is pressed
class Button(QThread):
	def __init__(self, g, tableP1, tableP2):
		# thread init
		QThread.__init__(self)
		
		# link to graphics and its buttons
		self.graphics = g
		
		# link to tables
		self.P1 = tableP1
		self.P2 = tableP2
		
		# buttons
		self.running = False
		
	def game_start(self):
		if not self.running:
			self.P1.start() 
			self.P2.start()
			self.running = True
	
	def game_pause(self):
		if self.running:
			# how to pause a thread ? how to re-run it ?
			self.running = False
	 
	def run(self):
		while True:
			if self.graphics.ui.start.isEnabled():
				self.game_pause()
			else:
				self.game_start()
			self.thread().sleep(1)