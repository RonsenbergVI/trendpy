# trendpy (alpha)
Bayesian trend filtering micro library

I am currently redesigning the API and will release an alpha version in late August.

## Documentation

The documentation can be found [here](http://trendpy.readthedocs.io/en/latest/).

## Contributing

Contribution will be welcomed once a first stable release is ready. [Contact Me]()

### Import data

Data is imported from a file (trendpy only supports csv for now).

```markdown

# import data from csv file (with dates and price) -- for now trendpy only
# support 1D time series

from trendpy import filter
from pandas import read_csv

filename='data.csv'
data = read_csv(filename)

filtered = filter(data['time series'])

```

# Requirements

These requirements reflect the testing environment.  It is possible
that trendpy will work with older versions.

* Python (3+)
* NumPy (1.12+)
* SciPy (0.13+)
* Pandas (0.19+)
* matplotlib (2.0+)
* statsmodels (0.6+)

# Sources

Research papers that helped develop this library

* Locally adaptative regression splines (1997) - Mammen, van der Geer
* Asymptotic equivalence of non-parametric regression and white noise (1996) - Brown, Lo
* Postwar US business cycles: an empirical investigation (1997) - Hodrick Prescott
* Regression Shrinkage and Selection via the Lasso - (1996) Tibshirani
* Lasso Regression: Estimation and Shrinkage via Limit of Gibbs Sampling - (2015) Rayaratnam et al.
* Assessing Convergence of the Markov Chain Monte Carlo Method in Multivariate Case - (2005) Nogueira et al.

### Support or Contact

Having trouble with trendpy? Check out our [documentation](http://trendpy.readthedocs.io/en/latest/).
