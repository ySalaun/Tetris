from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui

import params
import table_screen
import tetris_ai
import tetris_playscreen

# Main Tetris class
class Tetris(QtGui.QWidget):
	# initialization
	def __init__(self):
		# inherit from QWidget for reception of signals
		QtGui.QWidget.__init__(self)
		
		# keyboard init (contains the scene)
		self.keyboard	= Keyboard()
		
		# tables init
		self.tableP1	= table_screen.Table(1)
		self.tableP2	= table_screen.Table(2)
		self.screenP1	= self.keyboard.ui.screenP1
		self.screenP2	= self.keyboard.ui.screenP2
		
		# score initialization
		self.scoreP1	= 0
		self.scoreP2	= 0
		self.keyboard.ui.scoreP1.setDigitCount(9)
		self.keyboard.ui.scoreP2.setDigitCount(9)
		
		# boolean that indicates if game is running
		self.running	= False
		
		# link with a timer
		self.timerP1	= QtCore.QBasicTimer()
		self.timerP2	= QtCore.QBasicTimer()
		
		# link with an AI for player 2
		self.ai2		= tetris_ai.AI(self.tableP2, 2)
		
		# display the screen
		self.keyboard.show()
		
		# add connections to signal (buttons, keyboard, ...)
		self.connect_signals()
		
		# start the ai
		self.ai2.start()
	
	# starting method
	# only used once at the early beginning
	def start(self):
		self.startP1()
		self.startP2()
	
	# method called by timerP1 at each iteration
	def startP1(self):
		if not self.tableP1.game_over:
			if self.running:
				self.tableP1.start()
				if self.tableP1.game_over:
					self.game_over(1)
				else:
					self.updateScreen()
					time = self.tableP1.speed()
					self.timerP1.start(time, self)
			else:
				time = self.tableP1.speed()
				self.timerP1.start(time, self)
				
	# method called by timerP2 at each iteration
	def startP2(self):
		if not self.tableP2.game_over:
			if self.running:
				self.tableP2.start()
				if self.tableP2.game_over:
					self.game_over(2)
				else:
					self.updateScreen()
					time = self.tableP2.speed()
					self.timerP2.start(time, self)
			else:
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
		
	def game_over(self, p):
		print 'game lost for player',p
	
	# when left/right button for player [p] is pressed
	def move(self, p, direction):
		if self.running:
			if p == 1:
				self.tableP1.tet.move(self.tableP1, direction)
			elif p == 2:
				self.tableP2.tet.move(self.tableP2, direction)
			self.updateScreen(p)
		
	# when down button for player [p] is pressed
	def down(self, p):
		if self.running:
			if p == 1:
				self.tableP1.tet.low(self.tableP1)
			elif p == 2:
				self.tableP2.tet.low(self.tableP2)
			self.updateScreen(p)
		
	# when rotate button for player [p] is pressed
	def rotate(self, p):
		if self.running:
			if p == 1:
				self.tableP1.tet.rotate(1, self.tableP1)
			elif p == 2:
				self.tableP2.tet.rotate(1, self.tableP2)
			self.updateScreen(p)
		
	# when score signal is received for player [p]
	def score(self, p, n):
		if p == 1:
			self.scoreP1 += params.dico_score[min(n,4)]
			self.keyboard.ui.scoreP1.display(self.scoreP1)
		if p == 2:
			self.scoreP2 += params.dico_score[min(n,4)]
			self.keyboard.ui.scoreP2.display(self.scoreP2)

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
		
		# connect with signals from table for score
		QObject.connect(self.tableP1,SIGNAL("score"),self.score)
		QObject.connect(self.tableP2,SIGNAL("score"),self.score)
		
		# connect to ai
		QObject.connect(self.ai2,SIGNAL("left"),self.move)
		QObject.connect(self.ai2,SIGNAL("right"),self.move)
		QObject.connect(self.ai2,SIGNAL("down"),self.down)
		QObject.connect(self.ai2,SIGNAL("rotate"),self.rotate)
		
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
		if not table.game_over:
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


