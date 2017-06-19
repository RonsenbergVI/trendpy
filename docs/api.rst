.. _api:

API
---

This part of the documentation covers all the interfaces of trendpy. Whenever an external library is used
the most relevent part are documented and we provide links to the respective documentations.


factory
^^^^^^^
.. toctree::
   :maxdepth: 2

Factory class handling the creation of bayesian algorithms.

.. module:: trendpy.factory

.. autoclass:: StrategyFactory
    :members:

    .. automethod:: add

    .. automethod:: create


globals
^^^^^^^
.. toctree::
   :maxdepth: 2

A collection of functions used to perform estimations.

.. autofunction:: derivative_matrix

mcmc
^^^^
.. toctree::
   :maxdepth: 2

.. module:: trendpy.mcmc

.. autoclass:: MCMC
    :members:

    .. automethod:: __init__

series
^^^^^^
.. toctree::
   :maxdepth: 2


.. module:: trendpy.series

.. autoclass:: Series
    :members:

    .. automethod:: __init__

strategies
^^^^^^^^^^
.. toctree::
   :maxdepth: 2

Strategies tell the mcmc algorithm how to simulate the Markov chain.

.. module:: trendpy.strategies

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
