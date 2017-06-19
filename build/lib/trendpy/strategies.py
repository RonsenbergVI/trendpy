# strategies.py

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

from numpy import eye, zeros, dot, array, diag, sqrt, mean

from scipy.stats import multivariate_normal, invgamma, invgauss, gamma
from numpy.linalg import inv, norm

from trendpy.globals import derivative_matrix

__all__ = ['Parameter','Parameters','Strategy','L1Filter','Lasso']

class Parameter(object):

	def __init__(self, name, distribution, size, current_value=None):
		self.name = str(name)
		self.distribution = distribution
		self.size = size
		self.current_value = current_value

	@property
	def current_value(self):
		return self.__current_value

	@current_value.setter
	def current_value(self, current_value):
		self.__current_value = current_value

	def __str__(self):
		return """
			parameter name : %s
			parameter distribution : %s
		""" % (self.name, self.distribution.__str__())

	def __len__(self):
		return 1

	def is_multivariate(self):
		return self.size == (1,1)

class Parameters(object):

	def __init__(self, list={}, hierarchy=[]):
		self.list = list
		self.hierarchy = hierarchy

	@property
	def parameters(self):
		return self.__list

	@parameters.setter
	def parameters(self, list):
		if not (list=={}):
			self.__list = list
		else:
			self.__list = {}

	@property
	def hierarchy(self):
		return self.__hierarchy

	@hierarchy.setter
	def hierarchy(self, hierarchy):
		self.__hierarchy = hierarchy

	def __len__(self):
		return len(self.list)

	def __str__(self):
		descr = '(parameters: ----------------------- \n'
		descr += ', \n'.join(['name: %s, distribution: %s, size: %s' % (str(l.name), l.distribution.__str__(), l.size) for l in self.list.values()])
		descr += '\n ----------------------- )'
		return descr

	def append(self, parameter):
		self.list[parameter.name] = parameter
		self.hierarchy.append(parameter.name)

class Strategy(object):

	def __init__(self):
		self.parameters = None
		self.data = None
		self.options = None
		self.derivative_matrix = None
		self.parameters = None

	def parameters(self):
		raise NotImplementedError("Must be overriden")

	def initial_value(self,parameter_name):
		raise NotImplementedError("Must be overriden")

	def distribution_parameters(self, parameter_name):
		raise NotImplementedError("Must be overriden")

	def generate(self,parameter_name):
		raise NotImplementedError("Must be overriden")

	def output(self, simulations, burn, parameter_name):
		raise NotImplementedError("Must be overriden")

class L1Filter(Strategy):

	def __init__(self,data,alpha=1,rho=0.01,total_variation_order=2):
		self.rho = rho
		self.alpha = alpha
		self.data = data
		self.size = len(data)
		self.total_variation_order = total_variation_order
		self.parameters = self.parameters()
		self.derivative_matrix = derivative_matrix(self.size, self.total_variation_order)
		
	def parameters(self):
		parameters=Parameters()

		parameters.append(Parameter("trend", multivariate_normal, (self.size,1)))
		parameters.append(Parameter("sigma2", invgamma, (1,1)))
		parameters.append(Parameter("lambda2", gamma, (1,1)))
		parameters.append(Parameter("omega", invgauss, (self.size-self.total_variation_order,1)))

		return parameters

	def initial_value(self,parameter_name):
		if parameter_name=='trend':
			return array([(4*i+10) for i in range(self.size)])
		elif parameter_name=='sigma2':
			return 0.8
		elif parameter_name=='lambda2':
			return 1
		elif parameter_name==str('omega'):
			return 0.8*array([(30*(i/2)+3)/(2*(i/2)+35) for i in range(self.size-self.total_variation_order)])

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
		
	class Factory(object):
		def create(self,*args,**kwargs):
			return L1Filter(args[0],total_variation_order=kwargs['total_variation_order'])

class Lasso(Strategy):
	pass
