import pyperf
import functools
runner = pyperf.Runner()

def bench(loops):
    i = filter(bool, range(10000))
    for _ in range(loops):
        i = filter(bool, i)
    return len(list(i))

for size in (1000, 2000, 4000, 8000, 16000):
    func = functools.partial(bench, size)
    runner.bench_func(f'filter-{size}', func)
