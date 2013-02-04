# artificial intelligence for multiplayer tetris
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui

import params
import random
import table_screen
import tetrominos

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
		direction = random.randrange(1,5)
		self.move(direction)
		self.timer.start(100, self)
	

		
class AI_yohann(AI):
	def __init__(self, t, p):
		AI.__init__(self, t, p)
		
	def start(self):
		self.best_position()
		
	# compute the fusion table of the table value and the tetrominos
	def fusion(self, tet):
		table = []
		for index in range(params.ROW_NB*params.COL_NB):
			table.append(self.table.value[index])
		for (x,y) in params.dico_shape[tet.type][tet.angle]:
			i = tet.position_y+y
			j = tet.position_x+x
			table[i+j*params.ROW_NB] = self.table.value[i+j*params.ROW_NB]
		return table
	
	def blank(self, table, i, j):
		n = 0
		if j < params.COL_NB-1 and table[i+(j+1)*params.ROW_NB] == params.WHITE:
			n += 1
		if j > 1 and table[i+(j-1)*params.ROW_NB] == params.WHITE:
			n += 1
		if i >= 1 and table[i-1+j*params.ROW_NB] == params.WHITE:
			n += 1
		return n
		
	def cost(self, tet):
		table = self.fusion(tet)
		neighbours = tet.neighbours()
		
		cost = 0
		for (i,j) in neighbours:
			if not(i >= 0 and i < params.ROW_NB and j >= 0 and j < params.COL_NB):
				cost -= 1
			elif table[i+j*params.ROW_NB] == params.WHITE:
				if self.blank(table, i, j) == 0:
					cost += 10
			else:
				cost -= 1
		return cost
		
	def best_position(self):
		candidate = tetrominos.Tetrominos()
		type = self.table.tet.type
		
		candidates	= []
		cost_min	= 1000
		for x in range(params.COL_NB):
			for y in range(params.ROW_NB):
				for angle in range(params.dico_nbrot[type]):
					candidate.set(type, angle, x, y)
					if candidate.check_is_possible(self.table):
						cost = self.cost(candidate)
						candidates.append((x, y, angle, cost))
						if cost < cost_min or (cost == cost_min and y > Y_opt):
							X_opt		= x
							Y_opt		= y
							angle_opt	= angle
							cost_min	= cost
		#test = tetrominos.Tetrominos()
		#test.set(test.type, test.angle, 12, 24)
		#print test.check_is_possible(self.table)
		print cost_min, X_opt, Y_opt
		self.table.tet.position_x	= X_opt
		self.table.tet.angle		= angle_opt