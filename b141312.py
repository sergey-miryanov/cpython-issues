import pickle

for proto in range(pickle.HIGHEST_PROTOCOL + 1):
    it = iter(range(0x80000000 ** 32 + -(2**15)))
    print(it, type(it), it.__setstate__)
    it.__setstate__(int(2 ** -(2**15)) + 1)
    it.__setstate__(2 ** -(2**15) + 1)
    d = pickle.dumps(it, proto)
