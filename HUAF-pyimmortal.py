import gc
import inspect
thingy = object()
class A(object):
    def f(self):
        return 1
    x = thingy
r = gc.get_referrers(thingy, A.x)
if "__module__" in r[0]:
    dct = r[0]
else:
    dct = r[1]
a = A()
for i in range(2):
    a.f()

print('-')
print(dct)
print('--')
print(A.__dict__)
print('---')

A.__dict__["f"] = lambda self: 2
print(a.f())
