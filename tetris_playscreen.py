# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yohann\Documents\GitHub\Tetris\tetris_playscreen.ui'
#
# Created: Wed Dec 19 16:12:21 2012
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(757, 524)
        self.screenP1 = QtGui.QGraphicsView(Dialog)
        self.screenP1.setGeometry(QtCore.QRect(20, 20, 261, 481))
        self.screenP1.setObjectName(_fromUtf8("screenP1"))
        self.screenP2 = QtGui.QGraphicsView(Dialog)
        self.screenP2.setGeometry(QtCore.QRect(470, 20, 261, 481))
        self.screenP2.setObjectName(_fromUtf8("screenP2"))
        self.scoreLabelP2 = QtGui.QLabel(Dialog)
        self.scoreLabelP2.setGeometry(QtCore.QRect(310, 100, 121, 21))
        self.scoreLabelP2.setObjectName(_fromUtf8("scoreLabelP2"))
        self.scoreP1 = QtGui.QLCDNumber(Dialog)
        self.scoreP1.setGeometry(QtCore.QRect(310, 60, 131, 23))
        self.scoreP1.setObjectName(_fromUtf8("scoreP1"))
        self.scoreP2 = QtGui.QLCDNumber(Dialog)
        self.scoreP2.setGeometry(QtCore.QRect(310, 130, 131, 23))
        self.scoreP2.setObjectName(_fromUtf8("scoreP2"))
        self.start = QtGui.QPushButton(Dialog)
        self.start.setGeometry(QtCore.QRect(340, 180, 75, 23))
        self.start.setObjectName(_fromUtf8("start"))
        self.pause = QtGui.QPushButton(Dialog)
        self.pause.setEnabled(False)
        self.pause.setGeometry(QtCore.QRect(340, 220, 75, 23))
        self.pause.setAutoDefault(True)
        self.pause.setFlat(False)
        self.pause.setObjectName(_fromUtf8("pause"))
        self.exit = QtGui.QPushButton(Dialog)
        self.exit.setGeometry(QtCore.QRect(340, 260, 75, 23))
        self.exit.setStatusTip(_fromUtf8(""))
        self.exit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.exit.setObjectName(_fromUtf8("exit"))
        self.scoreLabelP1 = QtGui.QLabel(Dialog)
        self.scoreLabelP1.setGeometry(QtCore.QRect(310, 30, 121, 21))
        self.scoreLabelP1.setObjectName(_fromUtf8("scoreLabelP1"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.exit, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QObject.connect(self.start, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.pause.setDisabled)
        QtCore.QObject.connect(self.start, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.start.setEnabled)
        QtCore.QObject.connect(self.pause, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.pause.setEnabled)
        QtCore.QObject.connect(self.pause, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.start.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.scoreLabelP2.setText(_translate("Dialog", "Score Player 2:", None))
        self.start.setText(_translate("Dialog", "START", None))
        self.pause.setText(_translate("Dialog", "PAUSE", None))
        self.exit.setText(_translate("Dialog", "EXIT", None))
        self.scoreLabelP1.setText(_translate("Dialog", "Score Player 1:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

