from _testcapi import test_tuple_pack

import time
from logging import Logger
from logging.handlers import DatagramHandler
from unittest.mock import MagicMock
from shelve import Shelf

import pyperf


def bench_test_tuple_pack(value):
    for cnt in range(value):
        for _ in range(1000):
            test_tuple_pack(cnt)

def bench_test_tuple_concat(value):
    a = (True, False) * 10
    b = (False, True) * 10

    for cnt in range(value):
        for _ in range(1000):
            c = a[:cnt] + b[:cnt]

# def bench_cls_with_dunders(value):
#     for _ in range(value):
#         class C:
#             def __init__(self):
#                 pass
#             def __repr__(self):
#                 return ""
#             def __str__(self):
#                 return ""

# def bench_empty_cls_with_base(value):
#     count, bases = value
#     for _ in range(count):
#         class C(*bases):
#             pass

# def bench_cls_with_dunders_with_base(value):
#     count, bases = value
#     for _ in range(count):
#         class C(*bases):
#             def __init__(self):
#                 pass
#             def __repr__(self):
#                 return ""
#             def __str__(self):
#                 return ""


# def bench_import(value):
#     for _ in range(value):
#         import ast
#         import dis
#         import symtable
#         import sys
#         import _asyncio
#         import typing
#         import logging
#         import logging.handlers
#         import unittest
#         import unittest.mock
#         import shelve
#         import pathlib


def bench(runner: pyperf.Runner, name, func, args):
    def wfunc(loops, value):
        ts = time.perf_counter()
        for _ in range(loops):
            func(value)
        return time.perf_counter() - ts

    runner.bench_time_func(name, wfunc, args)

def add_cmdline_args(cmd, args):
    cmd.append(args.xxx)

if __name__ == '__main__':

    runner = pyperf.Runner(add_cmdline_args=add_cmdline_args)
    runner.argparser.add_argument('xxx', choices=['all', 'empty', 'cls', 'imported', 'builtin', 'import'])
    args = runner.parse_args()

    runs = (2, 5, 10)
    benches = (bench_test_tuple_pack, bench_test_tuple_concat)

    for b in benches:
        for run in runs:
            bench(runner, F'{b.__name__}-{run}', b, run)

    # runs = (1_000, 100_000)
    # runs=(1_000,)
    # bases = ((A, B), (A, B, D))
    # dunders = ((A_dun, B_dun), (A_dun, B_dun, D_dun))
    # bases2 = ((Logger,), (DatagramHandler, ), (MagicMock, ), (Shelf, ))
    # bases3 = ((tuple,), (dict, ), (list, ))

    # for run in runs:
    #     if args.xxx in ('all', 'empty'):
    #         bench(runner, f'{run}-empty_cls', bench_empty_cls, run)

    #     if args.xxx in ('all', 'cls'):
    #         bench(runner, f'{run}-cls_with_dunders', bench_cls_with_dunders, run)

    #     for b in bases + dunders:
    #         bname = F"bases={[c.__name__ for c in b]}"
    #         if args.xxx in ('all', 'empty'):
    #             bench(runner, f'{run}-empty_cls_with_bases-{bname}', bench_empty_cls_with_base, (run, b))

    #         if args.xxx in ('all', 'cls'):
    #             bench(runner, f'{run}-cls_with_bases-{bname}', bench_cls_with_dunders_with_base, (run, b))

    #     bs = []
    #     if args.xxx in ('all', 'imported'):
    #         bs.extend(bases2)
    #     if args.xxx in ('all', 'builtin'):
    #         bs.extend(bases3)

    #     for b in bs:
    #         bname = F"bases={[c.__name__ for c in b]}"
    #         bench(runner, f'{run}-empty_cls_with_bases-{bname}', bench_empty_cls_with_base, (run, b))
    #         bench(runner, f'{run}-cls_with_bases-{bname}', bench_cls_with_dunders_with_base, (run, b))

    #     if args.xxx in ('import',):
    #         bench(runner, f'{run}-import', bench_import, run)
