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

from enum import enum

class OptionsType(Enum):
    hp_filter="hp_filter"
    l1_filter="l1_filter"
    l1_c_filter="l1_c_filter"
    l2_c_filter="l2_c_filter"

class Options(object):

    def __init__(self,*args):
        self.norm=args[0]
        self.total_variation=args[1]
        self.parameters=args[2]

class OptionsFactory(object):

    @staticmethod
    def hp_filter():
        return Options(2,2,None)

    @staticmethod
    def l1_filter():
        return Options(1,1,{'xtol':1e-8,'disp':True})

    @staticmethod
    def l1_c_filter():
        return Options(2,1,{'xtol':1e-8,'disp':True})

    @staticmethod
    def l2_c_filter():
        return Options(1,2,None)
