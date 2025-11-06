import pickle
import sys

nested_object = current = {}
for i in range(50000):
    current['nested'] = {}
    current = current['nested']

def rec(level=1499):
    if level> 0:
        rec(level-1)

sys.setrecursionlimit(3750000)



x = pickle.dumps(nested_object)

rec()

