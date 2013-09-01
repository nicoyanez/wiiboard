import threading
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import *

import random

from ctypes  import *

import wiiuse
import time
import os
import math

class Wiibotones(threading.Thread):
      def __init__(self,w):
            threading.Thread.__init__(self)
            self.rotX = 0
            self.rotY = 0
            self.rotZ = 0
            self.window = w
            self.sigue=True
            self.releasedButton ={"1":"2","2":"1","16":"-","128":"HOME","4096":"+","8":"A","1024":"ABAJO",
                                  "512":"DERECHA","2048":"ARRIBA","256":"IZQUIERDA","4":"B","3":"1+2"}
            self.pressedButton  ={"2.86":"ARRIBA","1.43":"ABAJO","7.17":"DERECHA","3.58":"IZQUIERDA","1.12":"A",
                                  "5.60":"B","2.24":"-","1.79":"HOME","5.73":"+","2.80":"1","1.40":"2","2.75":"1+2"}
            #iniciar Wiimote
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
            time.sleep(0.1)
            wiiuse.rumble(self.wiimotes[0], 0)
            self.wm = self.wiimotes[0][0]
            #iniciar Wiimote
      def terminar(self):
            self.sigue = False
      def muestraAccel(self):
            wiiuse.motion_sensing(self.wiimotes,self.nmotes)
            wiiuse.poll(self.wiimotes, self.nmotes)
            t = self.wm.gforce.x
            temp=0
            try:
                  temp = math.trunc(t)
            except:
                  temp=0
            if temp< (self.rotX-3) or temp> (self.rotX+3):
                  self.rotX= temp
                  self.window.emit(SIGNAL("AccelX"), self.rotX)
            
            t = self.wm.gforce.y
            temp=0
            try:
                  temp = math.trunc(t)
            except:
                  temp=0
            if temp < (self.rotY-3) or temp > (self.rotY+3):
                  self.rotY= temp
                  self.window.emit(SIGNAL("AccelY"), self.rotY)
            t = self.wm.gforce.z
            temp=0
            try:
                  temp = math.trunc(t)
            except:
                  temp=0
            if temp != self.rotZ:
                  self.rotZ= temp
                  self.window.emit(SIGNAL("AccelZ"), self.rotZ)
      def run(self):
            while self.sigue:
                  self.muestraAccel()
                  wiiuse.poll(self.wiimotes, self.nmotes)
                  try:
                        rb = str(self.wm.accel_threshold)
                        if self.releasedButton.has_key(rb):
                              self.window.emit(SIGNAL("BotonSuelto"), self.releasedButton[rb])
                        pb=str(self.wm.orient_threshold)[:4]
                        if self.pressedButton.has_key(pb):
                              self.window.emit(SIGNAL("Boton"), self.pressedButton[pb])
                  except :
                    print "error"
class MyWindow(QtGui.QWidget):
      def __init__(self, *args):
            QtGui.QWidget.__init__(self, *args)
            self.setWindowTitle('Hilos botones y Accel')
            self.resize(400, 400)
            self.hilo = Wiibotones(self)
            self.hilo.start()
            ##slider##
            self.sldX = QtGui.QSlider(QtCore.Qt.Horizontal, self)
            self.sldX.setRange(-180, 180)
            self.sldY = QtGui.QSlider(QtCore.Qt.Vertical, self)
            self.sldY.setRange(-180, 180)
            ##slider##
            self.label = QtGui.QLabel(" Algo")
            self.label.setToolTip('Representa el boton  <b>PRESIONADO</b> Actualmente en el WII')
            self.label.setFont(QFont('Sans-serif',20))
            self.label1 = QtGui.QLabel(" Algo")
            self.label1.setToolTip('Representa el <b>ULTIMO BOTON SUELTO</b> en el WII')
            self.label1.setFont(QFont('Sans-serif',20))
            self.label2 = QtGui.QLabel(" Algo")
            self.label2.setToolTip('Representa el <b>Accel X</b> en el WII')
            self.label2.setFont(QFont('Sans-serif',20))
            self.label3 = QtGui.QLabel(" Algo")
            
            self.label3.setToolTip('Representa el <b>Accel Y</b> en el WII')
            self.label3.setFont(QFont('Sans-serif',20))
            self.label4 = QtGui.QLabel(" Algo")
            self.label4.setToolTip('Representa el <b>Accel Z</b> en el WII')
            self.label4.setFont(QFont('Sans-serif',20))

            layout = QVBoxLayout()
            layout.addWidget(self.label)
            layout.addWidget(self.label1)
            
            layout.addWidget(self.label2)
            layout.addWidget(self.sldX)
            layout.addWidget(self.label3)
            layout.addWidget(self.sldY)
            layout.addWidget(self.label4)
            
            self.setLayout(layout)
            
            self.connect(self, SIGNAL("Boton"),self.QueBoton)
            self.connect(self, SIGNAL("BotonSuelto"),self.BotonSuelto)
            self.connect(self, SIGNAL("AccelX"),self.MueveX)
            self.connect(self, SIGNAL("AccelY"),self.MueveY)
            self.connect(self, SIGNAL("AccelZ"),self.MueveZ)
            self.connect(self, QtCore.SIGNAL('triggered()'), self.closeEvent)

      def closeEvent(self, event):
            print "terminando Hilo"
            self.hilo.terminar()
            #self.hilo1.terminar()
            time.sleep(0.2)
            print "EL HILO HA MUERTO"
      def QueBoton(self,nombre):
            self.label.setText("se presiono " + nombre)
            self.label1.setText("")
      def BotonSuelto(self,nombre):
            self.label1.setText("se solto " + nombre)
            self.label.setText("")
      def MueveX(self,dato):
            self.label2.setText("Accel <b>X<b> = " + str(dato))
            self.sldX.setValue(dato)
      def MueveY(self,dato):
            self.label3.setText("Accel <b>Y<b> = " + str(dato))
            self.sldY.setValue(dato)
      def MueveZ(self,dato):
            self.label4.setText("Accel <b>Z<b> = " + str(dato))
if __name__ == "__main__":
      app = QtGui.QApplication(sys.argv)
      w = MyWindow() 
      w.show()
      sys.exit(app.exec_())
