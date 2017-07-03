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

	def test_empty_parameters(self):
		P = Parameters()
		self.assertEqual(P.list,{})

	def test_parameter_is_multivariate(self):
		p = Parameter('test',rv_continuous,(10,10))
		q = Parameter('test2',rv_continuous,(1,1))
		self.assertTrue(p.is_multivariate() and not q.is_multivariate())

	def test_initial_current_value(self):
		p = Parameter('test',rv_continuous,(10,10))
		self.assertIsNone(p.current_value)

	def test_add_parameter(self):
		P = Parameters()
		p = Parameter('test',rv_continuous,(10,10))
		P.append(p)
		self.assertTrue(p.name in P.list and p.name in P.hierarchy)

	def test_remove_all(self):
		P = Parameters()
		p = Parameter('test',rv_continuous,(10,10))
		P.append(p)
		P.removeAll()
		self.assertTrue(not p.name in P.list and not p.name in P.hierarchy)

	def test_hierarchy(self):
		P = Parameters()
		p = Parameter('test',rv_continuous,(10,10))
		q = Parameter('test2',rv_continuous,(1,1))
		P.append(p)
		P.append(q)
		self.assertTrue(P.hierarchy.index(p.name) < P.hierarchy.index(q.name))

	def test_parameters_before_initial_value(self):
		S = L1Filter(gamma.rvs(10,size=date_range(start='2014-01-01', end='2015-04-03',freq='D').size))
		print(S.parmeters.hierarchy)
		for name in S.parameters.hierarchy:
			self.assertEqual(S.parameters.list[name].current_value,None)

	def test_parameters_length(self):
		S = L1Filter(gamma.rvs(10,size=date_range(start='2014-01-01', end='2015-04-03',freq='D').size))
		self.assertEqual(len(S.parameters),4)

	def test_size_initial_values(self):
		S = L1Filter(gamma.rvs(10,size=date_range(start='2014-01-01', end='2015-04-03',freq='D').size))
		for name in S.parameters.hierarchy:
			S.parameters.list[name].current_value = S.initial_value(name)
			self.assertNotEqual(S.parameters.list[name].current_value,None)
			
	def test_distribution_parameters(self):
		S = L1Filter(gamma.rvs(10,size=date_range(start='2014-01-01', end='2015-04-03',freq='D').size))
		for name in S.parameters.hierarchy:
			S.parameters.list[name].current_value = S.initial_value(name)
		for name in S.parameters.hierarchy:
			self.assertIsInstance(S.distribution_parameters(name),dict)

	def test_random_draw_size(self):
		S = L1Filter(gamma.rvs(10,size=date_range(start='2014-01-01', end='2015-04-03',freq='D').size))
		for name in S.parameters.hierarchy:
			S.parameters.list[name].current_value = S.initial_value(name)
		for name in S.parameters.hierarchy:
			if S.parameters.list[name].is_multivariate():
				self.assertEqual(S.parameters.list[name].current_value.size,S.generate(name).size)

if __name__ == "__main__":
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TestSamplers))
	unittest.TextTestRunner(verbosity=2).run(suite)
	

	
