import time
import wiiuse
import sys
import ctypes
from ctypes import Structure, c_byte
#######iniciando Wiiii
####################
class b(Structure):
    _fields_ = [('a', c_byte*32) ]
nmotes = 1
wiimotes = wiiuse.init(nmotes)
found = wiiuse.find(wiimotes, nmotes, 5)
if not found:
    print 'not found'
    sys.exit(1)
connected = wiiuse.connect(wiimotes, nmotes)
if connected:
    print 'Connected to %i wiimotes (of %i found).' % (connected, found)
else:
    print 'failed to connect to any wiimote.'
    sys.exit(1)
for i in range(nmotes):
    wiiuse.set_leds(wiimotes[i], wiiuse.LED[i])
    wiiuse.status(wiimotes[0])
    #wiiuse.set_orient_threshold
    wiiuse.set_ir(wiimotes[0], 1)
    wiiuse.set_ir_vres(wiimotes[i], 1000, 1000)
wiiuse.rumble(wiimotes[0], 10)
time.sleep(0.1)
wiiuse.rumble(wiimotes[0], 0)
wm = wiimotes[0][0]
estructura = b()
while True:
    time.sleep(0.1)
    wiiuse.motion_sensing(wiimotes,nmotes)
    wiiuse.poll(wiimotes, nmotes)
    #print wm.accel_threshold
    try:
        if str(wm.orient_threshold)[:4] !="0.0":
            print "#####"
            #print str(wm.orient_threshold)[:3]
            print str(wm.orient_threshold)[:4]
            print hex(wm.accel_threshold)
            print str(wm.accel_threshold)
            print str(wm.event)
            print str(wm.gforce.x)
        #b.a= wm.event_buf
        #print b.a
        """for estructura in wm.event_buf:
            print estructura
            print sys.getsizeof(estructura)
        """
        #print wm.event_buf
        if wm.btns:
            for name,b in wiiuse.button.items():
                if wiiuse.is_just_pressed(wm, b):
                    print "algo se apreto"
        if wiiuse.using_acc(wm):
            print "acel"
    except :
        print "error"
    #print wm.gforce.x
    """print wiiuse.using_acc(wm)
    print wm.btns"""


#wiiuse.motion_sensing(wiimotes, 0)
###############################
#######iniciando wii
