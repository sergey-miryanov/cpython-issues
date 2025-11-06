

from contextlib import redirect_stdout
from io import StringIO
import sys
from threading import Thread
import time

class Foo:
    def __repr__(self):
        time.sleep(0.2)
        return "Foo"
    
class Bar:
    def __init__(self):
        self.x = sys.stdout
        setattr(sys, "stdout", StringIO())

    def __repr__(self):
        x = sys.stdout
        setattr(sys, "stdout", self.x)
        del x
        return "Bar"


def thread1():
    text = StringIO()
    with redirect_stdout(text):
        time.sleep(0.2)

def main():
    # t1 = Thread(target=thread1, args=())
    # t1.start()
    # time.sleep(0.1)
    # print(Foo())
    print(Bar())


if __name__ == "__main__":
    main()
