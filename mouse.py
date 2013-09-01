import win32api, win32con
import time
import math
win32api.SetCursorPos((100,5))
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
for i in range(50):
    x = 500+math.sin(math.pi*i/100)*500
    y = 500+math.cos(i)*100
    #win32api.SetCursorPos((math.trunc(x),math.trunc(y)))
    try:
        print " el mouse "+str(win32api.GetCursorPos())
        win32api.DragFinish(x,y)
        #print " el mouse "+str(win32api.mouse_event.__str__)
    except(e):
        print "error "+str(e)
    #win32api.SetCursorPos((math.trunc(x),math.trunc(y)))
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    #print str(math.trunc(x))+" \t"+str(math.trunc(y))
    time.sleep(.01)
#win32api.SetCursorPos((100,5))
#win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
