from PyQt4.QtCore import *

import params
import tetris_scene
import tetrominos

# Table class that checks when game over and contains the color of each case
class Table(QThread):
	# initialize table with white cases everywhere
	def __init__(self, g, p):
		# thread init
		QThread.__init__(self)
		self.running = False

		# table value init
		table = []
		for index in range(params.ROW_NB*params.COL_NB):
			table.append(params.WHITE)
		self.value = table
		self.graphics = g
		self.player = p
		self.speed_level = 1
		
		# tetrominos init
		self.tet = tetrominos.Tetrominos()
		
	# check in the table if there are complete lines and delete them
	# return the number of complete lines
	def checkLineComplete(self):
		line_complete = 0
		i = params.ROW_NB-1
		while i>=0:
			sum = 0
			for j in range(params.COL_NB):
				if self.value[i+j*params.ROW_NB] != params.WHITE:
					sum += 1
			if sum == params.COL_NB:
				self.deleteLine(i)
				line_complete += 1
			else:
				i = i-1
		return line_complete
		
	# delete line of [index] in the table
	def deleteLine(self, index):
		for i in range(0,index):
			for j in range(params.COL_NB):
				self.value[index-i+j*params.ROW_NB] = self.value[index-i-1+j*params.ROW_NB]
		for j in range(params.COL_NB):
			self.value[j*params.ROW_NB] = params.WHITE
	
	# compute the speed depending on the speed level
	def speed(self):
		return params.SPEED*5/self.speed_level
	
	# display a tetrominos after its move
	def display(self):
		while not self.graphics.running:
			self.msleep(self.speed())
		self.graphics.updateScreen(self.value, self.tet, self.player)
		self.msleep(self.speed())
	
	# threading methods
	def run(self):
		while not self.graphics.running:
			self.msleep(10)
		while True:
			self.display()
			# lowering tetrominos loop
			while self.tet.low(self):
				self.display()
			# when tetrominos cannot move anymore
			self.tet.add_tetrominos(self)
			# check if one line or more are complete
			line_complete = self.checkLineComplete()
			if line_complete:
				self.graphics.updateScreen(self.value, self.tet, self.player)
			self.tet = tetrominos.Tetrominos()
