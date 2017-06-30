# -*- coding: utf-8 -*-

# tests_samplers.py

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

from trendpy.samplers import *

from scipy.stats import rv_continuous, gamma

from pandas import DataFrame, date_range


class TestSamplers(unittest.TestCase):

	def setUp(self):
		self.p = Parameter('test',rv_continuous,(10,10))
		self.q = Parameter('test2',rv_continuous,(1,1))
		self.P = Parameters()
		dates = date_range(start='2014-01-01', end='2015-04-03',freq='D')
		d = gamma.rvs(10,size=dates.size)
		data = DataFrame(data=d, index=dates)
		self.S = L1Filter(data)

	def tearDown(self):
		self.P.removeAll()

	def test_empty_parameters(self):
		print('empty')
		self.assertEqual(self.P.list,{})
		self.assertEqual(self.P.hierarchy,[])

	def test_parameter_is_multivariate(self):
		self.assertTrue(self.p.is_multivariate() and not self.q.is_multivariate())

	def test_initial_current_value(self):
		self.assertIsNone(self.p.current_value)

	def test_add_parameter(self):
		self.P.append(self.p)
		self.assertTrue(self.p.name in self.P.list and self.p.name in self.P.hierarchy)
		self.P.removeAll()
		self.assertTrue(not self.p.name in self.P.list and not self.p.name in self.P.hierarchy)

	def test_hierarchy(self):
		self.P.append(self.p)
		self.P.append(self.q)
		self.assertTrue(self.P.hierarchy.index(self.p.name) < self.P.hierarchy.index(self.q.name))

	def test_parameters_distributions(self):
		for name in self.S.parameters.hierarchy:
			self.assertTrue(super(self.S.parameters.list[name].distribution)==rv_continuous or )
		
if __name__ == "__main__":
	unittest.main()
	
