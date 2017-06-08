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

from trendpy.timeseries import TimeSeries
from numpy.linalg import norm
from numpy import dot, ones, zeros

__all__ = ['Filter','L1','L2','options','derivative']


def derivative_matrix(size, order=1):
    # """
    # Compute discrete derivatives matrix with size (size-order,size)
    #
    # Parameters
    # ----------
    # size : integer
    #     number of observations
    # order : integer, optional
    #     order of the total variation
    #
    # Returns
    # -------
    # derivative_matrix:
    #     discrete derivative matrix
    # """
    D=zeros((size-order, size))
    if order==1:
        d=[-1,1]
    elif order==2:
        d=[1,-2,1]
    for n in range(size-order):
        for l in range(order+1):
            D[n,n+l]=d[l]
    return D

class Options(object):
    # """
    # Wrapper class containing all the parameters to configure a filter
    #
    # Methods that raise NotImplementedError should be overriden by
    # any subclass.
    # """

    def __init__(self,*args):
        self.norm=args[0]
        self.total_variation=args[1]
        self.parameters=args[2]

class Filter(object):
    # """
    # Abstract class for MCMC filters
    #
    # Methods that raise NotImplementedError should be overriden by
    # any subclass.
    # """

    def __init__(self,):
        self.price = None
        self.size = 0
        self.options = None
        self.derivative_matrix = None

    def filter(self,*args):
        # """
        # """
        raise NotImplementedError("Must be overriden")


class L1(Filter):

    def __init__(self, price=None, options=None):
        self.price = price
        self.size = len(price)
        self.options = options
        self.derivative_matrix = derivative_matrix(self.size, options.total_variation_order)

    #def filter(self, *args):
