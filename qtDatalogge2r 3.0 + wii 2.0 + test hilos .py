import threading
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import random

from ctypes  import *

import wiiuse
import time
import os
import math

###hilo
class Wiibotones(threading.Thread):
      def __init__(self,w):
            threading.Thread.__init__(self)
            self.window = w
            self.sigue=True
            self.nmotes = self.window.nmotes
            self.wiimotes = self.window.wiimotes
            self.wm = self.window.wm
      def terminar(self):
            self.sigue = False
      def run(self):
            while self.sigue:
                  #time.sleep(0.105)
                  #wiiuse.motion_sensing(self.wiimotes,self.nmotes)
                  wiiuse.poll(self.wiimotes, self.nmotes)
                  try:
                        time.sleep(0.1)
                        """print self.wm.orient_threshold
                        print self.wm.accel_threshold
                        print self.wm.event
                        print "#####"
                        print self.wm.gforce.x
                        print self.wm.gforce.y
                        print self.wm.gforce.z"""
                        s = str(self.wm.accel_threshold)
                        #print "thresold "+s
                        if s!="0":
                              if s=="1":
                                    print "se solto el boton 2"
                                    self.window.emit(SIGNAL("BotonSuelto"), "2")
                              if s=="2":
                                    print "se solto el boton 1"
                                    self.window.emit(SIGNAL("BotonSuelto"), "1")
                              if s=="16":
                                    print "se solto el boton -"
                                    self.window.emit(SIGNAL("BotonSuelto"), "-")
                              if s=="128":
                                    print "se solto el boton HOME"
                                    self.window.emit(SIGNAL("BotonSuelto"), "HOME")
                              if s=="4096":
                                    print "se solto el boton +"
                                    self.window.emit(SIGNAL("BotonSuelto"), "+")
                              if s=="8":
                                    print "se solto el boton A"
                                    self.window.emit(SIGNAL("BotonSuelto"), "A")
                              if s=="1024":
                                    print "se solto el boton ABAJO"
                                    self.window.emit(SIGNAL("BotonSuelto"), "ABAJO")
                              if s=="512":
                                    print "se solto el boton DERECHA"
                                    self.window.emit(SIGNAL("BotonSuelto"), "DERECHA")
                              if s=="2048":
                                    print "se solto el boton ARRIBA"
                                    self.window.emit(SIGNAL("BotonSuelto"), "ARRIBA")
                              if s=="256":
                                    print "se solto el boton IZQUIERDA"
                                    self.window.emit(SIGNAL("BotonSuelto"), "IZQUIERDA")
                              if s=="4":
                                    print "se solto el boton B"
                                    self.window.emit(SIGNAL("BotonSuelto"), "B")
                              if s=="3":
                                    print "se solto el boton 1 y 2"
                                    self.window.emit(SIGNAL("BotonSuelto"), "1 y 2")
                        if str(self.wm.orient_threshold)[:3] !="0.0":
                              #print "se presiono un boton -> "+str(self.wm.orient_threshold)
                              if str(self.wm.orient_threshold)[:4] =="2.86":
                                    print "arriba"
                                    self.window.emit(SIGNAL("Boton"), "ARRIBA")
                                    #self.window.repaint()
                              if str(self.wm.orient_threshold)[:4] =="1.43":
                                    print "abajo"
                                    self.window.emit(SIGNAL("Boton"), "ABAJO")
                              if str(self.wm.orient_threshold)[:4] =="7.17":
                                    print "derecha"
                                    self.window.emit(SIGNAL("Boton"), "DERECHA")
                              if str(self.wm.orient_threshold)[:4] =="3.58":
                                    print "izquierda"
                                    self.window.emit(SIGNAL("Boton"), "IZQUIERDA")
                              if str(self.wm.orient_threshold)[:4] =="1.12":
                                    print "A"
                                    self.window.emit(SIGNAL("Boton"), "A")
                              if str(self.wm.orient_threshold)[:4] =="5.60":
                                    print "B"
                                    self.window.emit(SIGNAL("Boton"), "B")
                              if str(self.wm.orient_threshold)[:4] =="2.24":
                                    print "-"
                                    self.window.emit(SIGNAL("Boton"), "-")
                              if str(self.wm.orient_threshold)[:4] =="1.79":
                                    print "Home"
                                    self.window.emit(SIGNAL("Boton"), "HOME")
                              if str(self.wm.orient_threshold)[:4] =="5.73":
                                    print "+"
                                    self.window.emit(SIGNAL("Boton"), "+")
                              if str(self.wm.orient_threshold)[:4] =="2.80":
                                    print "1"
                                    self.window.emit(SIGNAL("Boton"), "1")
                              if str(self.wm.orient_threshold)[:4] =="1.40":
                                    print "2"
                                    self.window.emit(SIGNAL("Boton"), "2")
                              if str(self.wm.orient_threshold)[:4] =="1.83" or str(self.wm.orient_threshold)[:4] =="9.18":
                                    print "1 y 2"
                                    self.window.emit(SIGNAL("Boton"), "1 y 2")
                        """wiiuse.motion_sensing(self.wiimotes, 1)
                        #wiiuse.poll(self.wiimotes, self.nmotes)
                        print "gforce "+str(self.wm.gforce.x)
                        print "gforce "+str(self.wm.gforce.y)
                        print "gforce "+str(self.wm.gforce.z)
                        print "accel "+str(self.wm.accel.x)
                        print "orient "+str(self.wm.orient.roll)
                        print "orient "+str(self.wm.orient.pitch)
                        print "orient "+str(self.wm.orient.yaw)
                        print "accel_calib "+str(self.wm.accel_calib.cal_g.x)
                        print "state "+str(self.wm.state)
                        print "lstate"+str(self.wm.lstate.orient.roll)
                        print "lstate"+str(self.wm.lstate.orient.pitch)
                        print "lstate"+str(self.wm.lstate.orient.yaw)
                        #wiiuse.motion_sensing(self.wiimotes, 0)"""
                        self.window.ingresaPuntoDeWiiMote()
                  except :
                    print "error"
###hilo

class Grafico(QtGui.QWidget):
    def __init__(self):
        super(Grafico, self).__init__()
        self.maxG1 =1.0
        self.maxG2 =1.0
        self.maxG3 =1.0
        self.minG1 =-1.0
        self.minG2 =-1.0
        self.minG3 =-1.0
        self.b1 = True
        self.b2 = True
        self.b3 = True
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.arr = [0 for i in range(0,350)]
        self.arr1 = [0 for i in range(0,350)]
        self.arr2 = [0 for i in range(0,350)]
        #######iniciando Wiiii
        #####################
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
        ###iniciando hilos
        self.hilo = Wiibotones(self)
        self.hilo.start()
        #################
        
        """super(Example, self).__init__()
        self.initUI()"""
    """def initUI(self):
        self.setGeometry(300, 300, 280, 270)
        self.setWindowTitle('Pen styles')
        self.show()"""

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(0, 0, 0, 160))
        qp.drawRect(0,470,700,5)
        qp.drawRect(0,0,5,700)
        self.drawLines(qp)
        qp.end()
    
    
    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 1.5, QtCore.Qt.DotLine)
        qp.setPen(pen)
        
        for i in range(1,len(self.arr)):
            #qp.setPen(QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            y1 = 150-100.0*self.arr[i-1]/abs(self.maxG1-self.minG1)
            y2 = 150-100.0*self.arr[i]/abs(self.maxG1-self.minG1)
            qp.drawLine(math.trunc(10+2*(i-1)),math.trunc(y1) , math.trunc(10+2*i),math.trunc(y2 ))
            #qp.setPen(QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            y1 = 280-100.0*self.arr1[i-1]/abs(self.maxG2-self.minG2)
            y2 = 280-100.0*self.arr1[i]/abs(self.maxG2-self.minG2)
            qp.drawLine(math.trunc(10+2*(i-1)),math.trunc(y1) , math.trunc(10+2*i),math.trunc(y2 ))
            #qp.setPen(QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            y1 = 400-100.0*self.arr2[i-1]/abs(self.maxG3-self.minG3)
            y2 = 400-100.0*self.arr2[i]/abs(self.maxG3-self.minG3)
            qp.drawLine(math.trunc(10+2*(i-1)),math.trunc(y1) , math.trunc(10+2*i),math.trunc(y2 ))
            """qp.setPen(QtGui.QColor(255, 2, 3))
            qp.setFont(QtGui.QFont('Decorative', 20))
            qp.drawText(750,150,str(self.arr[i]))"""
        """qp.drawLine(10, 20, 50, 110)
        qp.drawLine(50, 110, 250, 360)
        qp.drawLine(250, 360, 250, 160)
        qp.drawLine(250, 160, 500, 260)"""
        
   # def ingresaPunto(self,dato,arr):
    #    for i in range(1,len(self.arr)):
     #       self.arr[i-1]=self.arr[i]
      #  self.arr[len(self.arr)-1]=dato
        
    def congelaG1(self):
        self.b1=not self.b1
    def congelaG2(self):
        self.b2=not self.b2
    def congelaG3(self):
        self.b3=not self.b3

    
    def ingresaPuntoAleatorio(self):
        if self.b1:
            for i in range(1,len(self.arr)):
                self.arr[i-1]=self.arr[i]
            self.arr[len(self.arr)-1]=random.randint(1,800)
            
        if self.b2:
            for i in range(1,len(self.arr1)):
                self.arr1[i-1]=self.arr1[i]
            self.arr1[len(self.arr1)-1]=random.randint(1,800)

        if self.b3:
            for i in range(1,len(self.arr2)):
                self.arr2[i-1]=self.arr2[i]
            self.arr2[len(self.arr2)-1]=random.randint(1,800)
        self.l1.setText(str(self.arr[len(self.arr)-1]))
        self.l2.setText(str(self.arr1[len(self.arr1)-1]))
        self.l3.setText(str(self.arr2[len(self.arr2)-1]))
        self.repaint()
        
    def ingresaPuntoDeWiiMote(self):
        wiiuse.motion_sensing(self.wiimotes, self.nmotes)
        wiiuse.poll(self.wiimotes, self.nmotes)
        #print self.wm.flags
        #print wiiuse.api.read_data
        """if self.wm.btns:
            if wiiuse.is_pressed(self.wm, 0x0004):
                print "B"
            """
        """if wiiuse.is_just_pressed(self.wm, 0x1000):
            print "+"
        """
        #print self.wm.accel.x
        if wiiuse.using_acc(self.wm):
            print 'roll  = %i' % self.wm.orient.roll
            print 'pitch = %i' % self.wm.orient.pitch
            print 'yaw   = %i' % self.wm.orient.yaw
        if self.b1:
            for i in range(1,len(self.arr)):
                self.arr[i-1]=self.arr[i]
            self.arr[len(self.arr)-1]=self.wm.gforce.x
            
        if self.b2:
            for i in range(1,len(self.arr1)):
                self.arr1[i-1]=self.arr1[i]
            self.arr1[len(self.arr1)-1]=self.wm.gforce.y

        if self.b3 and str(self.wm.gforce.z)!='inf':
            for i in range(1,len(self.arr2)):
                self.arr2[i-1]=self.arr2[i]
            self.arr2[len(self.arr2)-1]=self.wm.gforce.z
        self.l1.setText(str(self.arr[len(self.arr)-1]))
        self.l2.setText(str(self.arr1[len(self.arr1)-1]))
        self.l3.setText(str(self.arr2[len(self.arr2)-1]))
        ####escalando
        if self.arr[len(self.arr)-1] > self.maxG1:
            self.maxG1=self.arr[len(self.arr)-1]*1.0
        if self.arr[len(self.arr)-1] < self.minG1:
            self.minG1=self.arr[len(self.arr)-1]*1.0

        if self.arr1[len(self.arr1)-1] > self.maxG2:
            self.maxG2=self.arr1[len(self.arr1)-1]*1.0
        if self.arr1[len(self.arr1)-1] < self.minG2:
            self.minG2=self.arr1[len(self.arr1)-1]*1.0

        if self.arr2[len(self.arr2)-1] > self.maxG3:
            self.maxG3=self.arr2[len(self.arr2)-1]*1.0
        if self.arr2[len(self.arr2)-1] < self.minG3:
            self.minG3=self.arr2[len(self.arr2)-1]*1.0
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
        self.label1.setGeometry(745,90,50,50)
        self.label2 = QtGui.QLabel('TEXTO',self)
        self.label2.setGeometry(745,190,50,50)
        self.label3 = QtGui.QLabel('TEXTO',self)
        self.label3.setGeometry(745,290,50,50)
        self.Widget.setLabels(self.label1,self.label2,self.label3)
        #########
        self.boton = QtGui.QPushButton("congela eje X",self)
        self.boton.setGeometry(745,150,70,50)
        self.botonY=QtGui.QPushButton("congela eje Y",self)
        self.botonY.setGeometry(745,250,70,50)
        self.botonZ=QtGui.QPushButton("congela eje Z",self)
        self.botonZ.setGeometry(745,350,70,50)
        #self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.giracubo )
        self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.Widget.congelaG1 )
        self.botonY.connect(self.botonY,QtCore.SIGNAL('clicked()'),self.Widget.congelaG2)
        self.botonZ.connect(self.botonZ,QtCore.SIGNAL('clicked()'),self.Widget.congelaG3)
        """timer = QtCore.QTimer(self)
        timer.setInterval(0)
        #QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.Widget.ingresaPuntoAleatorio)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.Widget.ingresaPuntoDeWiiMote)
        timer.start()"""
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
