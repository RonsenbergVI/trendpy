# -*- coding: utf-8 -*-

# __init__.py

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

from collections import Mapping

from trendpy.globals import *

from trendpy.version import version
from trendpy.factory import SamplerFactory
from trendpy.mcmc import MCMC


__version__ = version

def filter(data, method="L1", number_simulations=100, burns=50, total_variation=2, max_restart=5, verbose=0):
	""" Filters the trend of the time series.

	:param data: 1D time series to be filtered
	:type data: list, optional (data can also be a numpy array or a pandas.Series)
	:param method: path and name of the file to export
	:type method: str, optional
	:param number_simulations: number of simulations in the MCMC algorithm
	:type number_simulations: int, optional
	:param burns: number of draws dismissed as burning samples
	:type burns: int, optional
	:param max_restart: number of times the MCMC routine is allowed to restart.
	:type max_restart: int
	:param verbose: control console log information detail.
	:type verbose: int
	:return: Iterable of the same type with initial data and trend filtered time series.
	:rtype: `iterable`
	"""
	mcmc = MCMC(SamplerFactory.create(method,_tosequence(data),total_variation_order=total_variation))
	mcmc.run(number_simulations=number_simulations,max_restart=max_restart,verbose=verbose)
	trend = mcmc.output(burns,"trend")
	return trend


def _tosequence(X):
    """Turn X into a sequence or ndarray.""" #(code taken from scikit-learn)
    if isinstance(X, Mapping):  # single sample
        return [X]
    else:
        return tosequence(X)
