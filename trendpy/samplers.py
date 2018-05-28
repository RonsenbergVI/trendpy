# -*- coding: utf-8 -*-

# samplers.py

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

__all__ = ['Parameter','Parameters','Sampler','L1']

class Parameter(object):
	""" Implements an unknown parameter to be estimated

	Examples
	--------

	We first need to import the wanted posterior distribution in `Scipy`:

	>>> from scipy.stats import norm

	and then we can instanciate parameter:

	>>> param1 = Parameter('lambda',norm,(1,1),0.1)

	"""

	def __init__(self, name, distribution, size, current_value=None):
		""" Creates a parameter to estimate in the MCMC algorithm.

		:param name: Name of the parameter (unique identification)
		:type name: string
		:param distribution: Posterior Probability distribution of the parameter.
		:type distribution: `Scipy.stats.rv_continuous`
		:param size: Dimension of the parameter.
		:type name: tuple
		:param current_value: Current value of the parameter
		:type current_value: array
		"""
		self.name = str(name)
		self.distribution = distribution
		self.size = size
		self.current_value = current_value

	@property
	def current_value(self):
		"""Parameter current value (last generated)"""
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
		""" Checks if the parameter is univariate."""
		return not self.size == (1,1)

class Parameters(object):
	""" Implements the set of parameters to be estimated

	Examples
	--------

	We first need to import the wanted posterior distribution in `Scipy.stats`:

	>>> from scipy.stats import invgamma

	then we can create an empty parameter set and add a new parameter:

	>>> param1 = Parameter('sigma2',invgamma,(1,1),0.09)
	>>> params = Params()
	>>> params.append(param1)
	>>> print(params)
	"""
	def __init__(self, list=None, hierarchy=None):
		""" Creates a parameter set to estimate in the MCMC algorithm.

		:param list: A dictionary with the parameters to estimate
		:type list: dict
		:param hierarchy: List containing the order in which
	    		the Gibbs sampler updates the parameter values.
		:type hierarchy: array
		"""
		self.list = list
		self.hierarchy = hierarchy

	@property
	def list(self):
		""" Dictionary containing the parameters to be
			estimated.
		"""
		return self.__list

	@list.setter
	def list(self, new_value):
		self.__list = new_value if new_value is not None else {}

	@property
	def hierarchy(self):
		""" List containing the order in which
			the Gibbs sampler updates the
			parameter values.
		"""
		return self.__hierarchy

	@hierarchy.setter
	def hierarchy(self, new_value):
		self.__hierarchy = new_value if new_value is not None else []

	def __len__(self):
		return len(self.list)

	def __str__(self):
		descr = '(parameters: ----------------------- \n'
		descr += ', \n'.join(['name: %s, distribution: %s, size: %s' % (str(l.name), l.distribution.__str__(), l.size) for l in self.list.values()])
		descr += '\n ----------------------- )'
		return descr

	def __getitem__(self, key):
		if isinstance(key,str):
			try:
				return self.list[key]
			except KeyError:
				print("Key %s not found in parameter set" % key)
			except:
				print("Wrong key")
		elif isinstance(key,int):
			try:
				return self.list[self.hierarchy[key]]
			except KeyError:
				print("Key %s not found in parameter set" % key)
			except IndexError:
				print("Index out of bounds: %s > %s" % (key,len(self.hierarchy)))
		else:
			raise TypeError("Wrong Type")

	def __delitem__(self,key):
		pass

	def __contains__(self, item):
		if isinstance(item,Parameter):
			try:
				return item.name in self.hierarchy
			except KeyError:
				print("Key %s not found in parameter set" % key)
			except:
				print("Wrong key: %s" % item.name)
		else:
			raise TypeError("Wrong Type")

	def append(self, parameter):
		""" Adds a parameter to the parameter set.
			First parameter added is the first in the
			hierarchy.
		:param parameter: parameter to estimate
		:type parameter: trendpy.Parameter
		"""
		if not parameter.name in self.list:
			self.list[parameter.name] = parameter
			self.hierarchy.append(parameter.name)

	def clear(self):
		""" Removes all parameters."""
		self.list = None
		self.hierarchy = None

class Sampler(object):
	""" Abstract class for implementing Gibbs sampling algorithms and providing outputs."""

	def __init__(self):
		self.parameters = None
		self.data = None
		self.options = None
		self.derivative_matrix = None
		self.parameters = None

	def define_parameters(self):
		""" Method to set the parameter set to be updated
			in the MCMC algorithm.
		"""
		raise NotImplementedError("Must be overriden")

	def initial_value(self,parameter_name):
		""" Method that sets the initial value of the
			parameters to be estimated.

		:param parameter_name: name of the parameter.
		:type parameter_name: str
		:return: initial value of the parameter
		:rtype: `Numpy.dnarray`
        """
		raise NotImplementedError("Must be overriden")

	def distribution_parameters(self, parameter_name):
		""" Method that sets the parameters of the posterior
			distribution of the parameters to be estimated.

		:param parameter_name: name of the parameter.
		:type parameter_name: str
		:return: dictionary the parameters needed to compute the
			next value of the Markov chain for the parameter with name:
			parameter_name.
		:rtype: dict
        """
		raise NotImplementedError("Must be overriden")

	def generate(self,parameter_name):
		""" This method handles the generation of the random draws of
			the Markov chain for each parameters.

		:param parameter_name: name of the parameter of interest
		:type parameter_name: string
		:return: random draw from the posterior probability distribution
		:rtype: `Numpy.dnarray`
        """
		raise NotImplementedError("Must be overriden")

	def output(self, simulations, burn, parameter_name):
		""" Computes the poserior mean of the parameters.

		:param simulations: history of the Markov chain simulation
		:type simulations: dict
		:param burn: number of draws dismissed as burning samples
		:type burn: int
		:param parameter_name: name of the parameter of interest
		:type parameter_name: string
		:return: output of the MCMC algorithm
		:rtype: `Numpy.dnarray`
        """
		raise NotImplementedError("Must be overriden")

	class Factory(object):
		def create(self,*args,**kwargs):
			return Sampler()

class L1(Sampler):

	def __init__(self,data,alpha=0.1,rho=0.1,total_variation_order=2):
		self.rho = rho
		self.alpha = alpha
		self.__data = data
		self.size = len(data)
		self.total_variation_order = total_variation_order
		self.derivative_matrix = derivative_matrix(self.size, self.total_variation_order)
		self.define_parameters()


	@property
	def data(self):
		return self.__data

	@property
	def parameters(self):
		""" List containing the parameters to estimate."""
		return self.__parameters

	@parameters.setter
	def parameters(self, new_value):
		self.__parameters = new_value if new_value is not None else []

	def define_parameters(self):
		params=Parameters()

		params.append(Parameter("trend", multivariate_normal, (self.size,1)))
		params.append(Parameter("sigma2", invgamma, (1,1)))
		params.append(Parameter("lambda2", gamma, (1,1)))
		params.append(Parameter("omega", invgauss, (self.size-self.total_variation_order,1)))

		self.parameters = params

	def initial_value(self,parameter_name):
		if parameter_name=='trend':
			return array([(4*i+10)/20 for i in range(self.size)])
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
			pos = self.size-self.total_variation_order-1+self.alpha
			loc = 0.5*(norm(dot(self.derivative_matrix,self.parameters.list['trend'].current_value),ord=1))/self.parameters.list['sigma2'].current_value+self.rho
			scale = 1
		elif parameter_name==str('omega'):
			pos = [sqrt(((self.parameters.list['lambda2'].current_value**2)*self.parameters.list['sigma2'].current_value)/(dj**2)) for dj in dot(self.derivative_matrix,self.parameters.list['trend'].current_value)]
			loc = 0
			scale = self.parameters.list['lambda2'].current_value**2
		return {'pos' : pos, 'loc' : loc, 'scale' : scale}

	def generate(self,parameter_name):
		distribution = self.parameters.list[parameter_name].distribution
		parameters = self.distribution_parameters(parameter_name)

		if parameter_name=='trend':
			return distribution.rvs(parameters['mean'],parameters['cov'])
		elif parameter_name=='omega':
			return array([1/distribution.rvs(parameters['pos'][i],loc=parameters['loc'],scale=parameters['scale']) for i in range(len(self.parameters.list['omega'].current_value))]).reshape(self.parameters.list['omega'].current_value.shape)
		return distribution.rvs(parameters['pos'],loc=parameters['loc'],scale=parameters['scale']) #pb with the parameter name

	def output(self, simulations, burn, parameter_name):
		out = mean(simulations[parameter_name][:,:,burn:],axis=2)
		return out

	class Factory(object):
		def create(self,*args,**kwargs):
			return L1(args[0],total_variation_order=kwargs['total_variation_order'])
