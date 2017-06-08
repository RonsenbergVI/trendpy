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

from numpy import uint64

__all__ = ['Parameter','Parameters','MCMC']

class Parameter(object):
    # """
    # MCMC Parameters object
    #
    # Attributes
    # ----------
    # name : string
    #     name of the parameter
    # distribution : rv_continuous (scipy object)
    #     posterior distribution of the parameter
    # current_value : numpy array (possibly a number)
    #     last value generated for the parameter
    # """"

    def __init__(self, name=None, distribution=None, current_value=None):
        self.name = str(name)
        self.distribution = distribution
        self.current_value = current_value

    def __str__(self):
        return """
            parameter name : %s
            parameter distribution : %s
        """ % (self.name, self.distribution.__str__())

    def __len__(self):
        return

class Parameters(object):
    # """
    # Collection of MCMC Parameters
    #
    # Methods
    # -------
    # append
    #     adds a new parameter to the parameter collection
    #
    # Attributes
    # ----------
    # params: dictionary
    #     dictionary with the parameter name as key and the parameter instance as value
    # """"

    def __init__(self, parameters=None, hierarchy=None):
        self.parameters = parameters
        self.hierarchy = hierarchy

    @property
    def parameters(self):
        return self.___parameters

    @parameters.setter
    def parameters(self, parameters):
        if not (parameters==None):
            self.__parameters = parameters
        else:
            self.__parameters = {}

    @property
    def hierarchy(self):
        return self.__hierarchy

    @hierarchy.setter
    def hierarchy(self, hierarchy):
        self.__hierarchy = hierarchy

    def __len__(self):
        return uint64(len(params))

    def __str__(self):
        return """
            number of parameters : %d
            list : %s
        """ % (len(self), self.parameters.__str__())

    def append(self, parameter):
        # """
        # Adds a new parameter to the parameter set
        # """
        self.parameters[parameter.name] = parameter
        self.hierarchy.append(parameter.name)


class MCMC(object):
    # """
    # MCMC Abstract class: any MCMC filtering method is a subclass of this class
    #
    # Methods
    # -------
    # distribution_parameters :
    #
    #
    # summary :
    #
    #
    # generate :
    #
    #
    # run :
    #     runs the MCMC procedure
    #
    # Attributes
    # ----------
    # data :
    #
    #
    # parameters :
    #
    #
    # simulations :
    #
    #
    # """

    def __init__(self, data=None, parameters=None):
        """
        """
        self.data = data
        self.parameters = parameters
        self.simulations = {}

    def summary(self):
        """
        MCMC method summary
        """
        raise NotImplementedError("Must be overriden")

    def distribution_parameters(self, parameter_name=None, *args, **kwargs):
        raise NotImplementedError("Must be overriden")

    def generate(self, parameter_name=None):
        """
        """
        distribution = self.parameters[parameter_name].distribution
        parameters = self.distribution_parameters(parameter_name)
        return distribution.rvs(parameters[0],parameters[1])

    def run(self, run=50, number_simulations=100):
        """
        """
        n = {key : 1 for key in self.parameters.keys()}
        values = {key:value.current_value for (key, value) in self.parameters.items()}
        self.simulations = {key : zeros((param.shape[0], param.shape[1]*number_simulations)) for (key, param) in self.parameters.items()}

        for i in range(number_simulations):
            for name in hierarchy:
                values[name] = generate(name, values)
                histo[name][:,i*value.current_value.shape[1]:(i+1)*value.current_value.shape[1]] = values[name]
                n[name] = n[name]+1

#class MCMCL1(MCMC):

#class MCMCL2(MCMC):
