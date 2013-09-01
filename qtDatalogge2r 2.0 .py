import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import random

class Grafico(QtGui.QWidget):
    def __init__(self):
        super(Grafico, self).__init__()
        self.label = PyQt4.QtGui.QLabel("algo")
        self.label.move(400, 410)
        self.maxG1 =800
        self.b1 = True
        self.b2 = True
        self.b3 = True
        self.arr = [0 for i in range(0,350)]
        self.arr1 = [random.randint(10,100) for i in range(0,350)]
        self.arr2 = [random.randint(10,100) for i in range(0,350)]
        """super(Example, self).__init__()
        self.initUI()"""
    """def initUI(self):
        self.setGeometry(300, 300, 280, 270)
        self.setWindowTitle('Pen styles')
        self.show()"""

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()
    
    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 1.5, QtCore.Qt.DotLine)
        qp.setPen(pen)
        for i in range(1,len(self.arr)):
            y1 = 150-100.0*self.arr[i-1]/self.maxG1
            y2 = 150-100.0*self.arr[i]/self.maxG1
            qp.drawLine(10+2*(i-1),y1 , 10+2*i,y2 )
            """qp.setPen(QtGui.QColor(255, 2, 3))
            qp.setFont(QtGui.QFont('Decorative', 20))
            qp.drawText(750,150,str(self.arr[i]))"""
        """qp.drawLine(10, 20, 50, 110)
        qp.drawLine(50, 110, 250, 360)
        qp.drawLine(250, 360, 250, 160)
        qp.drawLine(250, 160, 500, 260)"""
        
    def ingresaPunto(self,dato):
        for i in range(1,len(self.arr)):
            self.arr[i-1]=self.arr[i]
        self.arr[len(self.arr)-1]=dato
        
    def congelaG1(self):
        self.b1=not self.b1
    
    def ingresaPuntoAleatorio(self):
        if self.b1:
            for i in range(1,len(self.arr)):
                self.arr[i-1]=self.arr[i]
            self.arr[len(self.arr)-1]=random.randint(1,800)
        self.repaint()

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(800, 500)
        self.setWindowTitle('Data Logger')
        self.initActions()
        self.initMenus()
        self.Widget = Grafico()
        self.setCentralWidget(self.Widget)
        """self.glWidget = GLWidget(self)
        self.setCentralWidget(self.glWidget)"""
        #########
        self.boton = QtGui.QPushButton("congela",self)
        self.boton.setGeometry(745,30,50,50)
        #self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.giracubo )
        self.boton.connect(self.boton,QtCore.SIGNAL('clicked()'), self.Widget.congelaG1 )
        timer = QtCore.QTimer(self)
        timer.setInterval(5)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.Widget.ingresaPuntoAleatorio)
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
