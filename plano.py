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
        self.cubeVtxArray = array(
            [
                #plano
                [-0.5, -0.5, 0.0],
                [0.5, -0.5, 0.0],
                [0.5, 0.5, 0.0],
                [-0.5, 0.5, 0.0]
            ])
        self.cubeIdxArray = [ 0, 1, 2, 3, 4]
        self.cubeClrArray = [
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [1.0, 1.0, 0.0]
            ]

    def spin(self):
        #self.xRotDeg = (self.xRotDeg  + 2) % 360.0
        self.yRotDeg = (self.yRotDeg  + 5) % 360.0
        self.zRotDeg = (self.zRotDeg  + 2) % 360.0
        self.parent.statusBar().showMessage('rotation %f' % self.yRotDeg)
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
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.glWidget.spin)
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
        QtGui.qApp.quit()

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
