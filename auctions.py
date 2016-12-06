#!/usr/bin/env python3

import itertools
from typing import Set, List, Tuple

class AuctionProtocol(object):
    def __init__(self):
        self.all_bids = []
        self.all_bid_dicts = []

    def add_bidder(self, bids: List[Tuple[Set[int], float]]):
        """
        bids: list of acceptable (won items, bid) tuples
        """
        self.all_bids.append(bids + [(set(), 0)])
        self.all_bid_dicts.append({frozenset(items): bid for items, bid in bids})

    def _maximize_welfare(self, all_bids: List[List[Tuple[Set[int], float]]]):
        """
        Returns outcome (list of (items won, bid) per bidder)
        which maximizes total welfare

        v: Function v' used for maximizing welfare
        """
        def is_valid_outcome(outcome) -> bool:
            """
            Returns true if all items won sets are disjoint
            """
            allocated_items = set()
            for items, bid in outcome:
                if not allocated_items.isdisjoint(items):
                    return False
                allocated_items |= items
            return True

        max_social_welfare = float('-Inf')
        argmax_social_welfare = None
        for outcome in itertools.product(*all_bids):
            if is_valid_outcome(outcome):
                social_welfare = sum(bid for items, bid in outcome)
                if social_welfare > max_social_welfare:
                    max_social_welfare = social_welfare
                    argmax_social_welfare = outcome

        return (argmax_social_welfare, max_social_welfare)

class VCGAuction(AuctionProtocol):
    """
    Generalized VCG mechanism
    https://en.wikipedia.org/wiki/Vickrey–Clarke–Groves_auction
    """
    def finalize(self) -> List[Tuple[Set[int], float]]:
        """
        Returns list of won items and price by bidder
        """
        allocation, total_bids = self._maximize_welfare(self.all_bids)
        return [
            (
                items,
                # p_i; if/else not necessary but improves performance
                self._maximize_welfare(self.all_bids[:i] + self.all_bids[i+1:])[1] \
                    - (total_bids - b_i) if items else 0
            ) for i, (items, b_i) in enumerate(allocation)
        ]

class GMSMAAuction(AuctionProtocol):
    # def finalize(self, v_prime) -> List[Tuple[Set[int], float]]:
    #     """
    #     v: Function v' which is the submodular version of v, which takes all bids
    #     """
    #     allocation = self._maximize_welfare(v_prime(self.all_bids, -1))[0]
    #     argmax_social_welfare, total_bids = self._maximize_welfare(self.all_bids)
    #     print(allocation)
    #     result = []
    #     for i, (items, v_prime_i) in enumerate(allocation):
    #         u_star = self._maximize_welfare(v_prime(self.all_bids, i))[1]
    #         p_i =  u_star - (total_bids - argmax_social_welfare[i][1])
    #         print('Bidder {}: u* = {}, p_i = {}, b_i = {}'.format(i, u_star, p_i, self.all_bid_dicts[i].get(frozenset(items), 0)))
    #         if p_i < self.all_bid_dicts[i].get(frozenset(items), 0):
    #             result.append((items, p_i))
    #         else:
    #             result.append((set(), 0))
    #     return result

    def finalize(self, v_prime) -> List[Tuple[Set[int], float]]:
        """
        v: Function v' which is the submodular version of v, which takes all bids
        """
        def remove_bids_with_items(all_bids, items):
            return [[bid for bid in bids if not bid[0] & items] for bids in all_bids]

        allocation = self._maximize_welfare(v_prime(self.all_bids, -1))[0]
        argmax_social_welfare, total_bids = self._maximize_welfare(self.all_bids)
        print(allocation)
        result = []
        for i, (items, v_prime_i) in enumerate(allocation):
            u_star = self._maximize_welfare(v_prime(self.all_bids, i))[1]
            p_i =  u_star - self._maximize_welfare(remove_bids_with_items(self.all_bids[:i] + self.all_bids[i+1:], items))[1]
            print('Bidder {}: u* = {}, p_i = {}, b_i = {}'.format(i, u_star, p_i, self.all_bid_dicts[i].get(frozenset(items), 0)))
            if p_i < self.all_bid_dicts[i].get(frozenset(items), 0):
                result.append((items, p_i))
            else:
                result.append((set(), 0))
        return result
