import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import random

from ctypes  import *

import wiiuse
import time
import os
import math
import win32api
import win32con

class Grafico(QtGui.QWidget):
    def __init__(self):
        super(Grafico, self).__init__()
        self.l1=0
        self.l2=0
        self.l3=0
        
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(0, 0, 0, 160))
        self.drawAll(qp)
        qp.end()
    
    def drawAll(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 10, QtCore.Qt.DotLine)
        qp.setPen(pen)
        try:
            pos=win32api.GetCursorPos()
            qp.drawPoint(pos[0],pos[1])
            self.l1.setText(str(pos))
            self.l2.setText(str(win32api.GetKeyState ))
            #self.l3.setText(str(win32api. ))
        except :
            print "error pintando "
    def ingresaPuntoDeWiiMote(self):
        self.repaint()
    
    def setLabels(self,l1,l2,l3):
        self.l1=l1
        self.l2=l2
        self.l3=l3

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(850, 500)
        self.setWindowTitle('Data Logger')
        self.initActions()
        #self.initMenus()
        self.Widget = Grafico()
        self.setCentralWidget(self.Widget)
        """self.glWidget = GLWidget(self)
        self.setCentralWidget(self.glWidget)"""
        #########
        self.label1 = QtGui.QLabel('TEXTO',self)
        self.label1.setGeometry(45,90,500,50)
        self.label2 = QtGui.QLabel('TEXTO',self)
        self.label2.setGeometry(45,190,500,50)
        self.label3 = QtGui.QLabel('TEXTO',self)
        self.label3.setGeometry(45,290,500,50)
        self.Widget.setLabels(self.label1,self.label2,self.label3)
        #########
        """self.boton = QtGui.QPushButton("congela eje X",self)
        self.boton.setGeometry(745,150,70,50)
        self.botonY=QtGui.QPushButton("congela eje Y",self)
        self.botonY.setGeometry(745,250,70,50)
        self.botonZ=QtGui.QPushButton("congela eje Z",self)
        self.botonZ.setGeometry(745,350,70,50)
        #self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.giracubo )
        self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.Widget.congelaG1 )
        self.botonY.connect(self.botonY,QtCore.SIGNAL('clicked()'),self.Widget.congelaG2)
        self.botonZ.connect(self.botonZ,QtCore.SIGNAL('clicked()'),self.Widget.congelaG3)"""
        timer = QtCore.QTimer(self)
        timer.setInterval(0)
        #QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.Widget.ingresaPuntoAleatorio)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.Widget.ingresaPuntoDeWiiMote)
        timer.start()
        """timer = QtCore.QTimer(self)
        timer.setInterval(1)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.glWidget.spin)
        timer.start()"""

    def initActions(self):
        self.exitAction = QtGui.QAction('Quit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.connect(self.exitAction, QtCore.SIGNAL('triggered()'), self.close)

    """def initMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.exitAction)"""

    def close(self):
        QtGui.qApp.quit()

    def keyPressEvent(self, e):
        print e.key()
        """if e.key() == QtCore.Qt.Key_Escape:
            print "dasa"
            self.close()
        if e.key() == QtCore.Qt.Key_Left:
            print "izq"""

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    """app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())"""
