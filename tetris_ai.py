# artificial intelligence for multiplayer tetris
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui

import random
import table_screen

UP		= 1
DOWN	= 2
LEFT	= 3
RIGHT	= 4

class AI(QtGui.QWidget):
	def __init__(self, t, p):
		# inherit from QWidget for reception of signals
		QtGui.QWidget.__init__(self)
		
		# associated with a table
		self.table	= t
		self.player	= p
		
		# associated with a timer
		self.timer	= QtCore.QBasicTimer()
	
	# timer event, call the corresponding starting function
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			self.start()
			
	def move(self, direction):
		if direction == LEFT:
			self.emit(QtCore.SIGNAL("left"), self.player, -1)
		elif direction == RIGHT:
			self.emit(QtCore.SIGNAL("right"), self.player, 1)
		elif direction == DOWN:
			self.emit(QtCore.SIGNAL("down"), self.player)
		elif direction == UP:
			self.emit(QtCore.SIGNAL("rotate"), self.player)
	
	def start(self):
		direction = random.randrange(1,4)
		self.move(direction)
		self.timer.start(100, self)