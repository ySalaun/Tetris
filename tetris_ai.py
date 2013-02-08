# artificial intelligence for multiplayer tetris
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui

import params
import random
import table_screen
import tetrominos
import time

UP		= 1
DOWN	= 2
LEFT	= 3
RIGHT	= 4

# generic class for AI
class AI(QtGui.QWidget):
	# initialization
	def __init__(self, t, p):
		# unherit from QWidget for reception of signals
		QtGui.QWidget.__init__(self)
		
		# associated with a table
		self.table	= t
		self.player	= p
		
		# associated with a timer
		self.timer	= QtCore.QBasicTimer()
		
		# identification for ai
		self.id = params.BASIC
		
		# for pause
		self.running = False
	
	# timer event, call the corresponding starting function
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId() and not self.table.game_over:
			self.start()
	
	# emit a signal in order to move in a given direction
	def move(self, direction):
		if direction	== LEFT:
			self.emit(QtCore.SIGNAL("left"), self.player, -1)
		elif direction	== RIGHT:
			self.emit(QtCore.SIGNAL("right"), self.player, 1)
		elif direction	== DOWN:
			self.emit(QtCore.SIGNAL("down"), self.player)
		elif direction	== UP:
			self.emit(QtCore.SIGNAL("rotate"), self.player)
	
	# starting method called regularly for ai 
	def start(self):
		direction = random.randrange(1,5)
		self.move(direction)
		self.timer.start(params.AI_LEVEL, self)

# AI created by Yohann
# very simple and has a lot of issues but works
class AI_yohann(AI):
	# initialization
	def __init__(self, t, p):
		AI.__init__(self, t, p)
		
		# storage of the best position
		self.X_opt		= 0
		self.Y_opt		= 0
		self.angle_opt	= 0
		
		# boolean that indicates if the optimal position is found
		self.opt_found	= False
		self.opt_path	= []
		# specify ai id
		self.id = params.YOHANN
		
	# starting method called regularly for ai 
	def start(self):
		# find the best position when not already
		if self.running:
			if not self.opt_found:
				not_reachable = []
				while True:
					self.best_position(not_reachable)
					self.opt_found = True
					self.opt_path = self.find_path()
					if len(self.opt_path) > 0:
						break
					not_reachable.append((self.Y_opt, self.X_opt))
			# move to this position
			self.go_to_opt()
		# call the timer to begin another cycle
		self.timer.start(params.AI_LEVEL, self)
	
	# method that finds the best path and execute it when necessary
	def go_to_opt(self):
		path = self.opt_path
		if len(path) > 0:
			command = path[len(path)-1]
			while command[1] <= self.table.tet.position_y:
				path.pop()
				if command[1] <= self.table.tet.position_y and command[0] != DOWN:
					self.move(command[0])
					break
				if len(path) > 0:
					command = path[len(path)-1]
				else:
					break
	
	# compute the fusion table of the table value and the tetrominos
	def fusion(self, tet):
		table = []
		for index in range(params.ROW_NB*params.COL_NB):
			table.append(self.table.value[index])
		for (x,y) in params.dico_shape[tet.type][tet.angle]:
			i = tet.position_y+y
			j = tet.position_x+x
			table[i+j*params.ROW_NB] = params.RED
		return table
	
	# computes the filling possibilities for a given tetrominos position
	def blank(self, table, i, j):
		n = 0
		if j < params.COL_NB-1 and table[i+(j+1)*params.ROW_NB] == params.WHITE:
			n += 1
		if j > 1 and table[i+(j-1)*params.ROW_NB] == params.WHITE:
			n += 1
		if i >= 1 and table[i-1+j*params.ROW_NB] == params.WHITE:
			n += 1
		return n
		
	def checkLineComplete(self, table):
		line_complete = 0
		for i in range(params.ROW_NB):
			sum = 0
			for j in range(params.COL_NB):
				if table[i+j*params.ROW_NB] != params.WHITE:
					sum += 1
			if sum == params.COL_NB:
				line_complete += 1
		return line_complete
	
	# computes the cost function of a given tetrominos in a given position
	def cost(self, tet):
		table		= self.fusion(tet)
		neighbours	= tet.neighbours()
		
		ghost_neighbours = 0
		cost = 0
		for (i,j) in neighbours:
			# if the neighbour is a border part it is very good (lower the cost)
			if not(i >= 0 and i < params.ROW_NB and j >= 0 and j < params.COL_NB):
				ghost_neighbours += 1
				cost -= 8
			# if the neighbour is a white case it can be bad
			elif table[i+j*params.ROW_NB] == params.WHITE:
				ghost_neighbours += 1
				escapes = self.blank(table, i, j)
				# if the white case is alone (no filling possibilities) it is very bad (increase the cost)
				if escapes == 0:
					cost += 500
				# if there is only one other white case near it, it is risky (increase a bit the cost)
				elif escapes == 1:
					cost += 20
				# else the case can be filled next time (no cost change)
			# if the neighbour is a tetrominos part it is very good (lower the cost)
			else:
				cost -= 10
		if ghost_neighbours == len(neighbours):
			return 1000
		line_filled = min(self.checkLineComplete(table), 4)
		if line_filled > 0:
			cost -= max(params.dico_score[line_filled]/50,10)
		return cost
	
	# finds the "best" position for a given tetrominos and stores it
	def best_position(self, not_reachable):
		candidate	= tetrominos.Tetrominos()
		type		= self.table.tet.type
		cost_min	= 1000
		for x in range(params.COL_NB):
			for y in range(1, params.ROW_NB):
				for angle in range(params.dico_nbrot[type]):
					candidate.set(type, angle, x, y)
					if not_reachable.count((y,x)) > 0 or not candidate.check_is_possible(self.table):
						continue
					cost = self.cost(candidate)
					if (cost < cost_min or cost <= cost_min + 5*(y - self.Y_opt)):
						self.X_opt		= x
						self.Y_opt		= y
						self.angle_opt	= angle
						cost_min		= cost
	
	# find a path to put the tetrominos in the 'best' position
	def find_path(self):
		# optimal tetrominos
		type		= self.table.tet.type
		tet_opt		= tetrominos.Tetrominos()
		tet_opt.set(type, self.angle_opt, self.X_opt, self.Y_opt)
		
		# current tetrominos
		X_curr		= self.table.tet.position_x
		Y_curr		= self.table.tet.position_y
		a_curr		= self.table.tet.angle
		tet_curr	= tetrominos.Tetrominos()
		tet_curr.set(type, a_curr, X_curr, Y_curr)
		
		path = []
		self.recursive_path(tet_opt, tet_curr, path)
		return path
	
	# recursive sub-method for find_path method
	def recursive_path(self, tet_path, tet_curr, path, direction = UP):
		# try to go upward
		while tet_path.low(self.table, -1) and tet_path.position_y != tet_curr.position_y:
			path.append((DOWN, tet_path.position_y, tet_path.position_x))
		# if the good line (y) is reached, go right or left and rotate if necessary
		if tet_path.position_y == tet_curr.position_y:
			if tet_path.position_x < tet_curr.position_x:
				for i in range(abs(tet_path.position_x-tet_curr.position_x)):
					path.append((LEFT, tet_path.position_y, tet_path.position_x))
			else:
				for i in range(abs(tet_path.position_x-tet_curr.position_x)):
					path.append((RIGHT, tet_path.position_y, tet_path.position_x))
			while tet_path.angle != tet_curr.angle:
				tet_path.angle = (tet_path.angle -1)%params.dico_nbrot[tet_path.type]
				path.append((UP, tet_path.position_y, tet_path.position_x))
			return True
		# else the tetrominos has to go right or left in order to find an 'escape'
		else:
			test = False
			path_left	= [(RIGHT, tet_path.position_y, tet_path.position_x)]
			if direction != RIGHT:
				tet_left = tet_path.copy()
				if tet_left.move(self.table, -1):
					test = self.recursive_path(tet_left, tet_curr, path_left, LEFT)
			if test:
				for i in range(len(path_left)):
					path.append(path_left[i])
				return True
			path_right	= [(LEFT, tet_path.position_y, tet_path.position_x)]
			if direction != LEFT:
				tet_right = tet_path.copy()
				if tet_right.move(self.table, 1):
					test = self.recursive_path(tet_right, tet_curr, path_right, RIGHT)
			if test:
				for i in range(len(path_right)):
					path.append(path_right[i])
				return True
		return False
