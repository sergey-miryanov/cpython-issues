import gc
import weakref
import types
import collections



class LateFin:
    __slots__ = ('ref',)

    def __del__(self):
        print('8')

        # 8. Now `latefin`'s finalizer is called. Here we
        #    obtain a reference to `func`, which is currently
        #    undergoing `tp_clear`.
        global func
        func = self.ref()

class Cyclic(tuple):
    __slots__ = ()

    # 4. The finalizers of all garbage objects are called. In
    #    this case this is only us as `func` doesn't have a
    #    finalizer.
    def __del__(self):
        print('5')

        # 5. Create a weakref to `func` now. If we had created
        #    it earlier, it would have been cleared by the
        #    garbage collector before calling the finalizers.
        self[1].ref = weakref.ref(self[0])

        # 6. Drop the global reference to `latefin`. The only
        #    remaining reference is the one we have.
        global latefin
        del latefin

    # 7. Now `func` is `tp_clear`-ed. This drops the last
    #    reference to `Cyclic`, which gets `tp_dealloc`-ed.
    #    This drops the last reference to `latefin`.

latefin = LateFin()
class X:
    pass
def func():
    print('x')
cyc = tuple.__new__(Cyclic, (func, latefin))

# 1. Create a reference cycle of `cyc` and `func`.
func.__module__ = cyc

# 2. Make the cycle unreachable, but keep the global reference
#    to `latefin` so that it isn't detected as garbage. This
#    way its finalizer will not be called immediately.
del func, cyc

# 3. Invoke garbage collection,
#    which will find `cyc` and `func` as garbage.
gc.collect()

# 9. Previously, this would crash because `func_qualname`
#    had been NULL-ed out by func_clear().
print(f"{func=}")
func()
