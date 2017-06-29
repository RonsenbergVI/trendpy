# -*- coding: utf-8 -*-

# tests_factory.py

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

#from __future__ import absolute_import


import os 
import sys
import inspect
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,parentdir) 

from trendpy.factory import *
from trendpy.samplers import *


class TestFactory(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		SamplerFactory.removeAll()

	def test_initial_dictionary_is_empty(self):
		self.assertEqual(SamplerFactory.factories,{})

	def test_is_sampler(self):
		s = Sampler()
		self.assertIsInstance(SamplerFactory.create("Sampler"),type(s))
		
	def test_factory_is_added_manually(self):
		s = Sampler()
		SamplerFactory.add("test",Sampler.Factory)
		self.assertTrue("test" in SamplerFactory.factories.keys())
		
	def test_factory_is_removed(self):
		s = Sampler()
		SamplerFactory.add("test",Sampler.Factory)
		SamplerFactory.remove("test")
		self.assertTrue("test" not in SamplerFactory.factories.keys())
	
if __name__ == "__main__":
	unittest.main()
