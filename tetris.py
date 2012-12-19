## wonderful project about tetris multiplayer game

import sys
import random
import tetris_playscreen

from PyQt4.QtCore import *	
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic

## MAIN ##
app = QtGui.QApplication(sys.argv)
Dialog = QtGui.QDialog()
ui = tetris_playscreen.Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()
sys.exit(app.exec_())
 
	