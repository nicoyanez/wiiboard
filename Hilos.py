import threading
import time
import random
from PyQt4 import QtCore
import PyQt4
  
class ew(threading.Thread):  
      def __init__(self,n):
          threading.Thread.__init__(self)
          self.n=n
          #iniciar Wiimote
          #iniciar Wiimote
  
      def run(self):
          for i in range(10):
              time.sleep(self.n)
              print "Soy el hilo "+str(self.n)+" en mi iteracion "+str(i)
              QtCore.SIGNAL("abdula")
              #if botones acelerometro
              #envio de senales Qt

t1 = ew(1)   
t2 = ew(1)
t3 = ew(1)   
t4 = ew(1)

t1.start() 
t2.start()
t3.start() 
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
