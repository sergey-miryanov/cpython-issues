import sys
def simple_for():
    for x in (1, 2):
        x
def gen():
    try:
        yield
    except:
        simple_for()
sys.settrace(lambda *args: None)
simple_for()
g = gen()
next(g)
