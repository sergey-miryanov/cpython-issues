

from io import StringIO
import sys
import warnings

    
class Foo:
    def __init__(self):
        self.x = sys.stderr
        setattr(sys, "stderr", StringIO())

    def __repr__(self):
        x = sys.stderr
        setattr(sys, "stderr", self.x)
        del x
        return "XXX"

def main():
    del warnings._showwarnmsg
    warnings.warn_explicit(Foo(),UserWarning,'filename', 0)


if __name__ == "__main__":
    main()
