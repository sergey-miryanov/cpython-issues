import sys
import _testcapi; 

class FakeIO:
    def __init__(self, what):
        self.what = what
    def write(self, str):
        pass
    def flush(self):
        pass
    def fileno(self):
        return 0
    
    @property
    def closed(self):
        for what in ['stderr', 'stdout']:
            stdfile = getattr(sys, what)
            setattr(sys, what, getattr(sys, F"__{what}__"))
            del stdfile
        return False
    
def main():
    # setattr(sys, 'stdout', FakeIO('stdout'))
    setattr(sys, 'stderr', FakeIO('stderr'))
    _testcapi.fatal_error(b"MESSAGE")

if __name__ == "__main__":
    main()
