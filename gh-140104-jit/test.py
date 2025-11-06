# def f():

#     if 0:
#         class Class:
#             pass

#     if 0:
#         instance = Class()

#     for _ in range(5000):
#         try:
#             _ = instance.f()
#         except Exception:
#             pass
#     Class.__bases__ = (object,)

# f()

def f():
    for i in range(500):
        try:
            g(i)
        except Exception:
            pass

for _ in range(5000):
    f()
