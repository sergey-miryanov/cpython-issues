import multiprocessing

q = multiprocessing.Queue()

try:

    q.put(lambda: None)
    print("Success!")
except Exception:
    print("Failure")
