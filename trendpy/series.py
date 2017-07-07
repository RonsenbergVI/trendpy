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

from __future__ import absolute_import

import matplotlib.pyplot as plt
import seaborn as sns

from trendpy.globals import DATE_FORMAT
from trendpy.mcmc import MCMC
from trendpy.factory import SamplerFactory

from statsmodels.iolib.table import SimpleTable
from statsmodels.iolib.summary import Summary, fmt_2cols, fmt_params

from datetime import datetime

from calendar import monthrange

from pandas import DataFrame, read_csv, period_range, Series

from numpy import array, sqrt, zeros_like, triu_indices_from, random, bool, nan
from numpy.linalg import norm

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

	def __len__(self):
		return self.data.size

	def __str__(self):
		return self.data.__str__()

	@staticmethod
	def from_csv(filename):
		""" Instantiate new time series from a csv file where the first
			column is a timestamp or a date or a datetime. For now

		:param filename: path of the file with extension (.csv or .txt)
		:type filename: str
		:return: the price time series
		:rtype: `trendpy.series.Series`
		"""
		time_series=Series()
		time_series.data=read_csv(filename,index_col=0,parse_dates=True)
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

		right = [('Ann. return:', 100.0*self.annualized_return()),
					 ('Ann. volatility:', 100.0*self.annualized_volatility()),
					 ('Max drawdown:', 100.0*self.max_drawdown()),
					 ('Drawdown Duration: ', 0),
					 ('Skewness:', self.skewness()),
					 ('Kurtosis:', self.kurtosis()),
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
		return float((252/len(returns))*sum(returns))

	def annualized_volatility(self):
		""" Computes the annualized return over a given period.

		:return: annualized return on the whole time series.
		:rtype: float
		"""
		returns = self.returns().data.as_matrix()
		T = len(returns)
		r = self.annualized_return()/T
		return float(sqrt((252/(len(returns)-1))*sum(array([(ret-r)**2 for ret in returns]))))

	def skewness(self):
		""" Computes the skewness of the returns empirical distribution.

		:return: skewness on the whole time series returns.
		:rtype: float
		"""
		returns = self.returns().data.as_matrix()
		T = len(returns)
		s = self.annualized_volatility()/sqrt(T)
		r = self.annualized_return()/T
		return float((T/((T-1)*(T-2)))*sum(array([((ret-r)/s)**3 for ret in returns])))

	def kurtosis(self):
		""" Computes the kurtosis of the returns empirical distribution.

		:return: kurtosis on the whole time series returns.
		:rtype: float
		"""
		returns = self.returns().data.as_matrix()
		T = len(returns)
		s = self.annualized_volatility()/sqrt(T)
		r = self.annualized_return()/T
		return float(((T*(T+1))/((T-1)*(T-2)*(T-3)))*sum(array([((ret-r)/s)**4 for ret in returns])) - (3*(T-1)**2)/((T-2)*(T-3)))

	def max_drawdown(self,window=30):
		""" Computes the maximum drawdown of the price time series.

		:param window: number of observations used.
		:type window: int, optional
		:return: drawdown duration of the time series.
		:rtype: float
		"""
		return float(min(self.rolling_max_drawdown(window=window).data.as_matrix()))

	def periodic_returns(self,show=True):
		""" Computes the maximum drawdown of the price time series.

		:return: periodic return plot of the time series.
		:rtype: float
		"""
		sns.set(style="white")
		start_date = self.data.index[0]
		end_date = self.data.index[-1]
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
				try:
					returns = self.data['%s-%s' % (year,m)].pct_change(periods=1).fillna(0).as_matrix()
					d.loc[year,month] = (252/len(returns))*sum(returns)
				except:
					d.loc[year,month] = nan
				m+=1
		f, ax = plt.subplots(figsize=(7, 7))
		title = '%s: periodic returns' % self.data.columns[0]
		plt.title(title,fontsize=14)
		ax.title.set_position([0.5,1.05])
		sns.heatmap(d,ax=ax,fmt="d",cmap="RdYlGn",linewidth=0.5)
		if show: plt.show()
		return d

	def rolling_max_drawdown(self,window=30):
		""" Computes the rolling maximum drawdown of the time series.

		:param window: number of observations used.
		:type window: int, optional
		:return: rolling maximum drawdown of the time series.
		:rtype: `pandas.DataFrame`
		"""
		price = self.data.as_matrix()
		rolling_drawdown = Series()
		data = DataFrame(array([price[i-1]/max(price[i-window:i])-1 for i in range(window,len(price),1)]),index=self.data.index[window:],columns=['%s - max drawdown' % self.data.columns[0]])
		rolling_drawdown.data = data
		return rolling_drawdown

	def rolling_volatility(self,window=360):
		""" Computes the annualized rolling volatility of the time series
		    with annualization possible. The formula used is the following:

		:param window: number of observations used.
		:type window: int, optional
		:param annualize:
		:type annualize: str, optional
		:return: rolling_volatility of the time series.
		:rtype: `pandas.DataFrame`
		"""
		returns = self.returns(period=1).data.as_matrix()
		rolling_vol = Series()
		data = DataFrame(array([(252/(len(returns[i-window:i])-1))*norm(returns[i-window:i],ord=2) for i in range(window,len(returns),1)]),index=self.data.index[window:],columns=['%s - rolling volatility' % self.data.columns[0]])
		rolling_vol.data = data
		return rolling_vol

	def save(self,filename='export.csv',separator=',',date_format='%d-%m-%y'):
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

	def filter(self, method="L1Filter",number_simulations=100, burns=50,total_variation=2,merge=True):
		""" Filters the trend of the time series.

		:param method: path and name of the file to export
		:type method: str, optional
		:param number_simulations: number of simulations in the MCMC algorithm
		:type number_simulations: int, optional
		:param burns: number of draws dismissed as burning samples
		:type burns: int, optional
		:param merge: joind the filtered trend to the current Series instance.
		:type merge: bool, optional
		:return: Series of trend filtered.
		:rtype: `pandas.DataFrame`
		"""
		mcmc = MCMC(SamplerFactory.create(method,self.data.as_matrix()[:,0],total_variation_order=total_variation))
		mcmc.run(number_simulations)
		trend = mcmc.output(burns,"trend")
		filtered_trend = Series()
		filtered_trend.data = DataFrame(trend,index=self.data.index,columns=[method])
		if merge: self.data = self.data.join(filtered_trend.data)
		return filtered_trend
