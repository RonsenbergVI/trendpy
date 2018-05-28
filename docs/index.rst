=======
trendpy
=======

.. module:: trendpy

**trendpy** is a bayesian filtering micro library.

The library also supports bayesian regression models (Lasso and Ridge).

Models are fitted using MCMC algorithms.


User's Guide
============

Requirements
------------

trendpy is build on top of the following libraries:

* `Numpy` (http://www.numpy.org)
* `SciPy` (http://www.scipy.org)
* `Pandas` (http://pandas.pydata.org/)
* `matplotlib` (http://http://matplotlib.org/)
* `statsmodels` (http://www.statsmodels.org/stable/index.html)


Issues
------

Should you encounter any issue with the library you can raise them here: https://github.com/ronsenbergVI/trendpypy/issues

.. include:: ../INSTALL.rst

Introduction to filtering theory
--------------------------------

Consider :math:`(y_t)_{t \in [0,T]}` the (continuous), normalized price process of a stock, verifying the decomposition:

.. math::



where :math:`x` is the price trend and :math:`\epsilon` a stochastic noise.
The process of trend filtering consists in recovering :math:`x` from the
observations of :math:`y`. Under regularity conditions, the first derivative of
:math:`x` indicates up or down price trends:

.. math::

   \mu_t = \dfrac{dx_t}{dt}

The trend filtering equation becomes:

.. math::

	dy_t = \mu_tdt + d\epsilon_t

A common assumption on the dynamic of the noise is:

.. math::

	d\epsilon_t = \sigma_t dW_t

with :math:`\sigma>0` and :math:`W` a standard Brownian motion.
From a theoretical point of view trend filtering is equivalent
to finding the functional form:

.. math::

	x_t = \textbf{f}(t,y)

Quickstart
----------

To create a new :py:meth:`~trendpy.series.Series` instance from a csv file::

	>>> from trendpy.series import Series
	>>> data = Series.from_csv('data.csv')
	>>> data.plot()

API Reference
=============

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.


Factory
-------

Factory class handling the creation of bayesian algorithms.

.. module:: trendpy.factory

.. autoclass:: SamplerFactory

	.. automethod:: add

	.. automethod:: removee

	.. automethod:: remove_All

	.. automethod:: create

Mcmc
----

Generic structure of the algorithms implemented.

.. module:: trendpy.mcmc

.. autoclass:: MCMC

	.. attribute:: sampler

	  implementation of the MCMC algorithm

	.. attribute:: simulations

	  dictionary containing the history of simulations (is None if
	  the MCMC algorithm has not been ran yet)

	.. automethod:: define_parameters

	.. automethod:: initial_value

	.. automethod:: distribution_parameters

	.. automethod:: generate

	.. automethod:: output

	.. automethod:: run


Samplers
--------

Samplers tell the mcmc algorithm how to simulate the Markov chain.

.. module:: trendpy.samplers

.. autoclass:: Parameter

	.. attribute:: distribution

	   Subclass of the Scipy rv_continuous class.

	.. attribute:: size

	   Dimensions of the parameter.

	.. attribute:: name

 	   Name of the parameter.

	.. automethod:: __init__

	.. automethod:: is_multivariate

.. autoclass:: Parameters

	.. attribute:: list

	   A dictionary with the parameters to estimate.

	.. attribute:: hierarchy

	   List containing the order in which
	   the Gibbs sampler updates the
	   parameter values.

	.. automethod:: __init__

	.. automethod:: append

.. autoclass:: Sampler

	.. attribute:: parameters

	   Parameters to be estimated in the MCMC algorithm.

	.. attribute:: data

	  array with the price time series

	.. automethod:: define_parameters

	.. automethod:: initial_value

	.. automethod:: distribution_parameters

	.. automethod:: generate

	.. automethod:: output

Trendpy Changelog
=================

We detail here the changes made to the library

.. include:: ../CHANGES


License
=======

trendpy is licensed under the MIT Licence. It means that the source
code provided in the binaries can be used, modified, or distributed
freely for commercial or personal use with conditions only requiring
preservation of copyright and license notices.

The full license text can be found below (:ref:`trendpy-license`).

Authors
-------

.. include:: ../AUTHORS

Contributing
------------

Contribution will be welcomed once a first stable release is ready.

License Definitions
-------------------

The following section contains the full license texts for trendpy and the
documentation.

-   "AUTHORS" hereby refers to all the authors listed in the
    :ref:`authors` section.

-   The ":ref:`trendpy-license`" applies to all the source code shipped as
    part of trendpy (trendpy itself as well as the examples and the unittests)
    as well as documentation.

trendpy License
---------------

.. include:: ../LICENSE
