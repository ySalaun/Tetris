from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic

import params
import table_screen
import tetris_playscreen
import time
import threading

# Main Tetris class
class Tetris(QtGui.QWidget):
	# initialization
	def __init__(self, parent = None):
		# inherit from QWidget for reception of signals
		QtGui.QWidget.__init__(self, parent)
		
		# keyboard init (contains the scene)
		self.keyboard = Keyboard()
		
		# tables init
		self.tableP1 = table_screen.Table(1)
		self.tableP2 = table_screen.Table(2)
		self.screenP1 = self.keyboard.ui.screenP1
		self.screenP2 = self.keyboard.ui.screenP2
		
		# boolean that indicates if game is running
		self.running = False
		
		# link with a timer
		self.timerP1 = QtCore.QBasicTimer()
		self.timerP2 = QtCore.QBasicTimer()
		
		# display the screen
		self.keyboard.show()
		
		# add connections to signal (buttons, keyboard, ...)
		self.connect_signals()
	
	# starting method
	# only used once at the early beginning
	def start(self):
		self.startP1()
		self.startP2()
	
	# method called by timerP1 at each iteration
	def startP1(self):
		if self.running:
			self.tableP1.start()
			self.updateScreen()
		time = self.tableP1.speed()
		self.timerP1.start(time, self)
	
	# method called by timerP2 at each iteration
	def startP2(self):
		if self.running:
			self.tableP2.start()
			self.updateScreen()
		time = self.tableP2.speed()
		self.timerP2.start(time, self)
	
	# timer event, call the corresponding starting function
	def timerEvent(self, event):
		if event.timerId() == self.timerP1.timerId():
			self.startP1()
		if event.timerId() == self.timerP2.timerId():
			self.startP2()
	
	# display functions
	# update [table] for [player] screen
	def updateScreen(self, player = 0):
		if player != 2:
			scene = Scene(self.screenP1.width(), int(self.screenP1.height()))
			scene.display(self.screenP1, self.tableP1)
		if player != 1:
			scene = Scene(self.screenP2.width(), int(self.screenP2.height()))
			scene.display(self.screenP2, self.tableP2)

	# when start button is pressed
	def game_start(self):
		self.running = True

	# when pause button is pressed
	def game_pause(self):
		self.running = False
	
	# when left/right button for player [p] is pressed
	def move(self, p, direction):
		if self.running:
			if p == 1:
				self.tableP1.tet.move(self.tableP1, direction)
			if p == 2:
				self.tableP1.tet.move(self.tableP2, direction)
			self.updateScreen(p)
		
	# when down button for player [p] is pressed
	def down(self, p):
		if self.running:
			if p == 1:
				self.tableP1.tet.low(self.tableP1)
			if p == 2:
				self.tableP1.tet.low(self.tableP2)
			self.updateScreen(p)
		
	# when rotate button for player [p] is pressed
	def rotate(self, p):
		if self.running:
			if p == 1:
				self.tableP1.tet.rotate(1, self.tableP1)
			if p == 2:
				self.tableP1.tet.rotate(1, self.tableP2)
			self.updateScreen(p)
		
	# when display signal is received for player [p]
	def display(self, p):
		print 'display player ', p

	# connect the signals to graphics
	def connect_signals(self):
		# connect start button
		QObject.connect(self.keyboard.ui.start,SIGNAL("clicked()"),self.game_start)
		
		# connect pause button
		QObject.connect(self.keyboard.ui.pause,SIGNAL("clicked()"),self.game_pause)
		
		# connect keyboard buttons
		QObject.connect(self.keyboard,SIGNAL("left"),self.move)
		QObject.connect(self.keyboard,SIGNAL("right"),self.move)
		QObject.connect(self.keyboard,SIGNAL("down"),self.down)
		QObject.connect(self.keyboard,SIGNAL("rotate"),self.rotate)
		QObject.connect(self.keyboard,SIGNAL("pause"),self.game_pause)
		
		# connect with signals from table
		QObject.connect(self.tableP1,SIGNAL("display"),self.display)

# Scene class that transform a table into a displayable scene
class Scene(QGraphicsScene):
	# initialization
	def __init__(self, w, h):
		# inherit from QGraphicsScene
		QGraphicsScene.__init__(self, 0, 0, w-2, h-2)
		
		#initialize width and height
		self.w = w-2
		self.h = h-2
		
		# initialize the size of the cases
		self.caseW = self.w/params.COL_NB
		self.caseH = self.h/params.ROW_NB
		
	# transform a table into a displayable scene
	def display(self, screen, table):
		t = 0
		while t < len(table.value):
			i = t%params.ROW_NB
			j = (t-i)/params.ROW_NB
			self.addCase(i, j, table.value[i+j*params.ROW_NB])
			t += 1
		for (x,y) in params.dico_shape[table.tet.type][table.tet.angle]:
			i = table.tet.position_y+y
			j = table.tet.position_x+x
			self.addCase(i, j, table.tet.color)
		screen.setScene(self)

	# add a case with coordinate (i,j) in the table
	def addCase(self, i, j, color):
		self.addRect(j*self.w/params.COL_NB, i*self.h/params.ROW_NB, self.caseW, self.caseH, QPen(color), QBrush(color))
		
# class that emit signal when a key is pressed
class Keyboard(QtGui.QDialog):
	# initialization
	def __init__(self, parent=None):
		# inherit from QDialog
		QtGui.QDialog.__init__(self, parent)
		
		# initialize the playscreen
		self.ui = tetris_playscreen.Ui_Dialog()
		
		# becomes dialog class for the playscreen
		self.ui.setupUi(self)

	# when a key is pressed, emit a signal for Tetris class
	def keyPressEvent(self, event):
		if event.key() == 90:
			self.emit(QtCore.SIGNAL("rotate"), 1)
		elif event.key() == 81:
			self.emit(QtCore.SIGNAL("left"), 1, -1)
		elif event.key() == 68:
			self.emit(QtCore.SIGNAL("right"), 1, 1)
		elif event.key() == 83:
			self.emit(QtCore.SIGNAL("down"), 1)
		elif event.key() == 32:
			self.emit(QtCore.SIGNAL("pause"))


