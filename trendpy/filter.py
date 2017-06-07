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

from trendpy.time_series import TimeSeries
from numpy.linalg import norm
from numpy import dot, ones, zeros
from scipy.optimize import minimize

class Filter(object):

    def __init__(self,time_series,eta,options):
        self.price=time_series
        self.y=self.price.data.as_matrix()
        self.eta=eta
        self.N=len(time_series)
        self.options=options
        self.D=self.get_derivative(option.total_variation)

    def get_trend(self,type):
        x0=ones(self.N)
        constraints= [{'type':'ineq','fun':self.pos_constraint},{'type':'ineq','fun':self.neg_constraint}]
        result=minimize(self.function,x0,args=(self.y,self.D),method='nelder-mead',options=self.options.parameters,contraints=constraints)
        print(res)
        return res

    def function(self,x,y,D):
        return 0.5*dot(x,dot(D,x.T))-dot(y,dot(D,x.T))

    def pos_constraint(self,x):
        return x-self.eta*ones(self.N)

    def neg_constraint(self,x):
        return self.eta*ones(self.N)-x

    def get_derivative(self,order):
        D=zeros((self.N-order,self.N))
        if order==1:
            a=1
            b=-1
            c=0
        elif order==2:
            a=1
            b=-2
            c=1
        for n in range(self.N-order):
            D[n,n]=a
            D[n,n+1]=b
            D[n,n+2]=c
        return D
