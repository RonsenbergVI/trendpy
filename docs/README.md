### Import data

Data is imported from a file (trendpy only supports csv for now).

```markdown

# import data from csv file (with dates and price) -- for now trendpy only
# support 1D time series

from trendpy.timeseries import TimeSeries

filename='data.csv'
fund=TimeSeries.from_csv('data.csv')

# plots time series
fund.plot()

```

### Trend filtering

There are 3 trend filters possible

* L1 filter
* L2 filter (or Hodrick-Prescott filter)
* Lp filter with 0<=p<=2

Custom filters with more options to come in first stable release.

```markdown

# trend filter with selected filter

fund.filter(number_simulations=30, burns=10)
fund.plot()

```

