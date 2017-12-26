# -*- coding: utf-8 -*-

# mcmc.py

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

from numpy import reshape, zeros

class MCMC(object):

	def __init__(self, sampler):
		self.sampler = sampler
		self.simulations = None

	def define_parameters(self):
		""" Method to set the parameter set to be updated
			in the MCMC algorithm.
		"""
		return self.sampler.define_parameters()

	def initial_value(self,parameter_name):
		""" Method that sets the initial value of the
			parameters to be estimated.

		:param parameter_name: name of the parameter.
		:type parameter_name: str
		:return: initial value of the parameter
		:rtype: `Numpy.dnarray`
        """
		return self.sampler.initial_value(parameter_name)

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
		return self.sampler.distribution_parameters(parameter_name) # returns a dictionary

	def generate(self, parameter_name):
		""" This method handles the generation of the random draws of
			the Markov chain for each parameters.

		:param parameter_name: name of the parameter of interest
		:type parameter_name: string
		:return: random draw from the posterior probability distribution
		:rtype: `Numpy.dnarray`
        """
		return self.sampler.generate(parameter_name)

	def output(self, burn, parameter_name):
		""" Computes the poserior mean of the parameters.

		:param parameter_name: name of the parameter of interest
		:type parameter_name: string
		:param burn: number of draws dismissed as burning samples
		:type burn: int
		:return: output of the MCMC algorithm
		:rtype: `Numpy.dnarray`
        """
		return self.sampler.output(self.simulations, burn, parameter_name)

	def run(self, number_simulations, max_restart, verbose):
		""" Runs the MCMC algorithm.

		:param number_simulations: number of random draws for each parameter.
		:type number_simulations: int
		:param max_restart: number of times the MCMC routine is allowed to restart.
		:type max_restart: int
		:param verbose: control console log information detail.
		:type verbose: int
		"""
		self.simulations = {key : zeros((param.size[0],param.size[1],number_simulations)) for (key, param) in self.sampler.parameters.list.items()}

		for name in self.sampler.parameters.hierarchy:
			self.sampler.parameters.list[name].current_value = self.initial_value(name)

		for i in range(number_simulations):
			if verbose > 0
				print("== step %i ==" % (int(i+1),))
			restart = 0
			restart_step = True
			while restart_step:
				for name in self.sampler.parameters.hierarchy:
					if verbose > 3
					print("== parameter %s ==" % name)
					try:
						self.sampler.parameters.list[name].current_value = self.generate(name)
						self.simulations[name][:,:,i] = self.sampler.parameters.list[name].current_value.reshape(self.sampler.parameters.list[name].size)
						restart_step = False
						restart = 0
					except:
						if restart < max_restart:
							restart+=1
							if verbose > 4
								print("== restart step %i ==" % i)
							restart_step = True
							break
						else:
							raise ValueError("Convergence error")
