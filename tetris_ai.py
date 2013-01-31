# artificial intelligence for multiplayer tetris
from PyQt4.QtCore import *

import table_screen

class AI(QThread):
	def __init__(self, t):
		# thread init
		QThread.__init__(self)
		
		# associated with a table
		self.table = t
		
	def translate(self, direction):
		self.table.tet.move(self.table, direction)
	
	def run(self):
		d = 1
		while True:
			if not self.translate(d):
				d = 1 - d
			self.msleep(10)