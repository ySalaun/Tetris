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
#ui.screenP1.drawForeground(QPainter.drawLine(5, 8, 15, 35))
scene = QGraphicsScene(0,0, int(ui.screenP1.width())-2,int(ui.screenP1.height())-2)
ui.screenP1.setScene(scene)
scene.addLine(2*int(ui.screenP1.width()),2*int(ui.screenP1.height()) , 0, 0)
sys.exit(app.exec_())
 
	