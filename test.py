def test(n=2000):
    d = {}
    for i in range(n):
        for j in range(n):
            d[(i,j)] = i


test()
