import time
import os
import subprocess as sp
rows, cols = os.popen('stty size', 'r').read().split()
sp.call('clear', shell=True)
for i in range(0, int(cols)):
    print('-', end='')
for i in range(0, int(rows)):
    print('|', end='')
    for i in range(0, int(cols) - 2):
        print(" ", end='')
    print('|')
for i in range(0, int(cols)):
    print('-', end='')
