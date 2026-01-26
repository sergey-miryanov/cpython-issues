import _thread
import threading

def task():
    pass

# _thread.start_new_thread(task, ())
_thread.start_joinable_thread(task, ()).join()
