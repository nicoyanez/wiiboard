import time
import wiiuse
import sys
import ctypes
from ctypes import Structure, c_byte
#######iniciando Wiiii
####################
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
    wiiuse.set_ir(wiimotes[0], 1)
    wiiuse.set_ir_vres(wiimotes[i], 1000, 1000)
wiiuse.rumble(wiimotes[0], 10)
time.sleep(0.1)
wiiuse.rumble(wiimotes[0], 0)
wm = wiimotes[0][0]
while True:
    wiiuse.motion_sensing(wiimotes,nmotes)
    wiiuse.poll(wiimotes, nmotes)
    print wm.ir.num_dots
    print wm.ir.x
    print wm.ir.y
    print "##"
