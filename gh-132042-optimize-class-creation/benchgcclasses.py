
import gc
import os
import time

clock = time.process_time


def make_classes(N):
    classes = []
    for i in range(N):
        class C:
            pass
        classes.append(C)
    return classes


def run():
    classes = make_classes(100_000)
    times = []
    for i in range(10):
        t1 = clock()
        gc.collect()
        dt = clock() - t1
        times.append(dt)

    print("GC time: %.1f ms" % (min(times) * 1e3,))
    print("RSS:")
    # os.system("ps u --pid %d" % (os.getpid(),))


run()
