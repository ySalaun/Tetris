## wonderful project about tetris multiplayer game

from PyQt4 import QtGui

import sys
import random

import params
import table_screen
import tetris_scene

## MAIN ##

app = QtGui.QApplication(sys.argv)

tableP1 = table_screen.Table()
tableP2 = table_screen.Table()
for i in range(1,params.ROW_NB*params.COL_NB):
	tableP1.value[i] = params.RED
for i in range(1,params.ROW_NB*params.COL_NB):
	tableP2.value[i] = params.GREEN
	
graphics = tetris_scene.Graphics(tableP1, tableP2)
graphics.run() 
tableP1.run() 
graphics.display()
tableP2.run()
graphics.display()

sys.exit(app.exec_()) 
	