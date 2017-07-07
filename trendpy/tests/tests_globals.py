# -*- coding: utf-8 -*-

# tests_globals.py

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

from numpy.random import randint

from numpy import inf

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0,parent_dir)

import trendpy.globals

class TestGlobals(unittest.TestCase):

	def setUp(self):
		self.order = int(randint(low=0,high=4,size=1))
		self.dim = int(randint(low=self.order+2,high=2000,size=1))
		self.D = trendpy.globals.derivative_matrix(self.dim,self.order)

	def tearDown(self):
		self.dim = None
		self.order = None
		self.D = None
		
	def test_derivative_matrix_size(self):
		self.assertEqual(self.D.shape,(self.dim-self.order,self.dim))
		
if __name__ == "__main__":
	unittest.main()
	
