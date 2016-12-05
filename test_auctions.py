"""
run on command line
$ pytest
"""

from auctions import *

def test_vcg():
    a = VCGAuction({1, 2, 3, 4})
    a.add_bid([({1}, 3), ({2}, 3)])
    a.add_bid([({1}, 4), ({2}, 4)])
    a.add_bid([({1, 2, 3, 4}, 100)])
    assert a.finalize() == [(set(), 0), (set(), 0), ({1, 2, 3, 4}, 7)]

def test_vcg2():
    a = VCGAuction({1, 2})
    a.add_bid([({1}, 6), ({1, 2}, 6)])
    a.add_bid([({1, 2}, 8)]),
    a.add_bid([({1, 2}, 5), ({2}, 5)])
    assert a.finalize() == [({1}, 3), (set(), 0), ({2}, 2)]

def test_vcg3():
    a = VCGAuction({1, 2})
    a.add_bid([({1}, 4), ({1, 2}, 7), ({2}, 3)])
    a.add_bid([({1, 2}, 8)])
    assert a.finalize() == [(set(), 0), ({1, 2}, 7)]
