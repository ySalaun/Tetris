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
table.value[0] = params.RED
graphics.display(2, table.value)

sys.exit(app.exec_()) 
	