# run with pytest on command line

from auctions import *

def test_vcg():
    a = VCGAuction({1, 2, 3, 4})
    a.add_bid([({1}, 3), ({2}, 3)])
    a.add_bid([({1}, 4), ({2}, 4)])
    a.add_bid([({1, 2, 3, 4}, 100)])
    assert a.finalize() == [(set(), 0), (set(), 0), ({1, 2, 3, 4}, 100)]