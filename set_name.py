import sys

class X:
    def __init__(self):
        pass


n = 'x'

def audit(event, args):
    if event == 'object.__setattr__':
        global n
        del n
        print(repr(args))

def main():
    sys.addaudithook(audit)

    X.__name__ = n
    print (X.__name__)
    print (X)

if __name__ == "__main__":
    main()
