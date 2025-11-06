import functools

def capture(*args, **kw):
    return (args, kw)
def extract_sig(part):
    return (part.func, part.args, part.keywords, part.__dict__)

def Z():
    pass

f = functools.partial(extract_sig)
f.__setstate__((capture, (1,), {}, ()))
f.__setstate__((capture, (1,), {}, {}))
