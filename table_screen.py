from PyQt4.QtCore import *
from PyQt4.QtGui import * 
from PyQt4 import QtGui, QtCore

import params
import random
import tetrominos

# Table class that checks when game over and contains the color of each case
class Table(QWidget):
	# initialize table with white cases everywhere
	def __init__(self, p):
		# QWidget initialization (for emitting signal)
		QtGui.QWidget.__init__(self)

		# table value init
		table = []
		for index in range(params.ROW_NB*params.COL_NB):
			table.append(params.WHITE)
		self.value			= table
		self.player			= p
		self.speed_level	= 1
		self.game_over		= False
		
		# tetrominos initialization
		self.tet			= tetrominos.Tetrominos()
		
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
	
	# add [n] lines in the table and translates the current tetrominos of [n]
	def addLine(self, n):
		game_over = False
		for i in range(0, n):
			for j in range(params.COL_NB):
				if self.value[i+j*params.ROW_NB] != params.WHITE:
					game_over = True
		for i in range(0,params.ROW_NB-n):
			for j in range(params.COL_NB):
				self.value[i+j*params.ROW_NB] = self.value[i+n+j*params.ROW_NB]
		for i in range(params.ROW_NB-n, params.ROW_NB):
			for j in range(params.COL_NB):
				if (random.randrange(4) != 1 or j == i) and j != params.COL_NB - i:
					self.value[i+j*params.ROW_NB] = params.dico_color[random.randrange(params.SHAPE_NB)]
				else:
					self.value[i+j*params.ROW_NB] = params.WHITE
		if game_over or not self.tet.check_is_possible(self):
			self.game_over = True
		
	# compute the speed depending on the speed level
	def speed(self):
		return params.SPEED*5/self.speed_level
	
	# emit a signal when 1 or more (max. 4) lines are filled
	def score(self, n):
		self.emit(QtCore.SIGNAL("score"), self.player, n)

	# threading methods
	def start(self):
		# try to lower the tetrominos
		if not self.tet.low(self):
			# when the tetrominos cannot move anymore
			self.tet.add_tetrominos(self)
			
			# check if one line or more are complete
			line_complete = self.checkLineComplete()
			if line_complete:
				self.score(line_complete)
			
			# create new tetrominos
			self.tet = tetrominos.Tetrominos()
			self.emit(QtCore.SIGNAL("new tetrominos"), self.player)
			if not self.tet.check_is_possible(self):
				self.game_over = True
