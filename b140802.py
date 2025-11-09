import sys

class JumpTracer:
    def __init__(self, func):
        self.code = func.__code__
        self.count = 0

    def trace(self, frame, event, arg):
        if event == 'line' and frame.f_code is self.code:
            if self.count == 1:
                frame.f_lineno = frame.f_lineno - 2
            self.count += 1
        return self.trace

def target():
    i = 90
    yield

tracer = JumpTracer(target)
sys.settrace(tracer.trace)
t = target()
next(t)

print(tracer.count)
