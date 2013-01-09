## wonderful project about tetris multiplayer game

from PyQt4 import QtGui

import sys
import random

import params
import table_screen
import tetris_scene

## MAIN ##

app = QtGui.QApplication(sys.argv)
graphics = tetris_scene.Graphics()

table = table_screen.Table()
for i in range(1,params.ROW_NB*params.COL_NB):
	table.value[i] = params.RED
graphics.display(2, table.value)
table.checkLineComplete()
graphics.display(2, table.value)

sys.exit(app.exec_()) 
	