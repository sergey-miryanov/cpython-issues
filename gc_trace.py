import gc
import weakref

class C1055820(object):
    def __init__(self, i):
        self.i = i
        self.loop = self

class GC_Detector(object):
    # Create an instance I.  Then gc hasn't happened again so long as
    # I.gc_happened is false.

    def __init__(self):
        self.gc_happened = False

        def it_happened(ignored):
            self.gc_happened = True

        # Create a piece of cyclic trash that triggers it_happened when
        # gc collects it.
        self.wr = weakref.ref(C1055820(666), it_happened)

def test_bug1055820d():
    # Corresponds to temp2d.py in the bug report.  This is very much like
    # test_bug1055820c, but uses a __del__ method instead of a weakref
    # callback to sneak in a resurrection of cyclic trash.

    ouch = []
    class D(C1055820):
        def __del__(self):
            ouch[:] = [c2wr()]

    d0 = D(0)
    # Move all the above into generation 2.
    gc.collect()

    c1 = C1055820(1)
    c1.keep_d0_alive = d0
    del d0.loop # now only c1 keeps d0 alive

    c2 = C1055820(2)
    c2wr = weakref.ref(c2) # no callback!

    d0 = c1 = c2 = None

    # What we've set up:  d0, c1, and c2 are all trash now.  d0 is in
    # generation 2.  The only thing keeping it alive is that c1 points to
    # it.  c1 and c2 are in generation 0, and are in self-loops.  There's
    # a global weakref to c2 (c2wr), but that weakref has no callback.
    # There are no other weakrefs.
    #
    #               d0 has a __del__ method that references c2wr
    #               ^
    #               |
    #               |     Generation 2 above dots
    #. . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . .
    #               |     Generation 0 below dots
    #               |
    #               |
    #            ^->c1   ^->c2 has a wr but no callback
    #            |  |    |  |
    #            <--v    <--v
    #
    # So this is the nightmare:  when generation 0 gets collected, we see
    # that c2 has a callback-free weakref, and c1 doesn't even have a
    # weakref.  Collecting generation 0 doesn't see d0 at all.  gc clears
    # c1 and c2.  Clearing c1 has the side effect of dropping the refcount
    # on d0 to 0, so d0 goes away (despite that it's in an older
    # generation) and d0's __del__ triggers.  That in turn materializes
    # a reference to c2 via c2wr(), but c2 gets cleared anyway by gc.

    # We want to let gc happen "naturally", to preserve the distinction
    # between generations.
    detector = GC_Detector()
    junk = []
    i = 0
    while not detector.gc_happened:
        i += 1
        junk.append([])  # this will eventually trigger gc

    print('Iterations before gc', i)
    assert len(ouch) == 1, len(ouch)  # else __del__ wasn't invoked
    for x in ouch:
        # If __del__ resurrected c2, the instance would be damaged, with an
        # empty __dict__.
        assert x is None, x


if __name__ == '__main__':
    test_bug1055820d()


# nascheme - 3998
# main - 14003
