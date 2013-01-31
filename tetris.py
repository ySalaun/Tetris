## wonderful project about tetris multiplayer game

from PyQt4 import QtGui
from PyQt4.QtGui  import QApplication

import sys

import params
import table_screen
import tetris_ai
import tetris_scene

## MAIN ##

app = QtGui.QApplication(sys.argv)
app.processEvents()

# initialize graphics
tetris = tetris_scene.Tetris()

# initialize AI
ai = tetris_ai.AI(tetris.tableP1)

# start tetris
tetris.start()

#ai.start()

sys.exit(app.exec_())
