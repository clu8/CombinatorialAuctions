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
    approximated_bids = [[({1}, 6), ({2}, 0), ({1, 2}, 6), (set(), 0)],
                         [({1}, 4), ({2}, 4), ({1, 2}, 8), (set(), 0)], 
                         [({1}, 0), ({2}, 5), ({1, 2}, 5), (set(), 0)]]
    def sanity_approximation(all_bids, i):
        if i == -1:
            return approximated_bids
        else:
            return approximated_bids[:i] + approximated_bids[i+1:] 
    a = GMSMAAuction()
    a.add_bidder([({1}, 6), ({2}, 0), ({1, 2}, 6)])
    a.add_bidder([({1}, 0), ({2}, 0), ({1, 2}, 8)])
    a.add_bidder([({1}, 0), ({2}, 5), ({1, 2}, 5)])
    assert a.finalize(sanity_approximation) == [({1}, 4), (set(), 0), ({2}, 4)]


