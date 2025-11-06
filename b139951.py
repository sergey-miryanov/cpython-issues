import gc
# gc.set_threshold(4000)
n = 2000
d = {}

for i in range(n):
    d[(i, i)] = d[(i, 0)] = d[(0, i)] = 0
gc.collect(0)
gc.disable()
for i in range(1, n):
    for j in range(1, n):
        d[(i, j)] = (
            i + j + d[(i - 1, j)] + d[(i, j - 1)] + d[(i - 1, j - 1)]
        ) % ((2**20) - 1)
gc.enable()
print((d[(n - 1, n - 1)] % 2) != 0)
