from auctions import *
from approximations import *
import random

class AuctionSimulator(object):
	def __init__(self, n_bidders, n_items, isVCG, approximation):
		self.n_bidders = n_bidders
		self.n_items = n_items
		self.isVCG = isVCG
		self.approximation = approximation

	def generate_bids(self):
		return []

	def simulate(self):
		bids = self.generate_bids()
		if self.isVCG:
			a = VCGAuction()
			for bid in bids:
				a.add_bidder(bid)
			return a.finalize()
		else:
			b = GMSMAAuction()
			for bid in bids:
				b.add_bidder(bid)
			return b.finalize(self.approximation)

class YokooSimulator(AuctionSimulator):
	def __init__(self, n_bidders, n_items, isVCG, approximation, k, r):
		super().__init__(n_bidders, n_items, isVCG, approximation)
		self.k = k
		self.r = r

	def generate_bids(self):
		bids = []
		for i in range(self.n_bidders):
			if random.random() < self.r:
				bids.append([({item for item in random.sample(range(self.n_items), self.k)}, random.randint(0, 1000*self.k))])
			else:
				bids.append([({item}, random.randint(0, 1000)) for item in random.sample(range(self.n_items), self.k)])

		return bids

class MultiMindedSimulator(AuctionSimulator):
	def __init__(self, n_bidders, n_items, isVCG, approximation, k, p, r):
		super().__init__(n_bidders, n_items, isVCG, approximation)
		self.k = k
		self.r = r
		self.p = p

	def generate_bids(self):
		bids = []
		for i in range(self.n_bidders):
			if random.random() < self.r:
				bids.append([({item for item in random.sample(range(self.n_items), self.k)}, random.randint(0, 1000*self.k))] for i in range(self.p))
			else:
				bids.append([({item}, random.randint(0, 1000)) for item in random.sample(range(self.n_items), self.k)])
		return bids








