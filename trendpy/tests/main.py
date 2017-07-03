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

import os
import sys
import inspect
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,parentdir)

import trendpy.tests.tests_factory
import trendpy.tests.tests_globals
import trendpy.tests.tests_mcmc
import trendpy.tests.tests_samplers
import trendpy.tests.tests_series

suite = unittest.TestSuite()

suite.addTest(unittest.makeSuite(trendpy.tests.tests_factory.TestFactory))
suite.addTest(unittest.makeSuite(trendpy.tests.tests_globals.TestGlobals))
suite.addTest(unittest.makeSuite(trendpy.tests.tests_mcmc.TestMCMC))
suite.addTest(unittest.makeSuite(trendpy.tests.tests_samplers.TestSamplers))
suite.addTest(unittest.makeSuite(trendpy.tests.tests_series.TestSeries))

unittest.TextTestRunner(verbosity=2).run(suite)
