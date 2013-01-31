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
			self.addCase(i, j, table[i+j*params.ROW_NB])
			t += 1
		for (x,y) in params.dico_shape[tet.type][tet.angle]:
			i = tet.position_y+y
			j = tet.position_x+x
			self.addCase(i, j, tet.color)
		screen.setScene(self)
		
	# add a case with coordinate (i,j) in the table
	def addCase(self, i, j, color):
		self.addRect(j*self.w/params.COL_NB, i*self.h/params.ROW_NB, self.caseW, self.caseH, QPen(color), QBrush(color))
		
# Main graphics class
class Graphics(QtGui.QMainWindow):
	# initialization
	# call ui_dialogu class to display screen and buttons
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)
		
		# screen init
		self.keyboard = Keyboard()
		# self.dialog = QtGui.QDialog()
		# self.ui = tetris_playscreen.Ui_Dialog()
		# self.ui.setupUi(self.dialog)
		
		# tables init
		self.P1 = self.keyboard.ui.screenP1
		self.P2 = self.keyboard.ui.screenP2
		
		# boolean that indicates if game is running
		self.running = False
		
		self.keyboard.show()
		#self.dialog.show()
		
		self.connect_signals()
	
	# display functions
	# update [table] for [player] screen
	def updateScreen(self, table, tet, player):
		if player == 1:
			scene = Scene(self.P1.width(), int(self.P1.height()))
			scene.display(self.P1, table, tet)
		else:
			scene = Scene(self.P2.width(), int(self.P2.height()))
			scene.display(self.P2, table, tet)
		
	def game_start(self):
		self.running = True

	def game_pause(self):
		self.running = False
	
	def left(self):
		print 'left'
	
	def right(self):
		print 'right'
		
	def down(self):
		print 'down'
		
	def rotate(self):
		print 'rotate'

	def connect_signals(self):
		# connect start button
		QObject.connect(self.keyboard.ui.start,SIGNAL("clicked()"),self.game_start)
		# connect pause button
		QObject.connect(self.keyboard.ui.pause,SIGNAL("clicked()"),self.game_pause)
		# connect keyboard buttons
		QObject.connect(self.keyboard,SIGNAL("left()"),self.left)
		QObject.connect(self.keyboard,SIGNAL("right()"),self.right)
		QObject.connect(self.keyboard,SIGNAL("down()"),self.down)
		QObject.connect(self.keyboard,SIGNAL("rotate()"),self.rotate)
		QObject.connect(self.keyboard,SIGNAL("pause()"),self.game_pause)

class Keyboard(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = tetris_playscreen.Ui_Dialog()
		self.ui.setupUi(self)

	def keyPressEvent(self, event):
		if event.key() == 90:
			self.emit(QtCore.SIGNAL("rotate()"))
		elif event.key() == 81:
			self.emit(QtCore.SIGNAL("left()"))
		elif event.key() == 68:
			self.emit(QtCore.SIGNAL("right()"))
		elif event.key() == 83:
			self.emit(QtCore.SIGNAL("down()"))
		elif event.key() == 32:
			self.emit(QtCore.SIGNAL("pause()"))


