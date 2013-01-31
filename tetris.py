## wonderful project about tetris multiplayer game

from PyQt4 import QtGui

import sys
import tetris_scene

## MAIN ##

app = QtGui.QApplication(sys.argv)
app.processEvents()

# initialize graphics
tetris = tetris_scene.Tetris()

# start tetris
tetris.start()

sys.exit(app.exec_())
