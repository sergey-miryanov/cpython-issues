import timeit
setup="from array import array; import ctypes; t = [i for i in range(1000000)];"
# standard way to build a C array, very slow
print(timeit.timeit(stmt='(ctypes.c_uint32 * len(t))(*t)',setup=setup,number=10))
# non standard way, by using an array, much faster
print(timeit.timeit(stmt="v = array('I',t);assert v.itemsize == 4; addr, count = v.buffer_info();p = ctypes.cast(addr,ctypes.POINTER(ctypes.c_uint32))",setup=setup,number=10))
# Results: 
# 1.7726366280003276
# 0.08820708599887439
