#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import params
import table_screen
import time
import random

class Tetrominos:
	# initialise a tetromino at the top of the screen
	def __init__(self):
		random.seed()
		self.type		= random.randrange(params.SHAPE_NB)
		self.angle		= random.randrange(params.dico_nbrot[self.type])
		self.position_x	= params.COL_NB/2
		self.position_y	= 0
		self.color		= params.dico_color[self.type]

	# check if the position is possible
	def check_is_possible(self,table):
		test = True
		for (x,y) in params.dico_shape[self.type][self.angle]:
			i = self.position_y+y
			j = self.position_x+x
			test = test and i >= 0 and i < params.ROW_NB
			test = test and j >= 0 and j < params.COL_NB
			if not test:
				break
			test = test and table.value[i+j*params.ROW_NB] == params.WHITE

		return test

	# turn the tetrominos
	def rotate(self,dir,table):
		aux = self.angle
		self.angle = (self.angle+dir)%params.dico_nbrot[self.type]
		if self.check_is_possible(table):
			return
		self.angle = aux

	# print and erase the tetrominos
	def add_tetrominos(self,table):
		for (x,y) in params.dico_shape[self.type][self.angle]:
			i = self.position_y+y
			j = self.position_x+x
			table.value[i+j*params.ROW_NB] = self.color
	
	# translate the tetrominos in a given [direction] and return True if it is possible
	def move(self, table, direction):
		self.position_x += direction
		if self.check_is_possible(table):
			return True
		self.position_x -= direction
		return False

	# lower the tetrominos and return True if it is possible
	def low(self,table):
		self.position_y += 1
		if self.check_is_possible(table):
			return True
		self.position_y -= 1
		return False
