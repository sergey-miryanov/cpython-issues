import sys

class FakeIO:
    def __init__(self, what):
        self.what = what

    @property
    def encoding(self):
        return "utf-8"
    
    def write(self, str):
        raise UnicodeEncodeError('utf-8', 'x', 0, 0, 'xxx')
    def flush(self):
        # self.restore_std('stderr')
        # self.restore_std('stdout')
        pass
    # def fileno(self):
    #     return 0
    
    @staticmethod
    def restore_std(what):
        stdfile = getattr(sys, what)
        setattr(sys, what, getattr(sys, F"__{what}__"))
        del stdfile

    @staticmethod
    def set_std(what):
        setattr(sys, what, FakeIO(what))


class Foo:
    def __repr__(self):
        FakeIO.restore_std('stdout')
        return 'Foo'

def main():
    print('main')
    FakeIO.set_std('stdout')

if __name__ == "__main__":
    main()
