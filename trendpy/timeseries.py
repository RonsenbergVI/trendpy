import matplotlib.pyplot as plt

from numpy import arange
from trendpy.mcmc import MCMC
from trendpy.strategies import L1Strategy
from pandas import DataFrame, read_csv

__all__ = ['TimeSeries']

class TimeSeries(object):
	def __init__(self):
		self.data=None
		self.is_log_price = False

	def __len__(self):
		return self.data.size

	def __str__(self):
		return self.data.__str__()

	@staticmethod
	def from_csv(filename, is_log_price=True):
		ts=TimeSeries()
		ts.is_log_price = is_log_price
		ts.data=read_csv(filename,index_col=0)
		return ts

	def plot(self):
		self.data.plot()
		plt.show()

	def filter(self, method="l1-filter", number_simulations=100, burns=50):
		mcmc = MCMC(self, L1Strategy(self.data.as_matrix()[:,0]))

		mcmc.run(number_simulations)

		trend = mcmc.output(burns,"trend")
		
		self.data = self.data.join(DataFrame(trend,index=self.data.index,columns=[method]))
		
	def export(self, filename, as_txt=False):
		pass
		
