
import sys


class FakeIO:
    def write(self, str):
        pass
    def flush(self):
        pass
    def fileno(self):
        return 0

class CrashStdin:
    def __init__(self):
        self.stdin = sys.stdin
        setattr(sys, "stdin", FakeIO())

    def __repr__(self):
        stdin = sys.stdin
        setattr(sys, "stdin", self.stdin)
        del stdin
        return "CrashStdin"
    
class CrashStdout:
    def __init__(self):
        self.stdout = sys.stdout
        setattr(sys, "stdout", FakeIO())

    def __repr__(self):
        stdout = sys.stdout
        setattr(sys, "stdout", self.stdout)
        del stdout
        return "CrashStdout"
    
class CrashStderr:
    def __init__(self):
        self.stderr = sys.stderr
        setattr(sys, "stderr", FakeIO())

    def __repr__(self):
        stderr = sys.stderr
        setattr(sys, "stderr", self.stderr)
        del stderr
        return "CrashStderr"
    

def audit(event, args):
    if event == 'builtins.input':
        repr(args)

def main():
    sys.addaudithook(audit)
    input(CrashStderr())


if __name__ == "__main__":
    main()
