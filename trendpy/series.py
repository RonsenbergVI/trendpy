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

from statsmodels.iolib.table import SimpleTable
from statsmodels.iolib.summary import Summary, fmt_2cols, fmt_params

from datetime import datetime

from pandas import DataFrame, read_csv

from numpy import array, sqrt

class Series(object):
	""" Implements univariate time series.

	Examples
	--------

		Import the class

		>>> from trendpy.series import Series

		create from csv

		>>> data = Series.from_csv('data.csv')
	"""
	def __init__(self):
		self.data=None
		self.begin_index=None
		self.ed_index=None

	def __len__(self):
		return self.data.size

	def __str__(self):
		return self.data.__str__()

	@staticmethod
	def from_csv(filename,index='date'):
		""" Instantiate new time series from a csv file where the first
			column is a timestamp or a date or a datetime.

		:param filename: path of the file with extension (.csv or .txt)
		:type filename: str
		:return: the price time series
		:rtype: `trendpy.series.Series`
		"""
		time_series=Series()
		time_series.data=read_csv(filename,index_col=0)
		return time_series
		
	def summary(self):
		""" Returns an ASCII table with basic statistics of the time series loaded.
		
		:return: ASCII table with main description of the data set
		:rtype: str
		"""
		smry = Summary()
		summary_title = 'Summary - %s ' % self.data.columns[0]
		left = [('Begin: ', self.data.index[0]),
					('End: ',self.data.index[len(self.data.index)-1]),
					('Number of observations: ', len(self.data.index)),
					('Number of time series: ', len(self.data.columns)),
					('', ''),
					('Date: ', datetime.now().strftime('%a, %b %d %Y %H:%M:%S'))]

		right = [('Ann. return:','%.2f%%' % float(100*self.annualized_return())),
					 ('Ann. volatility:','%.2f%%' % float(100*self.annualized_volatility())),
					 ('Max drawdown:', 0),
					 ('Drawdown Duration: ', 0),
					 ('Skewness:', 0),
					 ('Kurtosis:', 0)]
		keys = []
		values = []
		for key, value in left:
			keys.append(key)
			values.append([value])
		table = SimpleTable(values, txt_fmt=fmt_2cols, title=summary_title, stubs=keys)
		smry.tables.append(table)
		keys = []
		values = []
		for key, value in right:
			keys.append(key)
			values.append([value])
		table.extend_right(SimpleTable(values, stubs=keys))
		return smry

	def returns(self,period=1,annualize='Y'):
		""" Adds a new time series to the data with the returns of the original
			time series.

		:param period: number of days between two consecutive observations used to
				compute the returns.
		:type period: int, optional
		:return: output of the MCMC algorithm
		:rtype: `Numpy.dnarray`
		"""
		return_series = Series()
		return_series.data = self.data.pct_change(periods=period)
		return_series.data = return_series.data.fillna(0)
		return return_series
		
	def annualized_return(self):
		""" Computes the annualized return.
	
		:return: annualized return on the whole time series.
		:rtype: float
		"""
		returns = self.returns().data.as_matrix()
		return (252/len(returns))*sum(returns)
		
	def annualized_volatility(self):
		""" Computes the annualized volatility.
	
		:return: annualized volatility on the whole time series.
		:rtype: float
		"""
		r = self.annualized_return()
		returns = self.returns().data.as_matrix()
		return sqrt((252/(len(returns)-1))*sum(array([(ret-r)**2 for ret in returns])))
	
	def skewness(self):
		""" Computes the skewness of the returns empirical distribution.
	
		:return: skewness on the whole time series returns.
		:rtype: float
		"""
		pass
		#returns = self.returns().as_matrix()
		#return sum(array([s]))
	
	def kurtosis(self):
		""" Computes the kurtosis of the returns empirical distribution.
	
		:return: kurtosis on the whole time series returns.
		:rtype: float
		"""
		pass
	
	def drawdown_duration(self):
		""" Computes the drawdown duration of the price time series.
	
		:return: drawdown duration of th time series.
		:rtype: float
		"""
		pass

	def max_drawdown(self):
		""" Computes the maximum drawdown of the price time series.
	
		:return: drawdown duration of th time series.
		:rtype: float
		"""
		pass

	def periodic_returns(self,period=30):
		""" Computes the maximum drawdown of the price time series.
	
		:return: periodic return plot of the time series.
		:rtype: float
		"""
		pass

	def rolling_max_drawdown(self,lag=1):
		""" Computes the rolling maximum drawdown of the time series.

		:param lag: number of observations used.
		:type lag: int, optional
		"""
		pass

	def rolling_volatility(self,lag=360):
		""" Computes the rolling volatility of the time series
		    with annualization possible. The formula used is the following:

		:param lag: number of observations used.
		:type lag: int, optional
		:param annualize: 
		:type annualize: str, optional
		
		.. note::
			
			Volatility is computed in this method using the formula: :math:`\forall t \in [0,T], \quad y_t = x_t + \epsilon_t`
	
		"""
		returns = self.returns(period=1)

	def save(self,filename='export.csv',separator=',',date_format='%d-%m%y'):
		""" Saves the data contained in the object to a csv file.

		:param filename: path and name of the file to export
		:type filename: str, optional
		:param separator: separator between columns in file.
		:type separator: str, optional
		"""
		self.data.to_csv(filename,sep=separator,date_format='')

	def plot(self):
		""" Plots the time series."""
		self.data.plot()
		plt.show()

	def filter(self, method="L1Filter",number_simulations=100, burns=50,total_variation=2):
		""" Filters the trend of the time series.

		:param method: path and name of the file to export
		:type method: str, optional
		:param number_simulations: number of simulations in the MCMC algorithm
		:type number_simulations: int, optional
		:param burns: number of draws dismissed as burning samples
		:type burns: int, optional
		"""
		mcmc = MCMC(self, StrategyFactory.create(method,self.data.as_matrix()[:,0],total_variation_order=total_variation))
		mcmc.run(number_simulations)
		trend = mcmc.output(burns,"trend")
		self.data = self.data.join(DataFrame(trend,index=self.data.index,columns=[method]))
