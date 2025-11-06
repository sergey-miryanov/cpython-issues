import threading
from concurrent import interpreters

interp = interpreters.create()
interp.exec(f"""if True:
    import threading
    import time

    done = False

    def notify_fini():
        global done
        done = True
        raise Exception ('ahaha') # <-------
        t.join()
    threading._register_atexit(notify_fini)

    def task():
        while not done:
            time.sleep(0.1)
    t = threading.Thread(target=task)
    t.start()
""")
interp.close()
