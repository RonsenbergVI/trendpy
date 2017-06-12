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

from trendpy.mcmc import Parameter, Parameters
from scipy.stats import (norm, invgauss, invgamma, gamma, multivariate_normal)

from datetime import date, timedelta
from pandas import DataFrame, date_range, Series
from scipy.stats import invgamma, multivariate_normal, gamma, invgauss, norm as randnorm
from numpy import (sqrt, zeros, full, eye, transpose, multiply, dot, nan, floor, ones, diag, float, mean, ndindex, array)
from numpy.linalg import eigvals, norm, inv

__all__ = ['Options','OptionsFactory','ParametersFactory','MCMCStrategy','L1Strategy']

def derivative_matrix(size, order=1):
	print("derivative_matrix")
	D=zeros((size-order, size))
	if order==1:
		d=[-1,1]
	elif order==2:
		d=[1,-2,1]
	elif order==3:
		d=[-1,3,-3,1]
	for n in range(size-order):
		for l in range(order+1):
			D[n,n+l]=d[l]
	return D

class Options(object):

    def __init__(self, norm=1, total_variation_order=2):
        self.norm = norm
        self.total_variation_order = total_variation_order
		#self.autoregession_order
		#self.seasonality
		#self.levelshift

class OptionsFactory(object):

    @staticmethod
    def l1_filter():
        return Options(1,2)

class ParametersFactory(object):

	@staticmethod
	def l1_filter(size, order):
		parameters=Parameters()
		# two dimension shape compulsory
		parameters.append(Parameter("trend", multivariate_normal, (size,1)))
		parameters.append(Parameter("sigma2", invgamma, (1,1)))
		parameters.append(Parameter("lambda2", gamma, (1,1)))
		parameters.append(Parameter("omega", invgauss, (size-order,1)))
		print(parameters)
		return parameters

class MCMCStrategy(object):

	def __init__(self):
		self.parameters = None
		self.data = None

	def distribution_parameters(self, parameter_name):
		raise NotImplementedError("Must be overriden")

class L1Strategy(MCMCStrategy):

	def __init__(self, data,alpha=1,rho=0.01):
		self.data = data
		self.size = len(data)
		self.options = OptionsFactory.l1_filter()
		self.parameters = ParametersFactory.l1_filter(self.size,self.options.total_variation_order)
		self.derivative_matrix = derivative_matrix(self.size, self.options.total_variation_order)
		self.alpha = alpha
		self.rho = rho
		
	def parameters(self):
		

	def initial_value(self,parameter_name):
		if parameter_name=='trend':
			return array([(4*i+10) for i in range(self.size)])
		elif parameter_name=='sigma2':
			return 0.8
		elif parameter_name=='lambda2':
			return 1
		elif parameter_name==str('omega'):
			return 0.8*array([(30*(i/2)+3)/(2*(i/2)+35) for i in range(self.size-self.options.total_variation_order)])

	def distribution_parameters(self, parameter_name):
		if parameter_name=='trend':
			E = dot(dot(self.derivative_matrix.T,inv(diag(self.parameters.list['omega'].current_value))),self.derivative_matrix)
			mean = dot(inv(eye(self.size)+E),self.data)
			cov = (self.parameters.list['sigma2'].current_value)*inv(eye(self.size)+E)
			return {'mean' : mean, 'cov' : cov}
		elif parameter_name=='sigma2':
			E = dot(dot(self.derivative_matrix.T,inv(diag(self.parameters.list['omega'].current_value))),self.derivative_matrix)
			pos = self.size
			loc = 0
			scale = 0.5*dot((self.data-dot(eye(self.size),self.parameters.list['trend'].current_value)).T,(self.data-dot(eye(self.size),self.parameters.list['trend'].current_value)))+0.5*dot(dot(self.parameters.list['trend'].current_value.T,E),self.parameters.list['trend'].current_value)
		elif parameter_name=='lambda2':
			pos = self.size-2+self.alpha
			loc = 0.5*(norm(dot(self.derivative_matrix,self.parameters.list['trend'].current_value),ord=1))/self.parameters.list['sigma2'].current_value+self.rho
			scale = 1
		elif parameter_name==str('omega'):
			pos = [sqrt((self.parameters.list['lambda2'].current_value**2*self.parameters.list['sigma2'].current_value)/(dj**2)) for dj in dot(self.derivative_matrix,self.parameters.list['trend'].current_value)]
			loc = 0
			scale = self.parameters.list['lambda2'].current_value*2
		return {'pos' : pos, 'loc' : loc, 'scale' : scale}

	def generate(self,parameter_name):
		distribution = self.parameters.list[parameter_name].distribution
		parameters = self.distribution_parameters(parameter_name)

		if parameter_name=='trend':
			return distribution.rvs(parameters['mean'],parameters['cov']) 
		elif parameter_name=='omega':
			result = zeros(self.parameters.list['omega'].current_value.shape)
			for i in range(len(result)):
				result[i] = 1/distribution.rvs(parameters['pos'][i],loc=parameters['loc'],scale=parameters['scale']) 
			return result
		return distribution.rvs(parameters['pos'],loc=parameters['loc'],scale=parameters['scale']) #pb with the parameter name

	def output(self, simulations, burn, parameter_name):
		out = mean(simulations[parameter_name][:,:,burn:],axis=2)
		return out

