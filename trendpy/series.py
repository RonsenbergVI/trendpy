# -*- coding: utf-8 -*-

# series.py

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

from trendpy.mcmc import MCMC
from trendpy.factory import StrategyFactory

from pandas import DataFrame, read_csv

class Series(object):
	""" Implements univariate time series

	Examples
	--------

		Import the class

		>>> from trendpy.series import Series

		create from csv

		>>> data = Series.from_csv('data.csv')
	"""
	def __init__(self):
		self.data=None

	def __len__(self):
		return self.data.size

	def __str__(self):
		return self.data.__str__()

	@staticmethod
	def from_csv(filename):
		""" Instantiate new time series from a csv file

		:param filename: path of the file with extension (.csv or .txt)
		:type filename: str
		"""
		time_series=Series()
		time_series.data=read_csv(filename,index_col=0)
		return time_series

	def returns(self,period=1):
		""" Adds a new time series to the data with the returns of the original
			time series.

		:param period: number of days between two consecutive observations used to
				compute the returns.
		:type period: int
		"""
		pass

	def save(self,filename='export.csv',type='csv',separator=','):
		""" Saves the data contained in the object to a csv file

		:param filename: path and name of the file to export
		:type filename: str
		:param  type: by default csv, if no value is given then a csv file is saved.
				another possible format is json (other should be available in
				future releases).
		:type type: string, optional
		:param separator: separator between columns in file.
		:type separator: str
		"""
		if type=='csv':
			pass
		if type=='json':
			pass

	def plot(self):
		""" Plots the time series"""
		self.data.plot()
		plt.show()

	def filter(self, method="L1Filter",number_simulations=100, burns=50,total_variation=2):
		""" Filters the trend of the time series.

		:param method: path and name of the file to export
		:type method: str
		:param  type: by default csv, if no value is given then a csv file is saved.
				another possible format is json (other should be available in
				future releases).
		:type type: string, optional
		:param separator: separator between columns in file.
		:type separator: str
		"""
		mcmc = MCMC(self, StrategyFactory.create(method,self.data.as_matrix()[:,0],total_variation_order=total_variation))

		mcmc.run(number_simulations)

		trend = mcmc.output(burns,"trend")

		self.data = self.data.join(DataFrame(trend,index=self.data.index,columns=[method]))
