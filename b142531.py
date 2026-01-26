import time
import gc
import sys

def benchmark_step(disable_gc):
    if disable_gc:
        gc.disable()

    t0 = time.perf_counter()
    _ = [(0, 0, i) for i in range(15_000_000)]
    dt = time.perf_counter() - t0

    status = "GC DISABLED" if disable_gc else "GC ENABLED "
    print(f"{status}: {dt:.3f}s")

    if disable_gc:
        gc.enable()

if __name__ == "__main__":
    print(f"Python Version: {sys.version}")
    sample = (0, 0, 1)
    print(f"Is tuple(int, int, int) tracked? {gc.is_tracked(sample)}")

    print("--- Benchmark ---")
    benchmark_step(disable_gc=False)
    benchmark_step(disable_gc=True)
