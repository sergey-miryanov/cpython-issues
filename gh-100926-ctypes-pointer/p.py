import ctypes 
from ctypes.wintypes import USHORT, BYTE
from typing import Type

def shitemid_factory(size: int) -> Type[ctypes.Structure]:
    class SHITEMID_Var(ctypes.Structure):
        _fields_ = (
            ("cb", USHORT),
            ("abID", BYTE * size),
        )

    return SHITEMID_Var

def bad_func(sz):
    SHITEMID_Var = shitemid_factory(sz - ctypes.sizeof(USHORT))
    print('-'*80)
    print(SHITEMID_Var.__pointer_type__)
    item_var = ctypes.POINTER(SHITEMID_Var)
    print(SHITEMID_Var.__pointer_type__)
    print (item_var._type_, item_var.__base__.__base__)

for i in range(1):
    bad_func(64)
