# timeseries.py

# MIT License

# Copyright (c) 2017 Rene Jean Corneille

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
	def from_csv(filename, is_nomalized=True):
		ts=TimeSeries()
		ts.is_nomalized = is_nomalized
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

	def regression(self,method="lasso", number_simulations=100, burns=50):
		pass
		
	def fit(self,model="", number_simulations=100, burns=50):
		pass
		
	def export(self, filename, as_txt=False):
		pass
