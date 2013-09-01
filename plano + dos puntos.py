import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
from numpy import array

import wiiuse
import time
import os
import random
import threading
from math import sqrt,acos
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
            self.nmotes = 2
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
                  wiiuse.status(self.wiimotes[i])
                  wiiuse.set_ir(self.wiimotes[i], 1)
                  wiiuse.set_ir_vres(self.wiimotes[i], 1000, 1000)
            wiiuse.rumble(self.wiimotes[0], 10)
            wiiuse.rumble(self.wiimotes[1], 10)
            time.sleep(0.1)
            wiiuse.rumble(self.wiimotes[0], 0)
            wiiuse.rumble(self.wiimotes[1], 0)
            self.wm = self.wiimotes[0][0]
            self.wm2 = self.wiimotes[0][1]
            #iniciar Wiimote
      def terminar(self):
            self.sigue = False

      def ir_points(self):
            try:
                wiiuse.motion_sensing(self.wiimotes,self.nmotes)
                wiiuse.poll(self.wiimotes, self.nmotes)
                puntosx=[]
                puntosy=[]
                for b in self.wm.ir.dot:
                    if b.rx!=0 and b.rx<1030 and b.rx>0:
                        puntosx.append(b.rx)
                for a in self.wm2.ir.dot:
                    if a.rx!=0 and a.rx<800 and  a.rx>0:
                        puntosy.append(a.rx)
                puntos=[]
                for i in range(0,2):
                    #qp.drawPoint(puntosx[i],puntosy[i])
                    puntos.append(puntosx[i])
                    puntos.append(puntosy[i])
            except:
                print "error de ir"
            return puntos
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
      def giraPlano(self):
          #self.window.glWidget.escala= random.randint(10,500)
          #self.window.glWidget.repaintGL()
          #self.window.glWidget.updateGL()
          p = self.ir_points()
          if len(p)==4:
              #print (int)(sqrt( (p[2]-p[0])**2 + (p[3]-p[1])**2 ))
              self.window.glWidget.escala = (int)(sqrt( (p[2]-p[0])**2 + (p[3]-p[1])**2 ))
              #print (int)(sqrt( (p[2]-p[0])**2 + (p[3]-p[1])**2 ))
              #self.window.glWidget.escala= random.randint(10,500)
              #print "calculando"
              #self.window.glWidget.updateGL()
      def run(self):
            while self.sigue:
                  #self.muestraAccel()
                  #print self.ir_points()
                  wiiuse.poll(self.wiimotes, self.nmotes)
                  try:
                        rb = str(self.wm.accel_threshold)
                        if self.releasedButton.has_key(rb):
                              self.window.emit(SIGNAL("BotonSuelto"), self.releasedButton[rb])
                        pb=str(self.wm.orient_threshold)[:4]
                        if self.pressedButton.has_key(pb):
                              self.window.emit(SIGNAL("Boton"), self.pressedButton[pb])
                        self.giraPlano()
                        self.window.glWidget.updateGL()
                  except :
                    print "error RUN"

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.xRotDeg = 0.0
        self.yRotDeg = 0.0
        self.zRotDeg = 0.0
        self.escala  = 3.0

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0,  150))
        self.initGeometry()
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        if height == 0: height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslate( 0.0, 0.0, -50.0)
        porcentaje= self.escala*100/768
        print porcentaje
        #glScale( 5.0*porcentaje, 5.0*porcentaje, 5.0*porcentaje )
        #glScale( 10.0, 10.0, 10.0 )
        #print porcentaje
        ############
        glRotate(self.xRotDeg, 1.0, 0.0, 0.0)
        glRotate(self.yRotDeg, 0.0, 1.0, 0.0)
        glRotate(self.zRotDeg, 0.0, 0.0, 1.0)
        #############
        #glTranslate(-0.5, -0.5, -0.5)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointerf(self.cubeVtxArray)
        glColorPointerf(self.cubeClrArray)
        glDrawElementsui(GL_QUADS, self.cubeIdxArray)

    def initGeometry(self):
        """self.cubeVtxArray = array(
            [
                #plano
                [-0.5, -0.5, 0.0],
                [0.5, -0.5, 0.0],
                [0.5, 0.5, 0.0],
                [-0.5, 0.5, 0.0]
            ])"""
        self.cubeVtxArray = array(
            [
                #plano
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0]
            ])
        self.cubeIdxArray = [ 0, 1, 2, 3]
        self.cubeClrArray = [
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [1.0, 1.0, 0.0]
            ]

    def spin(self):
        #self.xRotDeg = (self.xRotDeg  + 2) % 360.0
        #self.yRotDeg = (self.yRotDeg  + 5) % 360.0
        #self.zRotDeg = (self.zRotDeg  + 2) % 360.0
        #self.parent.statusBar().showMessage('rotation %f' % self.yRotDeg)
        self.updateGL()

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(500, 500)
        self.setWindowTitle('Eje de coordenadas 3D')
        self.initActions()
        self.initMenus()
        self.glWidget = GLWidget(self)
        self.setCentralWidget(self.glWidget)
        self.hilo = Wiibotones(self)
        self.hilo.start()
        """timer = QtCore.QTimer(self)
        timer.setInterval(1)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.glWidget.spin)
        timer.start()"""

    def initActions(self):
        self.exitAction = QtGui.QAction('Quit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.connect(self.exitAction, QtCore.SIGNAL('triggered()'), self.closeEvent)


    def initMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.exitAction)

    def closeEvent(self, event):
        print "terminando Hilo"
        self.hilo.terminar()
        #self.hilo1.terminar()
        time.sleep(0.2)
        print "EL HILO HA MUERTO"

    def update(self):
        return 1

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            print "dasa"
            self.close()
        if e.key() == QtCore.Qt.Key_Left:
            print "izq"

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
