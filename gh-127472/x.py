import copy
import sys
import threading

SIZE = 1_000_000_000  # 1GB


print("Allocating initial arrays", flush=True)
_original = bytearray(42 for _ in range(SIZE))
_garbage = bytearray(13 for _ in range(SIZE // 4))


array = copy.copy(_original)


def new_array():
    return copy.copy(_original)


def worker1():
    global array
    while True:
        print("Extending array", flush=True)
        array.extend(array)
        print("Recreating array", flush=True)
        array = new_array()


def worker2():
    while True:
        expected = {0, 42}
        # Arguably, we shouldn't even see 0, but let's be lenient and assume
        # it might be zeroed memory not yet set to the actual value. In
        # reality, seeing 0 very likely indicates reading uninitialized memory.
        # When changing the program to also fail on 0, we can see a failure
        # much faster.
        for i in (0, SIZE - 1, -SIZE, -1):
            value = array[i]
            if value not in expected:
                print(
                    f"Array corrupted (observed array[{i}] = {value})",
                    file=sys.stderr,
                    flush=True,
                )
                return


def worker3():
    print("Putting other stuff into the memory", flush=True)
    while True:
        foo = [copy.copy(_garbage) for _ in range(5)]
        for f in foo:
            f.extend(f)
        del foo


t1 = threading.Thread(target=worker1, daemon=True)
t2 = threading.Thread(target=worker2, daemon=True)
t3 = threading.Thread(target=worker3, daemon=True)

t1.start()
t2.start()
t3.start()

t2.join()
