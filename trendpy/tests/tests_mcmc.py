# -*- coding: utf-8 -*-

# tests_mcmc.py

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

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0,parent_dir)

import trendpy.mcmc
import trendpy.samplers

class TestMCMC(unittest.TestCase):

	def setUp(self):
		self.s = trendpy.samplers.Sampler()
		self.mcmc = trendpy.mcmc.MCMC(self.s)

	def tearDown(self):
		self.s = trendpy.samplers.Sampler()
		self.mcmc = trendpy.mcmc.MCMC(self.s)

	def test_define_parameters(self):
		self.assertEqual(self.s.define_parameters,self.mcmc.sampler.define_parameters)

	def test_distribution_parameters(self):
		self.assertEqual(self.s.distribution_parameters,self.mcmc.sampler.distribution_parameters)

	def test_generate(self):
		self.assertEqual(self.s.generate,self.mcmc.sampler.generate)

if __name__ == "__main__":
	unittest.main()
	
