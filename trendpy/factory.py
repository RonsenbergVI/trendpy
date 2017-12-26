# -*- coding: utf-8 -*-

# factory.py

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

from trendpy.samplers import *

class SamplerFactory:
	factories = {}

	@staticmethod
	def add(id,factory):
		""" Adds a class to factory with a chosen id.

		:param id: name of the class.
		:type id: str
		:param factory: factory subclass of a Strategy instace.
		:type factory: `Strategy.Factory`
		"""
		SamplerFactory.factories[id] = factory

	@staticmethod
	def remove(id):
		""" Removes a class to factory with a chosen id.

		:param id: name of the class.
		:type id: str
		"""
		if id in SamplerFactory.factories:
			del SamplerFactory.factories[id]

	@staticmethod
	def removeAll():
		""" Removes all factories."""
		if not(SamplerFactory.factories == None or SamplerFactory.factories == {}):
			SamplerFactory.factories.clear()

	@staticmethod
	def create(id,*args,**kwargs):
		""" Creates an instance of the class.

		:param id: name of the class.
		:type id: str
		:param args: Positional arguments.
		:type args: list
		:param kwargs: Keyword arguments.
		:type kwargs: dict
		:return: new instance of a :py:meth:`~trendpy.strategies.Strategy` subclass
		:rtype: `Numpy.dnarray`
		"""
		if not id in SamplerFactory.factories:
			SamplerFactory.factories[id] = eval('%s.Factory()' % id)
		return SamplerFactory.factories[id].create(*args,**kwargs)
