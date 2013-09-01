import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.setGeometry(300, 300, 280, 270)
        self.setWindowTitle('Pen styles')
        self.show()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()
        
    def drawLines(self, qp):
      
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(20, 40, 250, 40)

        pen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(20, 80, 250, 80)

        pen.setStyle(QtCore.Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 120, 250, 120)

        pen.setStyle(QtCore.Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(20, 160, 250, 160)

        pen.setStyle(QtCore.Qt.DashDotDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 200, 250, 200)

        pen.setStyle(QtCore.Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        qp.drawLine(20, 240, 250, 240)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(500, 500)
        self.setWindowTitle('Data Logger')
        self.initActions()
        self.initMenus()
        """self.glWidget = GLWidget(self)
        self.setCentralWidget(self.glWidget)"""
        #########
        self.boton = QtGui.QPushButton("mueve",self)
        self.boton.setGeometry(10,30,50,20)
        #self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.giracubo )
        """timer = QtCore.QTimer(self)
        timer.setInterval(1)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.glWidget.spin)
        timer.start()"""
        """##################
        qp = QtGui.QPainter()
        qp.begin(self)
        
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(20, 40, 250, 40)

        pen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(20, 80, 250, 80)

        pen.setStyle(QtCore.Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 120, 250, 120)

        pen.setStyle(QtCore.Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(20, 160, 250, 160)

        pen.setStyle(QtCore.Qt.DashDotDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 200, 250, 200)

        pen.setStyle(QtCore.Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        qp.drawLine(20, 240, 250, 240)
        qp.end()
        ##################"""
        
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
    """app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())"""
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
