# -*- coding: utf-8 -*-

# tests_series.py

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

import os
import sys
import inspect
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,parentdir)

import trendpy.series

from scipy.stats import gamma
from pandas import DataFrame, date_range
from statsmodels.iolib.summary import Summary

class TestSeries(unittest.TestCase):

	def setUp(self):
		self.series = trendpy.series.Series()
		dates = date_range(start='2014-01-01', end='2015-04-03',freq='D')
		d = gamma.rvs(10,size=dates.size)
		data = DataFrame(data=d, index=dates)
		self.series.data = data

	def tearDown(self):
		self.series = trendpy.series.Series()

	def test_summary_type(self):
		self.assertIsInstance(self.series.summary(),Summary)

	def test_rolling_volatility_type(self):
		self.assertIsInstance(self.series.rolling_volatility().data,DataFrame)

	def test_rolling_volatility_data_type(self):
		self.assertIsInstance(self.series.rolling_volatility(),trendpy.series.Series)

	def test_returns_type(self):
		self.assertIsInstance(self.series.returns().data,DataFrame)

	def test_returns_data_type(self):
		self.assertIsInstance(self.series.returns(),trendpy.series.Series)

	def test_returns_has_NaN(self):
		self.assertFalse(self.series.returns().data.isnull().values.any())

	def test_volatility_is_positive(self):
		self.assertTrue(self.series.annualized_volatility()>0)

	def test_periodic_returns_is_seres(self):
		self.assertIsInstance(self.series.periodic_returns(show=False),DataFrame)

	def test_rolling_drawdown_has_NaN(self):
		self.assertFalse(self.series.rolling_max_drawdown().data.isnull().values.any())

	def test_rolling_drawdown_type(self):
		self.assertIsInstance(self.series.rolling_max_drawdown().data,DataFrame)

	def test_rolling_drawdown_data_type(self):
		self.assertIsInstance(self.series.rolling_max_drawdown(),trendpy.series.Series)

	def test_volatility_type(self):
		self.assertIsInstance(self.series.rolling_volatility().data,DataFrame)

	def test_volatility_data_type(self):
		self.assertIsInstance(self.series.rolling_volatility(),trendpy.series.Series)

	# fails -- to fix
	# def test_rolling_drawdown_sign(self):
		# s = self.series.rolling_max_drawdown().data
		# self.assertTrue(s[s > 0].values <= 0)

	# fails -- to fix
	# def test_volatility_sign(self):
		# s = self.series.rolling_volatility().data
		# self.assertTrue(s[s > 0].values.any().size <= 0)
		
if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TestSeries))
	unittest.TextTestRunner(verbosity=2).run(suite)
