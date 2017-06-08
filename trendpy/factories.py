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

from trendpy.filter import Options
from trendpy.mcmc import Parameter, Parameters
from scipy.stats import (norm, invgauss, invgamma, gamma, multivariate_normal)

__all__ = ['OptionsFactory','ParametersFactory']

class OptionsFactory(object):

    @staticmethod
    def hp_filter():
        return Options(2,2,None)

    @staticmethod
    def l1_filter():
        return Options(1,1,{'xtol':1e-8,'disp':True})

    @staticmethod
    def custom_filter():
        return Options(1,1,{'xtol':1e-8,'disp':True})

class ParametersFactory(object):

    @staticmethod
    def l1(size, order):
        parameters=Parameters()
        parameters.append(Parameter("trend", multivariate_normal, (size,size)))
        parameters.append(Parameter("sigma", invgamma, (1,1)))
        parameters.append(Parameter("lambda", gamma, (1,1)))
        for i in range(size-order):
            parameters.append(Parameter("omega%d" % i, invgamma, (1,1)))
        return parameters

    #@staticmethod
    #def l2(size, order):
