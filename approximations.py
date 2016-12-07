import itertools
from typing import Set, List, Tuple

import numpy as np
from scipy.optimize import linprog

def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r)
        for r in range(len(s))
    )

def is_unit_demand(bids: List[Tuple[Set[int], float]]):
    """
    Given bids, returns true if bidder is unit-demand (one item per bid). 
    """
    return all(len(items) <= 1 for items, bid in bids)

def single_minded_approximation(all_bids: List[List[Tuple[Set[int], float]]], i):
    """
    Assume that all bidders are either unit-demand or single-minded. 
    """
    def gen_approximate_bids(bids):
        bundle, bid = bids[0]
        return [(set(subset), len(subset) / len(bundle) * bid) for subset in powerset(bundle)]

    return [bids if is_unit_demand(bids) else gen_approximate_bids(bids) for bids in all_bids]

def additive_valuation_approximation(all_bids, i):
    """
    All bidders are either unit-demand or not. For non-unit-demand bidders,
    performs linear programming to minimize estimated v_ij for each item j
    given Av = b, where each A(r, :) indicates items in bundle and b(r)
    indicates corresponding bid. Then adds all estimated bids for all
    bundles in power set of union of bundles bidder i submitted a bid for. 
    """
    all_items = list(set.union(set.union(items for items, bid in bids) for bids in all_bids))
    item_to_idx = {item: i for i, item in enumerate(all_items)}

    def gen_approximate_bids(bids):
        v_bounds = (0, None)
        A = np.array([1 if item in items else 0 for item in all_items] for items, bid in bids)
        b = np.array(bid for bid in bids)
        v = linprog(np.ones(len(all_items)), A_ub=A, b_ub=b, bounds=v_bounds)

        def approximate_bid(items):
            return sum(v[item_to_idx[item]] for item in items)

        bidder_items = set.union(items for items, bid in bids)
        return [(set(subset), approximate_bid(subset)) for subset in powerset(bidder_items)]

    return [bids if is_unit_demand(bids) else gen_approximate_bids(bids) for bids in all_bids]
