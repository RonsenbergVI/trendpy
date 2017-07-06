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

from scipy.stats import gamma
from pandas import DataFrame, date_range

class TestSamplers(unittest.TestCase):

	def setUp(self):
		self.sampler = L1Filter(gamma.rvs(3,size=date_range(start='2014-01-01', end='2015-04-03',freq='D').size))

	def tearDown(self):
		self.sampler = Sampler()

	def test_empty_parameters_list(self):
		self.assertEqual(self.sampler.parameters.list,{})

	def test_empty_parameters_hierarchy(self):
		self.assertEqual(self.sampler.parameters.hierarchy,[])

	def test_parameter_is_multivariate(self):
		self.sampler.define_parameters()
		self.assertTrue(self.sampler.parameters['omega'].is_multivariate() and not self.sampler.parameters['sigma2'].is_multivariate())

	def test_remove_all(self):
		self.sampler.define_parameters()
		param1 = self.sampler.parameters['omega']
		param2 = self.sampler.parameters['sigma2']
		self.sampler.parameters.clear()
		self.assertTrue(not param1 in self.sampler.parameters and not param2 in self.sampler.parameters)

	def test_hierarchy(self):
		self.sampler.define_parameters()
		self.assertTrue(self.sampler.parameters.hierarchy.index('trend') < self.sampler.parameters.hierarchy.index('omega'))

	def test_parameters_before_initial_value(self):
		self.sampler.define_parameters()
		for name in self.sampler.parameters.hierarchy:
			self.assertIsNone(self.sampler.parameters[name].current_value)

	def test_parameters_length(self):
		self.sampler.define_parameters()
		self.assertEqual(len(self.sampler.parameters),4)

	def test_size_initial_values(self):
		self.sampler.define_parameters()
		for name in self.sampler.parameters.hierarchy:
			self.sampler.parameters[name].current_value = self.sampler.initial_value(name)
			self.assertIsNotNone(self.sampler.parameters[name].current_value)

	def test_distribution_parameters(self):
		self.sampler.define_parameters()
		for name in self.sampler.parameters.hierarchy:
			self.sampler.parameters.list[name].current_value = self.sampler.initial_value(name)
		for name in self.sampler.parameters.hierarchy:
			self.assertIsInstance(self.sampler.distribution_parameters(name),dict)

	def test_random_draw_size(self):
		self.sampler.define_parameters()
		for name in self.sampler.parameters.hierarchy:
			self.sampler.parameters[name].current_value = self.sampler.initial_value(name)
		for name in self.sampler.parameters.hierarchy:
			if self.sampler.parameters[name].is_multivariate():
				self.assertEqual(self.sampler.parameters[name].current_value.size,self.sampler.generate(name).size)

if __name__ == "__main__":
	unittest.main()
