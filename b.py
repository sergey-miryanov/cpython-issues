import weakref
from _testcapi import ManagedWeakrefNoGCType, ManagedDictNoGCType

# a = ManagedWeakrefNoGCType()
# print(a)
# print(a.test())

# # w = weakref.ref(a)
# # print(w)


# del a
# # del w

for _ in range(1_000_000):
    a = ManagedDictNoGCType()
    a.a = 1
    a.b = [1, 2]

    del a

print('finish')
