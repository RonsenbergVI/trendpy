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

from numpy import zeros, reshape
from scipy.stats import rv_continuous

__all__ = ['Parameter','Parameters','MCMC']

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
		
class Distribution(rv_continuous):
	pass

class MCMC(object):

	def __init__(self, data, strategy):
		self.data = data
		self.strategy = strategy
		self.simulations = None

	def summary(self):
		smry = ""
		return smry

	def distribution_parameters(self, parameter_name, *args, **kwargs):
		return self.strategy.distribution_parameters(parameter_name, *args, **kwargs) # returns a dictionary

	def generate(self, parameter_name):
		return self.strategy.generate(parameter_name)

	def output(self, burn, parameter_name):
		return self.strategy.output(self.simulations, burn, parameter_name)
		
	def define_parameters(self):
		return self.strategy.define_parameters()

	def initial_value(self,parameter_name):
		return self.strategy.initial_value(parameter_name)

	def run(self, number_simulations=100):
		self.simulations = {key : zeros((param.size[0],param.size[1],number_simulations)) for (key, param) in self.strategy.parameters.list.items()}

		for name in self.strategy.parameters.hierarchy:
			self.strategy.parameters.list[name].current_value = self.initial_value(name)
			
		for i in range(number_simulations):
			print("== step %i ==" % (int(i+1),))
			restart_step = True
			while restart_step:
				for name in self.strategy.parameters.hierarchy:
					print("== parameter %s ==" % name)
					try:
						self.strategy.parameters.list[name].current_value = self.generate(name)
						self.simulations[name][:,:,i] = self.strategy.parameters.list[name].current_value.reshape(self.strategy.parameters.list[name].size)
						restart_step = False
					except:
						print("== restart step %i ==" % i)
						restart_step = True
						break

class ConvergenceAnalysis(object):
	
