d = {}

class X(object):
    def __hash__(self):
        return 1
    def __eq__(self, other):
        d.clear()

d[X()] = None
d[X()] = None
for _ in range(10):
    d.update({X():None})


