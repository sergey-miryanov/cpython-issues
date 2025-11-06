import pyperf
import _testcapi
import functools
runner = pyperf.Runner()
for size in (1, 2):
    func = functools.partial(_testcapi.bench_tuple_set_item, size)
    runner.bench_time_func(f'tuple-{size}', func)
