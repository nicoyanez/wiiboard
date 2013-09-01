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
            """wiiuse.rumble(self.wiimotes[0], 10)
            time.sleep(0.1)
            wiiuse.rumble(self.wiimotes[0], 0)"""
            for i in range(4):
                  wiiuse.set_leds(self.wiimotes[0], wiiuse.LED[3-i])
                  time.sleep(0.2)
            self.wm = self.wiimotes[0][0]
            #iniciar Wiimote
            while self.sigue:
                  time.sleep(0.1)
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

class Wiibotones(threading.Thread):
      def __init__(self):
            threading.Thread.__init__(self)
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
            wiiuse.rumble(self.wiimotes[0], 10)
            time.sleep(0.1)
            wiiuse.rumble(self.wiimotes[0], 0)
            self.wm = self.wiimotes[0][0]
            #iniciar Wiimote
      def terminar(self):
            self.sigue = False
      def run(self):
            while self.sigue:
                  time.sleep(0.105)
                  #wiiuse.motion_sensing(self.wiimotes,self.nmotes)
                  wiiuse.poll(self.wiimotes, self.nmotes)
                  try:
                        """print self.wm.orient_threshold
                        print self.wm.accel_threshold
                        print self.wm.event
                        print "#####"
                        print self.wm.gforce.x
                        print self.wm.gforce.y
                        print self.wm.gforce.z"""
                        if str(self.wm.orient_threshold)[:3] !="0.0":
                              #print "se presiono un boton -> "+str(self.wm.orient_threshold)
                              if str(self.wm.orient_threshold)[:4] =="2.86":
                                    print "arriba"
                              if str(self.wm.orient_threshold)[:4] =="1.43":
                                    print "abajo"
                              if str(self.wm.orient_threshold)[:4] =="7.17":
                                    print "derecha"
                              if str(self.wm.orient_threshold)[:4] =="3.58":
                                    print "izquierda"
                              if str(self.wm.orient_threshold)[:4] =="1.12":
                                    print "A"
                              if str(self.wm.orient_threshold)[:4] =="5.60":
                                    print "B"
                              if str(self.wm.orient_threshold)[:4] =="2.24":
                                    print "-"
                              if str(self.wm.orient_threshold)[:4] =="1.79":
                                    print "Home"
                              if str(self.wm.orient_threshold)[:4] =="5.73":
                                    print "+"
                              if str(self.wm.orient_threshold)[:4] =="2.80":
                                    print "1"
                              if str(self.wm.orient_threshold)[:4] =="1.40":
                                    print "2"
                              if str(self.wm.orient_threshold)[:4] =="1.83" or str(self.wm.orient_threshold)[:4] =="9.18":
                                    print "1 y 2"
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
                        wiiuse.motion_sensing(self.wiimotes, 0)"""
                  except :
                    print "error"

t = WiiAccel()
t.start()
t.join()
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
