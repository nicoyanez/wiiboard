import  wiiuse
import time


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
#print wiimotes
for i in range(nmotes):
    wiiuse.set_leds(wiimotes[i], wiiuse.LED[i])
    wiiuse.status(wiimotes[0])
    wiiuse.set_ir(wiimotes[0], 1)
    wiiuse.set_ir_vres(wiimotes[i], 1000, 1000)
wiiuse.rumble(wiimotes[0], 10)
time.sleep(0.5)
wiiuse.rumble(wiimotes[0], 0)

