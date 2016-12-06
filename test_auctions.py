"""
run on command line
$ pytest
"""

from auctions import *

def test_vcg():
    a = VCGAuction()
    a.add_bidder([({1}, 3), ({2}, 3)])
    a.add_bidder([({1}, 4), ({2}, 4)])
    a.add_bidder([({1, 2, 3, 4}, 100)])
    assert a.all_bid_dicts[2] == {frozenset({1, 2, 3, 4}): 100}
    assert a.finalize() == [(set(), 0), (set(), 0), ({1, 2, 3, 4}, 7)]

def test_vcg2():
    a = VCGAuction()
    a.add_bidder([({1}, 6), ({1, 2}, 6)])
    a.add_bidder([({1, 2}, 8)]),
    a.add_bidder([({1, 2}, 5), ({2}, 5)])
    assert a.finalize() == [({1}, 3), (set(), 0), ({2}, 2)]

def test_vcg3():
    a = VCGAuction()
    a.add_bidder([({1}, 4), ({1, 2}, 7), ({2}, 3)])
    a.add_bidder([({1, 2}, 8)])
    assert a.finalize() == [(set(), 0), ({1, 2}, 7)]

def test_gmsma():
    def sanity_approximation(all_bids):
        return [[({1}, 4), ({2}, 9), ({1, 2}, 9)],
                [({1}, 4), ({2}, 4), ({1, 2}, 11)], 
                [({1}, 10), ({2}, 4), ({1, 2}, 10)]]
    a = GMSMAAuction()
    a.add_bidder([({1}, 4), ({2}, 9), ({1, 2}, 9)])
    a.add_bidder([({1}, 6), ({2}, 5), ({1, 2}, 11)])
    a.add_bidder([({1}, 10), ({2}, 4), ({1, 2}, 10)])
    assert a.finalize(sanity_approximation) == [({1}, 4), (set(), 0), ({2}, 4)]


