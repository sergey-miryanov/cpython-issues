import threading
import _thread
import weakref
import sys
import gc

def test_settrace_leak_0():
    local = _thread._local()

    class ClassWithDel:
        def __del__(self):
            threading.settrace(tracer)

    def tracer(frame, event, arg):
        local.c = ClassWithDel()

    old_trace = threading.gettrace()
    try:
        threading.settrace(tracer)
        t = threading.Thread()
        t.start()
        t.join()
        del t
    finally:
        threading.settrace(old_trace)

def test_settrace_leak_1():
    local = _thread._local()

    class ClassWithDel:
        def __del__(self):
            local.x = ClassWithDel()

    local.c = ClassWithDel()


def test_settrace_leak():

    class ClassWithDel:
        def __del__(self):
            ClassWithDel()

    ClassWithDel()

def rec():
    rec()


rec()
