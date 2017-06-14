# strategy.py

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

from scipy.stats import rv_continuous

__all__ = ['Parameter','Parameters','Strategy']


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
		
		
class StrategyFactory(object):
	
