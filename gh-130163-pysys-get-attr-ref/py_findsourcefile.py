import sys
import io

_io_open = io.open

def io_open(*args, **kwargs):
    print (args, kwargs)
    if 'ss' in args:
        pass

    return _io_open(*args, **kwargs)

setattr(io, 'open', io_open)

raise Exception('1')