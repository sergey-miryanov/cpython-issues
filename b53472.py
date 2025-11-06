x = 0
def f():
    x = 1
    class C:
        x = x
    assert C.x == 1, C.x
f()
