# -*- coding: utf-8 -*-

# globals.py

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

from collections import Sequence
from numpy import zeros, asarray, ndarray

__all__ = ['derivative_matrix','tosequence']

def derivative_matrix(size, order=2):
	""" Computes a discrete difference operator.

	:param size: dimension of the matrix.
	:type size: int
	:param order: derivation order.
	:type order: int
	:return: Discrete difference operator
	:rtype: `Numpy.dnarray`
	"""
	D=zeros((size-order, size))
	if order==0:
		d=[1]
	elif order==1:
		d=[-1,1]
	elif order==2:
		d=[1,-2,1]
	elif order==3:
		d=[-1,3,-3,1]
	for n in range(size-order):
		for l in range(order+1):
			D[n,n+l]=d[l]
	return D

def tosequence(x):
    """Cast iterable x to a Sequence. (Code from scikit-learn)

    Parameters
    ----------
    x : iterable
    """
    if isinstance(x, ndarray):
        return asarray(x)
    elif isinstance(x, Sequence):
        return x
    else:
        return list(x)
