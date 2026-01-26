# import sys
# sys.setrecursionlimit(30)

# str_v1 = ''
# tuple_v2 = (None, None, None, None, None)
# small_int_v3 = 4


# def f1():

#     for _ in range(10):
#         abs(0)

#     tuple_v2[small_int_v3]
#     tuple_v2[small_int_v3]
#     tuple_v2[small_int_v3]

#     def recursive_wrapper_4569():
#         str_v1 > str_v1
#         str_v1 > str_v1
#         str_v1 > str_v1
#         recursive_wrapper_4569()

#     recursive_wrapper_4569()


# for i_f1 in range(19000):
#     print(i_f1)
#     try:
#         f1()
#     except RecursionError:
#         pass

import _testcapi
import _testinternalcapi
import sys

def frame_0_interpreter() -> None:
    assert sys._jit.is_active() is False

def frame_1_interpreter() -> None:
    assert sys._jit.is_active() is False
    frame_0_interpreter()
    assert sys._jit.is_active() is False

def frame_2_jit(expected: bool) -> None:
    # Inlined into the last loop of frame_3_jit:
    assert sys._jit.is_active() is expected
    # Insert C frame:
    _testcapi.pyobject_vectorcall(frame_1_interpreter, None, None)
    assert sys._jit.is_active() is expected

def frame_3_jit() -> None:
    # JITs just before the last loop:
    # 1 extra iteration for tracing.
    for i in range(_testinternalcapi.TIER2_THRESHOLD + 2):
        # Careful, doing this in the reverse order breaks tracing:
        expected = True and i >= _testinternalcapi.TIER2_THRESHOLD
        print(i, sys._jit.is_active(), expected, _testinternalcapi.TIER2_THRESHOLD)
        assert sys._jit.is_active() is expected
        frame_2_jit(expected)
        assert sys._jit.is_active() is expected

def frame_4_interpreter() -> None:
    assert sys._jit.is_active() is False
    frame_3_jit()
    assert sys._jit.is_active() is False

assert sys._jit.is_active() is False
frame_4_interpreter()
assert sys._jit.is_active() is False
