import itertools
from typing import Set, List, Tuple

def unit_demand_approximation(all_bids: List[List[Tuple[Set[int], float]]]):
    """
    Assume that all bids are either unit-demand or single-minded. 
    """
    def is_single_minded(bids: List[Tuple[Set[int], float]]):
        """
        Given bids, returns true if bidder is single-minded (one bid for k items, k > 1)
        bids: list of (items, bid) tuples from single bidder
        """
        return len(bids) == 1 and len(bids[0]) > 1

    def gen_approximate_bids(bids):
        def powerset(iterable):
            """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
            s = list(iterable)
            return itertools.chain.from_iterable(
                itertools.combinations(s, r)
                for r in range(1, len(s))
            )

        bundle, bid = bids[0]
        return [(set(subset), len(subset) / len(bundle) * bid) for subset in powerset(bundle)]

    return [gen_approximate_bids(bids) if is_single_minded(bids) else bids
            for bids in all_bids]
