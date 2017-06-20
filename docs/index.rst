=======
trendpy
=======

.. module:: trendpy

**trendpy** is a bayesian filtering micro library.

The library also supports bayesian regression models (Lasso and Ridge).

Models are fitted using MCMC algorithms.


User's Guide
============

.. toctree::
   :maxdepth: 2

Requirements
------------

trenpy is build on top of the following libraries:

* `Numpy` (http://www.numpy.org)
* `SciPy` (http://www.scipy.org)
* `Pandas` (http://pandas.pydata.org/)
* `matplotlib` (http://http://matplotlib.org/)
* `statsmodels` (http://www.statsmodels.org/stable/index.html)

and for testing I chose py.test (http://pytest.org/latest/)

Issues
------

Should you encounter any issue with the library ou can raise them here: https://github.com/ronsenbergVI/filterpy/issues

Installing trendpy
------------------

Installation with pip (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The library is available on pypi and to install the last available version, run this command:

.. code-block:: bash

    $ pip install trendpy

To test the installation:

    >>> import trendpy
    >>> trendpy.__version__

this should display the version installed on your system.

Installation from GitHub
^^^^^^^^^^^^^^^^^^^^^^^^

trendpy releases are also available on github (https://github.com/ronsenbergVI/trendpy). 
You first need to clone (or fork if you want to modify it) and 

.. code-block:: bash

		$ git clone https://github.com/ronsenbergVI/trendpy.git
		$ cd trendpy
		$ python setup.py build
		$ python setup.py install 


Introduction to filtering theory
--------------------------------

Consider :math:`(y_t)_{t \in [0,T]}` the (continuous), normalized price process of a stock, verifying the decomposition:
	
.. math::

   \forall t \in [0,T], \quad y_t = x_t + \epsilon_t

where :math:`x` is the price trend and :math:`\epsilon` a stochastic noise.
The process of trend filtering consists in recovering :math:`x` from the 
observations of :math:`y`. Under regularity conditions, the first derivative of 
:math:`x` indicates up or down price trends:

.. math::

   \mu_t = \dfrac{x_t}{dt}

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

To create a new series from a csv file:: 

	from trendpy.series import Series
	data = Series.from_csv('data.csv')
	data.plot()


Adding new algorithms
---------------------

The MCMC class containts thegeneric structure of any MCMC algorithm:

* `definition of the parameters (posterior distribution, dimensions)`
* `initialisation of the parameters to be estimated`
* `random simulation of the parameters from their respective posterior distributions`

Thus any new algorithm can be added to the library by subclassing the **Strategy** class::

	class BlackScholes(Strategy):
		
		def __init__():
			pass


Then the new MCMC instance just needs to be initialized with the new strategy and ran::

	new_mcmc = MCMC(self, StrategyFactory.create("BlackScholes",data))

	mcmc.run(number_simulations=50)
	
	estimation = mcmc.output()


API Reference
=============

.. toctree::
   :maxdepth: 2

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

API
---

factory
^^^^^^^
Factory class handling the creation of bayesian algorithms.

globals
^^^^^^^

A collection of functions used to perform estimations.

mcmc
^^^^
Generic structure of the algorithms implemented.

series
^^^^^^

Class implementing time series analysis.

strategies
^^^^^^^^^^

Strategies tell the mcmc algorithm how to simulate the Markov chain.

.. module:: trendpy.strategies

.. autoclass:: Parameter

	.. attribute:: trendpy.distribution
	
	   Subclass of the Scipy rv_continuous class. 

	.. attribute:: trendpy.size
	
	   Dimensions of the parameter. 

	.. attribute:: name
	
 	   Name of the parameter. 

	.. automethod:: __init__

	.. automethod:: is_multivariate

Additional Notes
================

.. toctree::
   :maxdepth: 2

Additional notes for anyone interested.

Trendpy Changelog
-----------------

We detail here the changes made to the library

.. include:: ../CHANGES

License
-------

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
