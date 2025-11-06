
import sys

class UnraisableHookInitiator:
    def __del__(self):
        raise Exception('1')
    
class UnraisableHook:
    def __call__(self, *args, **kwds):
        print('X', *args)

    def __repr__(self):
        h = sys.unraisablehook
        setattr(sys, 'unraisablehook', sys.__unraisablehook__)
        del h
        return 'UnraisableHook'

def audit(event, args):
    repr(args)

def main():
    sys.addaudithook(audit)
    setattr(sys, 'unraisablehook', UnraisableHook())
    x = UnraisableHookInitiator()
    del x


if __name__ == "__main__":
    main()
