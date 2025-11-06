import weakref
import _testcapi as t

a = t.WeakrefNoGC()
r = weakref.ref(a)
print(a)
print(r)
