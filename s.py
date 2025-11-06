from concurrent import interpreters
import _interpreters

def func(*args, **kwargs):
    # pass # ok
    assert False # crash

def clean_up_interpreters():
    for interp in interpreters.list_all():
        if interp.id == 0:  # main
            continue
        try:
            interp.close()
        except _interpreters.InterpreterError:
            pass  # already destroyed


def test():
    interp = interpreters.create()
    interp.call_in_thread(func)

try:
    for _ in range(100):
        test()
finally:
    clean_up_interpreters()

