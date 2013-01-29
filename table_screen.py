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

		# table value init
		table = []
		for index in range(params.ROW_NB*params.COL_NB):
			table.append(params.WHITE)
		self.value = table
		self.graphics = g
		self.player = p
		self.tet=tetrominos.Tetrominos()
		
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
			
	# threading methods
	def run(self):
		while True:
			while self.tet.low(self): 
				self.graphics.updateScreen(self.value, self.tet, self.player)
				self.thread().sleep(params.SPEED)
				print 'low'
			self.tet.add_tetrominos(self)
			line_complete = self.checkLineComplete()
			if line_complete:
				print 'jackpot'
				self.graphics.updateScreen(self.value, self.tet, self.player)
			self.tet = tetrominos.Tetrominos()
