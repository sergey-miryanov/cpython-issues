import sys
import _testcapi; 

class FakeIO:
    def __init__(self, what):
        self.what = what
    def write(self, str):
        return 1024
        pass
    def flush(self):
        self.restore_std('stderr')
        self.restore_std('stdout')
        pass
    def fileno(self):
        return 0
    
    @staticmethod
    def restore_std(what):
        stdfile = getattr(sys, what)
        setattr(sys, what, getattr(sys, F"__{what}__"))
        del stdfile

    
    # @property
    # def closed(self):
    #     for what in ['stderr', 'stdout']:
    #         stdfile = getattr(sys, what)
    #         setattr(sys, what, getattr(sys, F"__{what}__"))
    #         del stdfile
    #     return False

class X(SystemExit):
    def __init__(self, code):
        super().__init__()
        self.code = code

    def __repr__(self):
        return "X"
    
class Y:
    def __init__(self, code):
        self.code = code

    def __repr__(self):
        FakeIO.restore_std('stderr')
        FakeIO.restore_std('stdout')
        return "Y" + self.code

def main():
    setattr(sys, 'stdout', FakeIO('stdout'))
    setattr(sys, 'stderr', FakeIO('stderr'))
    raise X(Y('22'))

if __name__ == "__main__":
    main()
