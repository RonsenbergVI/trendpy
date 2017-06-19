.. _api:

API
---

.. module:: trendpy

This part of the documentation covers all the interfaces of trendpy. Whenever an external library is used
the most relevent part are documented and we provide links to the respective documentations.


factory
-------

Factory class handling the creation of bayesian algorithms.

.. autoclass:: StrategyFactory
    :members:

    .. automethod:: add
	
	.. automethod:: create


globals
-------

A collection of functions used to perform estimations.

.. autofunction:: derivative_matrix

mcmc
----

.. autoclass:: MCMC
    :members:

    .. automethod:: __init__

series
------

.. autoclass:: Series
    :members:

    .. automethod:: __init__

strategies
----------

Strategies tell the mcmc algorithm how to simulate the Markov chain. 

.. autoclass:: Parameter
    :members:

    .. automethod:: __init__


.. autoclass:: Parameters
    :members:

    .. automethod:: __init__


.. autoclass:: Strategy
    :members:

    .. automethod:: __init__


.. autoclass:: L1Filter
    :members:

    .. automethod:: __init__
