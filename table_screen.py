# Table class that checks when game over and contains the color of each case

import params

class Table():
	def __init__(self):
		table = []
		index = 0
		while index < params.ROW_NB*params.COL_NB:
			table.append(params.WHITE)
			index += 1
		self.value = table
		
		