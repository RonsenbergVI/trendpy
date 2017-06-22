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
import seaborn as sns

from trendpy.globals import DATE_FORMAT
from trendpy.mcmc import MCMC
from trendpy.factory import StrategyFactory

from statsmodels.iolib.table import SimpleTable
from statsmodels.iolib.summary import Summary, fmt_2cols, fmt_params

from datetime import datetime

from calendar import monthrange

from pandas import DataFrame, read_csv, period_range, Series

from numpy import array, sqrt, zeros_like, triu_indices_from, random, bool


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
			column is a timestamp or a date or a datetime. For now 

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
					('End: ',self.data.index[-1]),
					('Number of observations: ', len(self.data.index)),
					('Number of time series: ', len(self.data.columns)),
					('', ''),
					('', ''),
					('Date: ', datetime.now().strftime('%a, %b %d %Y %H:%M:%S'))]

		right = [('Ann. return:','%.2f%%' % float(100*self.annualized_return())),
					 ('Ann. volatility:','%.2f%%' % float(100*self.annualized_volatility())),
					 ('Max drawdown:', 0),
					 ('Drawdown Duration: ', 0),
					 ('Skewness:', 0),
					 ('Kurtosis:', 0),
					 ('t-test p value',0)]
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

	def returns(self,period=1):
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
		""" Computes the annualized return over a given period.

		:param period: period of interest either a year, year-month
		     or date range.
		:type period: str
		:return: annualized return on the whole time series.
		:rtype: float
		"""
		returns = self.returns().data.as_matrix()
		return (252/len(returns))*sum(returns)
		
	def annualized_volatility(self):
		""" Computes the annualized return over a given period.

		:return: annualized return on the whole time series.
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

	def periodic_returns(self):
		""" Computes the maximum drawdown of the price time series.
	
		:return: periodic return plot of the time series.
		:rtype: float
		"""
		sns.set(style="white")
		start_date = datetime.strptime(self.data.index[0],DATE_FORMAT)
		end_date = datetime.strptime(self.data.index[-1],DATE_FORMAT)
		#print(start_date)
		#print(end_date.year.__class__)
		#print(period_range(start_date.year,end_date.year,freq='A-DEC'))
		d = DataFrame(data=0,
		index=period_range(start_date.year,end_date.year,freq='A-DEC'),
		columns=list(['Jan',
		              'Feb',
					  'Mar',
					  'Apr',
					  'May',
					  'Jun',
					  'Jul',
					  'Aug',
					  'Sep',
					  'Oct',
					  'Nov',
					  'Dec']))
		for year in d.index.to_series().astype(str):
			m = 1
			for month in d.columns:
				print('%s-%s' % (year,m))
				print(self.annualized_return('%s-%s' % (year,m)))
				d.ix[year,month] = self.annualized_return('%s-%s' % (year,m))
				m+=1
		f, ax = plt.subplots(figsize=(7, 7))
		title = '%s: periodic returns' % self.data.columns[0] 
		plt.title(title,fontsize=14)
		ax.title.set_position([0.5,1.05])
		sns.heatmap(d,ax=ax,annot=True,fmt="d",cmap="YlGnBu")
		plt.show()

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
