#!/usr/bin/env python3

import itertools
from typing import Set, List, Tuple

class AuctionProtocol(object):
    def __init__(self, item_ids: Set[int]):
        self.item_ids = item_ids
        self.bids = []

    def add_bid(self, items_to_bid: List[Tuple[Set[int], float]]):
        """
        bids: list of acceptable (won items, bid) tuples

        Examples:
        Single-minded bidder: {{1, 3, 4}: 5}
        Single-demand bidder: {{1}: 2, {3}: 2, {4}: 2}
        """
        self.bids.append(items_to_bid + [(set(), 0)])

    def _maximize_welfare(self, bids: List[List[Tuple[Set[int], float]]]):
        """
        Returns outcome (list of (items won, bid) per bidder)
        which maximizes total welfare
        """
        def is_valid_outcome(outcome) -> bool:
            """
            Returns true if all items won sets are disjoint
            """
            allocated_items = set()
            for items_won, bid in outcome:
                if not allocated_items.isdisjoint(items_won):
                    return False
                allocated_items |= items_won
            return True

        max_social_welfare = float('-Inf')
        argmax_social_welfare = None
        for outcome in itertools.product(*bids):
            if is_valid_outcome(outcome):
                social_welfare = sum(bid for items, bid in outcome)
                if social_welfare > max_social_welfare:
                    max_social_welfare = social_welfare
                    argmax_social_welfare = outcome

        return (argmax_social_welfare, max_social_welfare)

class VCGAuction(AuctionProtocol):
    def finalize(self) -> List[Tuple[Set[int], float]]:
        """
        Returns list of won items and price by bidder
        """
        outcome, total_bids = self._maximize_welfare(self.bids)
        result = []
        for i, (items_won, b_i) in enumerate(outcome):
            p_i = self._maximize_welfare(self.bids[:i] + self.bids[i+1:])[1] \
                    - (total_bids - b_i)
            result.append((items_won, p_i))
        
        return result

class GMSMAAuction(AuctionProtocol):
    pass

