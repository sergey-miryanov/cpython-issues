import gc

async def demo():
    a = object()
    print(gc.get_referrers(a))


try:
    demo().send(None)
except StopIteration as e:
    print(f"{e.value=}")

# import threading
# import time
# import sys

# gen = None

# class PrintSoon:
#     def __init__(self):
#         self.me = self

#     def __del__(self):
#         print("PrintSoon.__del__ called")
#         print(gen.gi_frame.f_locals["localvar"])

# class TriggerOnDelete:
#     def __del__(self):
#         # create some cyclic trash to be deleted next GC
#         PrintSoon()

# class MySpecialClass:
#     pass

# MySpecialClass.arg = TriggerOnDelete()

# def gensleep():
#     global MySpecialClass
#     localvar = MySpecialClass
#     del MySpecialClass
#     time.sleep(10000)
#     yield 1


# def thread_run():
#     global gen
#     gen = gensleep()
#     for _ in gen:
#         pass

# def main():
#     t = threading.Thread(target=thread_run, daemon=True)
#     t.start()

# if __name__ == "__main__":
#     main()
