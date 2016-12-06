import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from auctions import *
from approximations import *
from simulations import *



def revenue_plot(n_bidders, n_items, k, n_trials):
	step_size = 0.01
	vcg_revenue = []
	gmsma_revenue = []
	x = []
	for r in np.arange(0, 1, step_size):
		print(r)
		average_vcg_revenue = 0
		average_gmsma_revenue = 0
		for i in range(n_trials):
			sim = YokooSimulator(n_bidders, n_items, True, None, k, r)
			sim2 = YokooSimulator(n_bidders, n_items, False, unit_demand_approximation, k, r)
			average_vcg_revenue += sim.simulate()
			average_gmsma_revenue += sim2.simulate()
		average_gmsma_revenue /= n_trials
		average_vcg_revenue /= n_trials
		vcg_revenue.append(average_vcg_revenue)
		gmsma_revenue.append(average_gmsma_revenue)
	plt.plot(np.arange(0, 1, step_size), gmsma_revenue)
	plt.show()

revenue_plot(6, 4, 2, 1000)


