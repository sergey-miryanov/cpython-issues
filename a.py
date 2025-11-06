from concurrent import interpreters
interp1 = interpreters.create()
interp1.close() # same output occurs without this
