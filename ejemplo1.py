import pygame
import wiiuse.pygame_wiimote as pygame_wiimote
import sys
import time
import os

if os.name != 'nt': print 'press 1&2'
pygame_wiimote.init(1, 5) # look for 1, wait 5 seconds
n = pygame_wiimote.get_count() # how many did we get?

if n == 0:
    print 'no wiimotes found'
    sys.exit(1)
