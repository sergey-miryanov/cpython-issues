import faulthandler
import sys
import time



faulthandler.dump_traceback_later(10 * 1e-308, exit=True, file=sys.__stderr__)
assert False
