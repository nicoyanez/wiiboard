import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
from numpy import array

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.xRot = 0.0
        self.yRotDeg = 0.0
        self.zRot = 0.0

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
        glScale(20.0, 20.0, 20.0)
        #glRotate(self.yRotDeg, 0.2, 1.0, 0.3)
        ###############################
        glRotate(self.yRotDeg, 0.0, 1.0, 0.0)
        glRotate(self.xRot, 1.0, 0.0, 0.0)
        glRotate(self.zRot, 0.0, 0.0, 1.0)
        glTranslate(-0.5, -0.5, -0.5)
        ###############################
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointerf(self.cubeVtxArray)
        glColorPointerf(self.cubeClrArray)
        glDrawElementsui(GL_QUADS, self.cubeIdxArray)

    def initGeometry(self):
        self.cubeVtxArray = array(
            [[0.0, 0.0, 0.0],
            [0.5, 0.0, 0.0],
            [0.5, 0.5, 0.0],
            [0.0, 0.5, 0.0],
            [0.0, 0.0, 1.0],
            [0.5, 0.0, 1.0],
            [0.5, 0.5, 1.0],
            [0.0, 0.5, 1.0]])
        self.cubeIdxArray = [
            0, 1, 2, 3,
            3, 2, 6, 7,
            1, 0, 4, 5,
            2, 1, 5, 6,
            0, 3, 7, 4,
            7, 6, 5, 4 ]
        self.cubeClrArray = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 1.0],
            [0.0, 1.0, 1.0 ]]

    def spin(self):
        self.xRot = (self.xRot  + 2) % 360.0
        self.yRotDeg = (self.yRotDeg  + 2) % 360.0
        self.zRot = (self.zRot  + 2) % 360.0
        #emit(QtCore.SIGNAL("xRotationChanged"), xRot)
        self.parent.statusBar().showMessage('rotation x %f y %f z %f' % (self.xRot , self.yRotDeg , self.zRot))
        self.updateGL()

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(500, 500)
        self.setWindowTitle('GL Cube Test')
        self.initActions()
        self.initMenus()
        self.glWidget = GLWidget(self)
        self.setCentralWidget(self.glWidget)
        #########
        self.boton = QtGui.QPushButton("mueve",self)
        self.boton.setGeometry(10,30,50,20)
        self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.giracubo )
        timer = QtCore.QTimer(self)
        timer.setInterval(1)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.glWidget.spin)
        timer.start()
    def initActions(self):
        self.exitAction = QtGui.QAction('Quit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.connect(self.exitAction, QtCore.SIGNAL('triggered()'), self.close)

    def giracubo(self):
        #glWidget.spin()
        print "girando"
        self.glWidget.spin()

    def initMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.exitAction)

    def close(self):
        QtGui.qApp.quit()

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
