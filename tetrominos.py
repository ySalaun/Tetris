#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import params
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

	# set a tetrominos with the given parameters
	def set(self, t, a, x, y):
		self.type		= t
		self.angle		= a
		self.position_x	= x
		self.position_y	= y
	
	# copy a tetrominos
	def copy(self):
		tet = Tetrominos()
		tet.set(self.type, self.angle, self.position_x, self.position_y)
		return tet
	
	# check if the position is possible
	def check_is_possible(self,table):
		test = True
		for (x,y) in params.dico_shape[self.type][self.angle]:
			i = self.position_y+y
			j = self.position_x+x
			test = test and i >= 0 and i < params.ROW_NB
			test = test and j >= 0 and j < params.COL_NB
			if not test:
				return False
			test = test and table.value[i+j*params.ROW_NB] == params.WHITE
		return test

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
	# the option direction allows the tetrominos to go higher (used for ai only)
	def low(self, table, direction = 1):
		self.position_y += direction*1
		if self.check_is_possible(table):
			return True
		self.position_y -= direction*1
		return False
		
	# turn the tetrominos
	def rotate(self, dir ,table):
		aux = self.angle
		self.angle = (self.angle+dir)%params.dico_nbrot[self.type]
		if self.check_is_possible(table):
			return
		self.position_x -= 1
		if self.check_is_possible(table):
			return
		self.position_x += 2
		if self.check_is_possible(table):
			return
		self.position_x -= 1
		self.angle = aux
	
	# compute neighbours of the tetrominos
	def neighbours(self):
		neighbours = set()
		for (x,y) in params.dico_shape[self.type][self.angle]:
			i = self.position_y+y
			j = self.position_x+x
			for t in [-1, 1]:
				neighbours.add((i+t,j))
				neighbours.add((i,j+t))
		for (x,y) in params.dico_shape[self.type][self.angle]:
			i = self.position_y+y
			j = self.position_x+x
			neighbours.add((i,j))
			neighbours.remove((i,j))
		return neighbours
