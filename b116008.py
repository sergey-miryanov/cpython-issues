import faulthandler
import signal
faulthandler.register(signal.SIGUSR1)

import threading
import time

def rec(x):
    a = 1
    b = 2
    c = 3
    if x>0: return rec(x-1)

def loop():
    while True:
        rec(123)

threading.Thread(target=loop).start()

time.sleep(1000)
