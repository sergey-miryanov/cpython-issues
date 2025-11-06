import sys

class Hook:
    def __call__(self, *args, **kwds):
        pass

    def __repr__(self):
        h = sys.excepthook
        setattr(sys, 'excepthook', sys.__excepthook__)
        del h
        return 'Hook'

def audit(event, args):
    repr(args)

def main():
    sys.addaudithook(audit)
    setattr(sys, 'excepthook', Hook())
    raise

if __name__ == "__main__":
    main()
