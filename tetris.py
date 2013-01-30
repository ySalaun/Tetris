## wonderful project about tetris multiplayer game

from PyQt4 import QtGui
from PyQt4.QtGui  import QApplication

import sys

import params
import table_screen
import tetris_ai
import tetris_button
import tetris_scene

## MAIN ##

app = QtGui.QApplication(sys.argv)

# initialize graphics
graphics = tetris_scene.Graphics()

# initialize table threads
tableP1 = table_screen.Table(graphics, 1)
tableP2 = table_screen.Table(graphics, 2)

# temporary
for i in range(1,params.ROW_NB*params.COL_NB):
	tableP1.value[i] = params.WHITE
for i in range(1,params.ROW_NB*params.COL_NB):
	tableP2.value[i] = params.WHITE

# initialize AI
ai = tetris_ai.AI(tableP1)

# initialize buttons thread
button = tetris_button.Button(graphics, tableP1, tableP2)

# thread start
#button.start()
tableP1.start() 
#ai.start()
#tableP2.start()

sys.exit(app.exec_())
