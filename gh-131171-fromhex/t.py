import binascii
import random
import string
import time
from itertools import product

import pyperf

def bench_ref_fromhex(loops, value):
    range_it = range(loops)
    t0 = time.perf_counter()
    for _ in range_it:
        bytes.fromhex_ref(value)
    return time.perf_counter() - t0

def bench_new_fromhex(loops, value):
    range_it = range(loops)
    t0 = time.perf_counter()
    for _ in range_it:
        bytes.fromhex(value)
    return time.perf_counter() - t0

def bench_ref_a2b_hex(loops, value):
    range_it = range(loops)
    t0 = time.perf_counter()
    for _ in range_it:
        binascii.unhexlify(value)
    return time.perf_counter() - t0

def make_value(n, p=0):
    # n = q + s with even q and s; p = fraction of whitespaces
    # q = 2 * k = n * (1 - p)
    # s = n * p
    assert n % 2 == 0
    assert 0 <= p <= 1
    s = int(n * p)
    if s % 2 == 1:
        s = min(n, s + 1)
    q = max(0, n - s)
    assert s % 2 == 0
    assert q % 2 == 0
    # choose the random characters that will form the pairs
    chars = random.choices(string.hexdigits.lower(), k=q)
    terms = [''.join(chars[i:i + 2]) for i in range(0, q, 2)]
    terms.extend(random.choices(string.whitespace, k=s))
    random.shuffle(terms)
    return ''.join(terms), s

def bench(runner, name, func, ns=(16, 128, 1024), ps=(0,)):
    for n, p in product(ns, ps):
        value, n_ws = make_value(n, p)
        runner.bench_time_func(f'[{n}]+space[{n_ws}]', func, value)

def add_cmdline_args(cmd, args):
    cmd.append(args.implementation)

if __name__ == '__main__':
    runner = pyperf.Runner(add_cmdline_args=add_cmdline_args)
    runner.argparser.add_argument('implementation', choices=['ref', 'new', 'a2b'])
    args = runner.parse_args()

    ns = (16, 128, 1024)
    ps = (0, 0.1, 0.5, 0.9)

    # ns = (16,)
    # ps = (0,)
    if args.implementation in ('ref', 'new'):
        if args.implementation == 'ref':
            fromhex = bench_ref_fromhex
        elif args.implementation == 'new':
            fromhex = bench_new_fromhex
        bench(runner, args.implementation, fromhex, ns=ns, ps=ps)
    elif args.implementation == 'a2b':
        bench(runner, 'a2b_hex', bench_ref_a2b_hex, ns=ns)
