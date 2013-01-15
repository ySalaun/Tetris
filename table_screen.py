# Table class that checks when game over and contains the color of each case

import params
import tetris_scene
import threading

class Table(threading.Thread):
	# initialize table with white cases everywhere
	def __init__(self):
		# thread init
		threading.Thread.__init__(self)

		# table value init
		table = []
		for index in range(params.ROW_NB*params.COL_NB):
			table.append(params.WHITE)
		self.value = table
		
	# check in the table if there are complete lines and delete them
	def checkLineComplete(self):
		i = params.ROW_NB-1
		while i>=0:
			sum = 0
			for j in range(params.COL_NB):
				if self.value[i+j*params.ROW_NB] != params.WHITE:
					sum += 1
			if sum == params.COL_NB:
				self.deleteLine(i)
			else:
				i = i-1
				
	# delete line of [index] in the table
	def deleteLine(self, index):
		for i in range(0,index):
			for j in range(params.COL_NB):
				self.value[index-i+j*params.ROW_NB] = self.value[index-i-1+j*params.ROW_NB]
		for j in range(params.COL_NB):
			self.value[j*params.ROW_NB] = params.WHITE
			
	# threading methods
	def run(self):
		self.checkLineComplete()