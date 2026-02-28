import _testinternalcapi
import pyperf


def add_cmdline_args(cmd, args):
    cmd.append(args.what)


def main():

    runner = pyperf.Runner(add_cmdline_args=add_cmdline_args)
    runner.argparser.add_argument('what', choices=['all', ])
    args = runner.parse_args()

    if args.what.lower() in ('all', ):
        runner.bench_time_func('bench_tuple_new_pair', _testinternalcapi.bench_tuple_new_pair)
        runner.bench_time_func('bench_tuple_pack_pair', _testinternalcapi.bench_tuple_pack_pair)
        runner.bench_time_func('bench_tuple_from_array_pair', _testinternalcapi.bench_tuple_from_array_pair)
        runner.bench_time_func('bench_tuple_from_array_pair_steal', _testinternalcapi.bench_tuple_from_array_pair_steal)
        runner.bench_time_func('bench_tuple_from_pair', _testinternalcapi.bench_tuple_from_pair)
        runner.bench_time_func('bench_tuple_from_pair_steal', _testinternalcapi.bench_tuple_from_pair_steal)



if __name__ == '__main__':
    main()

