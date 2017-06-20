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

Consider :math:`(y)_{t \in [0,T]}` the (continuous )


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

	new_mcmc = MCMC(self, StrategyFactory.create("BlackScholes",data,total_variation_order=2))

	mcmc.run(number_simulations=50)
	
	estimation = mcmc.output()


API Reference
=============

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

API
---

.. module:: trendpy

.. autoclass:: StrategyFactory
   :members: add, create

.. autoclass:: MCMC
	:members: define_parameters, initial_value, distribution_parameters, generate, output, run

.. autoclass:: Series
   :members: from_csv, returns, save, plot, filter

.. autoclass:: Message
   :members: attach, add_recipient
   
.. autoclass:: Parameter
   :members: __init__, is_multivariate
   
.. autoclass:: Parameters
   :members: append

.. autoclass:: Strategy
   :members: define_parameters, initial_value, distribution_parameters, generate, output



Additional Notes
================

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
