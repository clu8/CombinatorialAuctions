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

class VCGAuction(AuctionProtocol):
    def finalize(self) -> List[Tuple[Set[int], float]]:
        """
        Returns list of won items and price by bidder
        """
        def maximize_welfare(bids: List[List[Tuple[Set[int], float]]]):
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
            for outcome in itertools.product(*self.bids):
                if is_valid_outcome(outcome):
                    social_welfare = sum(bid for items, bid in outcome)
                    if social_welfare > max_social_welfare:
                        max_social_welfare = social_welfare
                        argmax_social_welfare = outcome

            return (argmax_social_welfare, max_social_welfare)
    
        def calculate_prices(outcome: List[Tuple[Set[int], float]],
                             total_bids: float) \
                             -> List[Tuple[Set[int], float]]:
            """
            outcome: list of (items_won, bid) per bidder
            total_bids: sum of all bids
            returns: list of (items_won, price) per bidder
            """
            result = []
            for i, (items_won, bid) in enumerate(outcome):
                p_i = maximize_welfare(outcome[:i] + outcome[i+1:])[1] \
                      - (total_bids - bid)
                result.append((items_won, p_i))
            
            return result

        return calculate_prices(*maximize_welfare(self.bids))

class GMSMAAuction(AuctionProtocol):
    pass

