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

class WiiAccel(threading.Thread):
      def __init__(self):
            threading.Thread.__init__(self)
            self.sigue=True
      def terminar(self):
            self.sigue = False
      def run(self):
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
            """wiiuse.rumble(self.wiimotes[0], 10)
            time.sleep(0.1)
            wiiuse.rumble(self.wiimotes[0], 0)"""
            for i in range(4):
                  wiiuse.set_leds(self.wiimotes[0], wiiuse.LED[3-i])
                  time.sleep(0.2)
            self.wm = self.wiimotes[0][0]
            #iniciar Wiimote
            while self.sigue:
                  wiiuse.motion_sensing(self.wiimotes, self.nmotes)
                  wiiuse.poll(self.wiimotes, self.nmotes)
                  print wiiuse.using_acc(self.wm)
                  print "gforce \t"+str(self.wm.gforce.x)
                  print "gforce \t"+str(self.wm.gforce.y)
                  print "gforce \t"+str(self.wm.gforce.z)
                  print "accel \t"+str(self.wm.accel.x)
                  print "orient \t"+str(self.wm.orient.roll)
                  print "orient \t"+str(self.wm.orient.pitch)
                  print "orient \t"+str(self.wm.orient.yaw)
                  print "accel_calib \t"+str(self.wm.accel_calib.cal_g.x)
                  print "state \t"+str(self.wm.state)
                  print "lstate\t"+str(self.wm.lstate.orient.roll)
                  print "lstate\t"+str(self.wm.lstate.orient.pitch)
                  print "lstate\t"+str(self.wm.lstate.orient.yaw)
                  print "#"*30
                  time.sleep(0.1)

class Wiibotones(threading.Thread):
      def __init__(self,w):
            threading.Thread.__init__(self)
            self.rotX = 0
            self.rotY = 0
            self.rotZ = 0
            self.window = w
            self.sigue=True
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
            if temp != self.rotX:
                  self.rotX= temp
                  self.window.emit(SIGNAL("AccelX"), self.rotX)
            t = self.wm.gforce.y
            temp=0
            try:
                  temp = math.trunc(t)
            except:
                  temp=0
            if temp != self.rotY:
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
                  #time.sleep(0.105)
                  #wiiuse.motion_sensing(self.wiimotes,self.nmotes)
                  wiiuse.poll(self.wiimotes, self.nmotes)
                  """print self.wm.gforce.x
                  print self.wm.gforce.y
                  print self.wm.gforce.z
                  print "####" """
                  try:
                        """print self.wm.orient_threshold
                        print self.wm.accel_threshold
                        print self.wm.event
                        print "#####" """
                        BotonSuelto = str(self.wm.accel_threshold)
                        #print "thresold "+s
                        if BotonSuelto!="0":
                              if BotonSuelto=="1":
                                    print "se solto el boton 2"
                                    self.window.emit(SIGNAL("BotonSuelto"), "2")
                              if BotonSuelto=="2":
                                    print "se solto el boton 1"
                                    self.window.emit(SIGNAL("BotonSuelto"), "1")
                              if BotonSuelto=="16":
                                    print "se solto el boton -"
                                    self.window.emit(SIGNAL("BotonSuelto"), "-")
                              if BotonSuelto=="128":
                                    print "se solto el boton HOME"
                                    self.window.emit(SIGNAL("BotonSuelto"), "HOME")
                              if BotonSuelto=="4096":
                                    print "se solto el boton +"
                                    self.window.emit(SIGNAL("BotonSuelto"), "+")
                              if BotonSuelto=="8":
                                    print "se solto el boton A"
                                    self.window.emit(SIGNAL("BotonSuelto"), "A")
                              if BotonSuelto=="1024":
                                    print "se solto el boton ABAJO"
                                    self.window.emit(SIGNAL("BotonSuelto"), "ABAJO")
                              if BotonSuelto=="512":
                                    print "se solto el boton DERECHA"
                                    self.window.emit(SIGNAL("BotonSuelto"), "DERECHA")
                              if BotonSuelto=="2048":
                                    print "se solto el boton ARRIBA"
                                    self.window.emit(SIGNAL("BotonSuelto"), "ARRIBA")
                              if BotonSuelto=="256":
                                    print "se solto el boton IZQUIERDA"
                                    self.window.emit(SIGNAL("BotonSuelto"), "IZQUIERDA")
                              if BotonSuelto=="4":
                                    print "se solto el boton B"
                                    self.window.emit(SIGNAL("BotonSuelto"), "B")
                              if BotonSuelto=="3":
                                    print "se solto el boton 1 y 2"
                                    self.window.emit(SIGNAL("BotonSuelto"), "1 y 2")
                        BotonPresionado=str(self.wm.orient_threshold)[:4]
                        if BotonPresionado !="0.0":
                              #print "se presiono un boton -> "+str(self.wm.orient_threshold)
                              if BotonPresionado =="2.86":
                                    print "arriba"
                                    self.window.emit(SIGNAL("Boton"), "ARRIBA")
                                    #self.window.repaint()
                              if BotonPresionado =="1.43":
                                    print "abajo"
                                    self.window.emit(SIGNAL("Boton"), "ABAJO")
                              if BotonPresionado =="7.17":
                                    print "derecha"
                                    self.window.emit(SIGNAL("Boton"), "DERECHA")
                              if BotonPresionado =="3.58":
                                    print "izquierda"
                                    self.window.emit(SIGNAL("Boton"), "IZQUIERDA")
                              if BotonPresionado =="1.12":
                                    print "A"
                                    self.window.emit(SIGNAL("Boton"), "A")
                              if BotonPresionado =="5.60":
                                    print "B"
                                    self.window.emit(SIGNAL("Boton"), "B")
                              if BotonPresionado =="2.24":
                                    print "-"
                                    self.window.emit(SIGNAL("Boton"), "-")
                              if BotonPresionado =="1.79":
                                    print "Home"
                                    self.window.emit(SIGNAL("Boton"), "HOME")
                              if BotonPresionado =="5.73":
                                    print "+"
                                    self.window.emit(SIGNAL("Boton"), "+")
                              if BotonPresionado =="2.80":
                                    print "1"
                                    self.window.emit(SIGNAL("Boton"), "1")
                              if BotonPresionado =="1.40":
                                    print "2"
                                    self.window.emit(SIGNAL("Boton"), "2")
                              if BotonPresionado =="2.75":
                                    print "1 y 2"
                                    self.window.emit(SIGNAL("Boton"), "1 y 2")
                              """if BotonPresionado =="1.83" or BotonPresionado =="9.18":
                                    print "1 y 2"
                                    self.window.emit(SIGNAL("Boton"), "1 y 2")"""
                        #wiiuse.motion_sensing(self.wiimotes, 1)
                        """print "gforce "+str(self.wm.gforce.x)
                        print "gforce "+str(self.wm.gforce.y)
                        print "gforce "+str(self.wm.gforce.z)
                        print "accel "+str(self.wm.accel.x)
                        print "orient "+str(self.wm.orient.roll)
                        print "orient "+str(self.wm.orient.pitch)
                        print "orient "+str(self.wm.orient.yaw)"""
                        #print "accel_calib "+str(self.wm.accel_calib.cal_g.x)
                        #print "state "+str(self.wm.state)
                        """print "lstate"+str(self.wm.lstate.orient.roll)
                        print "lstate"+str(self.wm.lstate.orient.pitch)
                        print "lstate"+str(self.wm.lstate.orient.yaw)"""
                        #wiiuse.motion_sensing(self.wiimotes, 0)
                  except :
                    print "error"
class MyWindow(QtGui.QWidget):
      def __init__(self, *args):
            QtGui.QWidget.__init__(self, *args)
            self.setWindowTitle('Hilos botones y Accel')
            self.resize(400, 400)
            self.hilo = Wiibotones(self)
            #self.hilo1 = WiiAccel()
            self.hilo.start()
            #self.hilo1.start()
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
            #self.connect(self, SIGNAL("didSomething"),self.update_label)
            self.connect(self, SIGNAL("Boton"),self.QueBoton)
            self.connect(self, SIGNAL("BotonSuelto"),self.BotonSuelto)
            self.connect(self, SIGNAL("AccelX"),self.MueveX)
            self.connect(self, SIGNAL("AccelY"),self.MueveY)
            self.connect(self, SIGNAL("AccelZ"),self.MueveZ)
            self.connect(self, QtCore.SIGNAL('triggered()'), self.closeEvent)
      def nada(self):
            print "nada"
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
      #w.hilo.terminar()
      sys.exit(app.exec_())
      

"""t = WiiAccel()
t.start()
t.join()"""
"""
t1 = ew()   
t1.start() 
#t1.join()

print "asada"
time.sleep(4)
print "hilo principal "
time.sleep(4)
print "hilo principal "
time.sleep(4)
print "hilo principal "
time.sleep(4)
print "hilo principal "
time.sleep(4)
print "hilo principal "
time.sleep(4)
print "hilo principal "
time.sleep(4)
print "hilo principal "
time.sleep(4)

print "hilo principal final"
t1.terminar()"""
