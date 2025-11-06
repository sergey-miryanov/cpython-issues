
from contextlib import redirect_stderr
from io import StringIO
import sys
from threading import Thread
import time


class Foo:
    def __repr__(self):
        return "Foo"

def thread1():
    with redirect_stderr(StringIO()):
        raise Exception('test')

def main():
    for i in range(1000):
        t1 = Thread(target=thread1, args=(),name=Foo()).start()

    time.sleep(5)


if __name__ == "__main__":
    main()
