# trendpy
trend filtering micro library
## Repository Content


## Documentation

The documentation can be found [here]().

## Contributing

Contribution will be welcomed once a first stable release is ready. [Contact me]()

### Import data

Data is imported from a file (trendpy only supports csv for now).

```markdown

# import data from csv file (with dates and price) -- for now trendpy only
# support 1D time series

  filename='snp500.csv'
  data = TimeSeries.from_csv(filename)
# plots time series
  data.plot()

```

### Trend filtering

There are 4 trend filters possible

* L2 (or Hodrick-Prescott) filter
* L1 filter
* L1-T filter
* L1-C filter

and two possible optimisation methods:

* interior-point
* MCMC

```markdown

# trend filter with selected filter

  data.filter('hp_filter',optimisation=true)
  data.plot(trend=true)

```

# Requirements

These requirements reflect the testing environment.  It is possible
that trendpy will work with older versions.

* Python (2.7.11+)
* NumPy (1.12+)
* SciPy (0.13+)
* Pandas (0.19+)
* seaborn (0.7.1+)

# Sources

Research papers that helped develop this library

* Locally adaptative regression splines (1997) - Mammen, van der Geer
* Asymptotic equivalence of non-parametric regression and white noise (1996) - Brown, Lo
* Postwar US business cycles: an empirical investigation (1997) - Hodrick Prescott
* Regression Shrinkage and Selection via the Lasso - (1996) Tibshirani
* Lasso Regression: Estimation and Shrinkage via Limit of Gibbs Sampling - (2015) Rayaratnam et al.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
