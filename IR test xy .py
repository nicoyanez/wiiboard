import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import random

from ctypes  import *

#import pywiiuse as wiiuse
import wiiuse
import time
import os
import math

class Grafico(QtGui.QWidget):
    def __init__(self):
        super(Grafico, self).__init__()
        self.l1=0
        self.l2=0
        self.l3=0
        self.nmotes = 1
        self.wiimotes = wiiuse.init(self.nmotes)
        found = wiiuse.find(self.wiimotes, self.nmotes, 5)
        if not found:
            print 'not found'
            sys.exit(1)
        connected = wiiuse.connect(self.wiimotes, self.nmotes)
        if connected:
            print 'Connected to %i wiimotes (of %i found).' % (connected, found)
        else:
            print 'failed to connect to any wiimote.'
            sys.exit(1)
        for i in range(self.nmotes):
            wiiuse.set_leds(self.wiimotes[i], wiiuse.LED[i])
            wiiuse.status(self.wiimotes[0])
            wiiuse.set_ir(self.wiimotes[0], 1)
            wiiuse.set_ir_vres(self.wiimotes[i], 1000, 1000)
        wiiuse.rumble(self.wiimotes[0], 10)
        time.sleep(0.5)
        wiiuse.rumble(self.wiimotes[0], 0)
        self.wm = self.wiimotes[0][0]
        #wiiuse.motion_sensing(self.wiimotes, 0)
        ###############################
        #######iniciando wii

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(0, 0, 0, 160))
        qp.drawRect(0,470,700,5)
        qp.drawRect(0,0,5,700)
        self.drawLines(qp)
        qp.end()
    
    
    def drawLines(self, qp): ## este metodo hay que editarlo para que pinte yn punto
        wiiuse.motion_sensing(self.wiimotes, self.nmotes)
        wiiuse.poll(self.wiimotes, self.nmotes)
        pen = QtGui.QPen(QtCore.Qt.black, 10, QtCore.Qt.DotLine)
        qp.setPen(pen)
        try:
            T="(x,y)\t\tnum_dots\t\taspect\tpos\tstate\tax\tay\t\tdistance\tz\n"
            x=self.wm.ir.x
            y=self.wm.ir.y
            T+="("+str(x)+" , "+str(y)+")\t"+str(self.wm.ir.num_dots)+"\t\t"+str(self.wm.ir.pos)+"\t"+str(self.wm.ir.state)+"\t"+str(self.wm.ir.ax)+"\t"+str(self.wm.ir.ay)+"\t\t"+str(self.wm.ir.distance)+"\t"+str(self.wm.ir.z)
            #print str(x)+" "+str(y)
            qp.drawPoint(x,y)
            self.l1.setText("Accel X\t\tAccel Y\n"+str(self.wm.gforce.x)+"\t\t"+str(self.wm.gforce.y)+"")
            self.l2.setText(T)
            #print "##"
            T="(x,y)\t\torder\tVisible\trx\try\tsize\n"
            for a in self.wm.ir.dot:
                T+="( "+str(a.x)+" , "+str(a.y)+" )\t"+str(a.order)+"\t"+str(a.visible)+"\t"+str(a.rx)+"\t"+str(a.ry)+"\t"+str(a.size)+"\n"
                qp.drawPoint(a.rx,a.ry)
            T+="VRES\t"
            for a in self.wm.ir.vres:
                T+=str(a)+"\t"
            T+="\t###\tOfset\t"
            for a in self.wm.ir.offset:
                T+=str(a)+"\t"
            self.l3.setText(T)
            #print "##" 
            #self.l3.setText(str(self.wm.ir.dot))
        except:
            print "error pintando"
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
        self.initMenus()
        self.Widget = Grafico()
        self.setCentralWidget(self.Widget)
        """self.glWidget = GLWidget(self)
        self.setCentralWidget(self.glWidget)"""
        #########
        self.label1 = QtGui.QLabel('TEXTO',self)
        self.label1.setGeometry(30,90,600,300)
        self.label2 = QtGui.QLabel('TEXTO',self)
        self.label2.setGeometry(30,190,600,300)
        self.label3 = QtGui.QLabel('TEXTO',self)
        self.label3.setGeometry(30,290,600,300)
        self.Widget.setLabels(self.label1,self.label2,self.label3)
        #########
        """self.boton = QtGui.QPushButton("congela eje X",self)
        self.boton.setGeometry(745,150,70,50)
        self.botonY=QtGui.QPushButton("congela eje Y",self)
        self.botonY.setGeometry(745,250,70,50)
        self.botonZ=QtGui.QPushButton("congela eje Z",self)
        self.botonZ.setGeometry(745,350,70,50)"""
        #self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.giracubo )
        """self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.Widget.congelaG1 )
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

    def initMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.exitAction)

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
