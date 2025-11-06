import gc
import sys

# sys.setrecursionlimit(5000)

# gc.collect(2)
# gc.callbacks.append(print)

# def rec(level):
#     a = [object(), (level,)]
#     if level <= 0:
#         return a

#     return rec(level-1)

# a = rec(1000)
# print(a)

class X:
    def __init__(self):
        gc.collect(2)

X()
a = X()
b = X()
c = X()

a.a = a
a.b = b

b.c = c
c.a = a

print(sys.getrefcount(a))
print(sys.getrefcount(b))
print(sys.getrefcount(c))
