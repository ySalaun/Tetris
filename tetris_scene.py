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
	def display(self, screen, table, tet):
		t = 0
		while t < len(table):
			i = t%params.ROW_NB
			j = (t-i)/params.ROW_NB
			self.addCase(i, j, table[t])
			if j == 0:
				self.addCase(i, j, params.RED)
			t += 1
		print '-----------'
		for (x,y) in params.dico_shape[tet.type][tet.angle]:
			i = tet.position_y-y
			j = tet.position_x+x
			print i, j
			self.addCase(i, j, tet.color)
		screen.setScene(self)
		
	# add a case with coordinate (i,j) in the table
	def addCase(self, i, j, color):
		self.addRect(j*self.w/params.COL_NB, i*self.h/params.ROW_NB, self.caseW, self.caseH, QPen(color), QBrush(color))
		
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
		self.P2 = self.ui.screenP2
		
		self.dialog.show()
	
	# display functions
	# update [table] for [player] screen
	def updateScreen(self, table, tet, player):
		if player == 1:
			scene = Scene(self.P1.width(), int(self.P1.height()))
			scene.display(self.P1, table, tet)
		else:
			scene = Scene(self.P2.width(), int(self.P2.height()))
			scene.display(self.P2, table, tet)
	
	# update screen display
	def display(self):
		# player 1 scene
		scene = Scene(self.P1.width(), int(self.P1.height()))
		scene.display(self.P1, self.tableP1)
		# player 2 scene
		scene = Scene(self.P2.width(), int(self.P2.height()))
		scene.display(self.P2, self.tableP2)
