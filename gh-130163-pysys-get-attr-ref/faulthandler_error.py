
# from contextlib import redirect_stderr
# from threading import Thread
# import time
# from faulthandler import dump_traceback, enable, dump_traceback_later


# class FakeFile:
#     def __init__(self):
#         self.f = open('x', 'w')
#     def write(self, s):
#         self.f.write(s)
#     def flush(self):
#         time.sleep(0.2)
#     def fileno(self):
#         time.sleep(0.2)
#         return self.f.fileno()

# def thread1():
#     text = FakeFile()
#     with redirect_stderr(text):
#         time.sleep(0.2)

# def main():
#     enable(None, True)
#     t1 = Thread(target=thread1, args=())
#     t1.start()
#     time.sleep(0.1)
#     # time.sleep(0.1)
#     # dump_traceback_later(0.1, True, None, False)
#     # print(Foo())
#     # enable(None, True)
#     # ctypes.string_at(0)
#     # dump_traceback(None, False)
#     dump_traceback_later(0.1, False, None, False)


# if __name__ == "__main__":
#     main()


import sys
from faulthandler import dump_traceback, enable, dump_traceback_later

class FakeIO:
    def __init__(self, what):
        self.what = what
    def write(self, str):
        pass
    def flush(self):
        pass
    def fileno(self):
        self.restore_std('stderr')
        return 0
    
    @staticmethod
    def restore_std(what):
        stdfile = getattr(sys, what)
        setattr(sys, what, getattr(sys, F"__{what}__"))
        del stdfile

    @staticmethod
    def set_std(what):
        setattr(sys, what, FakeIO(what))
    
def main():
    enable(None, True)
    FakeIO.set_std('stderr')
    # enable(None, True)
    # dump_traceback(None, False)
    # dump_traceback_later(0.1, False, None, False)

if __name__ == "__main__":
    main()
