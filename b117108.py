if 1:
    class Obj:
        def __init__(self, i):
            self.val = i

    import sys
    print(sys.version)
    from time import perf_counter as now

    start = now()
    xs = [Obj(i) for i in range(2**22)]
    finish = now()
    print(finish - start)
