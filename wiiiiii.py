import pywiiuse as wiiuse
import time


nmotes = 1
wiimotes = wiiuse.wiiuse_init(nmotes)
found = wiiuse.wiiuse_find(wiimotes, nmotes, 5)
if not found:
    print 'not found'
    sys.exit(1)
connected = wiiuse.wiiuse_connect(wiimotes, nmotes)
if connected:
    print 'Connected to %i wiimotes (of %i found).' % (connected, found)
else:
    print 'failed to connect to any wiimote.'
    sys.exit(1)
#print wiimotes
for i in range(nmotes):
    wiiuse.wiiuse_set_leds(wiimotes[i], wiiuse.wiiuse_LED[i])
    wiiuse.wiiuse_status(wiimotes[0])
    wiiuse.wiiuse_set_ir(wiimotes[0], 1)
    wiiuse.wiiuse_set_ir_vres(wiimotes[i], 1000, 1000)
wiiuse.wiiuse_rumble(wiimotes[0], 10)
time.sleep(0.5)
wiiuse.wiiuse_rumble(wiimotes[0], 0)

