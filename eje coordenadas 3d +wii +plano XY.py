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



class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.xRotDeg = 0.0
        self.yRotDeg = 0.0
        self.zRotDeg = 0.0
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

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0,  0))
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
        glTranslate(0.0, 0.0, -50.0)
        glScale(15.0, 15.0, 15.0)
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
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0]
            ])"""
        self.cubeVtxArray = array(
            [
                #X
                [0.1, 0.1, 0.0],
                [0.0, 0.1, 0.0],
                [0.0, 1.1, 0.0],
                [0.1, 1.1, 0.0],
                #y
                [0.1, 0.0, 0.0],
                [0.1, 0.1, 0.0],
                [1.1, 0.1, 0.0],
                [1.1, 0.0, 0.0],
                #z              
                [0.0, 0.0, 0.0],
                [0.0, 0.1, 0.0],
                [0.0, 0.1, 1.0],
                [0.0, 0.0, 1.0],
                #plano
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.1, 0.0, 1.0],
                [1.1, 0.0, 0.0]
            ])
        """self.cubeIdxArray = [
            0, 1, 2, 3,
            3, 2, 6, 7,
            1, 0, 4, 5,
            2, 1, 5, 6
            ]"""
        self.cubeIdxArray = [ 0, 1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16]
        self.cubeClrArray = [
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],

            [0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],

            [1.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],

            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0]
            ]

    def spin(self):
        self.xRotDeg = (self.xRotDeg  + 2) % 360.0
        self.yRotDeg = (self.yRotDeg  + 5) % 360.0
        self.zRotDeg = (self.zRotDeg  + 2) % 360.0
        self.parent.statusBar().showMessage('rotation %f' % self.yRotDeg)
        self.updateGL()

    def update(self):
        wiiuse.motion_sensing(self.wiimotes, self.nmotes)
        wiiuse.poll(self.wiimotes, self.nmotes)
        #print "\t######"
        #print self.wm.gforce.x
        if str(self.wm.gforce.x)!='inf':
            self.zRotDeg = 360-self.wm.gforce.x
        if str(self.wm.gforce.y)!='inf':
            self.xRotDeg = 360-self.wm.gforce.y
        """if str(self.wm.gforce.z)!='inf':
            self.yRotDeg = self.wm.gforce.z"""
        self.parent.statusBar().showMessage('x %f - y %f - z %f' % (self.xRotDeg,self.yRotDeg,self.zRotDeg))
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
        timer = QtCore.QTimer(self)
        timer.setInterval(1)
        #QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.glWidget.spin)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.glWidget.update)
        timer.start()

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
        #wiiuse.disconnect(self.glWidget.wm)
        #self.glWidget.wiimotes.disconnect()
        QtGui.qApp.quit()
        os.sys.exit(0)

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
