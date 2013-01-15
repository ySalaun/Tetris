from PyQt4.QtCore import *	
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic

import params
import tetris_playscreen
import time
import threading

# Scene class that transform a table into a displayable scene
class Scene(QGraphicsScene):
	# initialization
	def __init__(self, w, h):
		QGraphicsScene.__init__(self, 0, 0, w-2, h-2)
		self.w = w-2
		self.h = h-2
		self.caseW = self.w/params.COL_NB
		self.caseH = self.h/params.ROW_NB
		
	# transform a table into a displayable scene
	def display(self, screen, table):
		t = 0
		while t < len(table):
			j = t%params.ROW_NB
			i = (t-j)/params.ROW_NB
			self.addCase(i, j, table[t])
			t += 1
		screen.setScene(self)
		
	# add a case with coordinate (i,j) in the table
	def addCase(self, i, j, color):
		self.addRect(i*self.w/params.COL_NB, j*self.h/params.ROW_NB, self.caseW, self.caseH, QPen(color), QBrush(color))
		
# Main graphics class
class Graphics():
	# initialization
	# call ui_dialogu class to display screen and buttons
	def __init__(self):
		# screen init
		self.dialog = QtGui.QDialog()
		self.ui = tetris_playscreen.Ui_Dialog()
		self.ui.setupUi(self.dialog)
		
		# tables init
		self.P1 = self.ui.screenP1
		self.tableP1 = []
		self.P2 = self.ui.screenP2
		self.tableP2 = []
		
		self.dialog.show()
	
	# display functions
	# update [table] for [player] screen
	def updateScreen(self, table, player):
		if player == 1:
			self.tableP1 = table
		else:
			self.tableP2 = table
		self.display()
	
	# update screen display
	def display(self):
		# player 1 scene
		scene = Scene(self.P1.width(), int(self.P1.height()))
		scene.display(self.P1, self.tableP1)
		# player 2 scene
		scene = Scene(self.P2.width(), int(self.P2.height()))
		scene.display(self.P2, self.tableP2)