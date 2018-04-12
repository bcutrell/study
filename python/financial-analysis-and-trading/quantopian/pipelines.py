
'''
Pipelines
  compute some scalar value for all assets
  filter assets based off that scalar value
  set desired portfolio weights of filtered assets
  place orders on assets to reflect desired portfolio weights
'''

# Classifier - function that transforms input and timestamp to a categorical output ( AAPL -> Tech Sector )
# Factor - takes in asset + timestamp and returns numerical output

from quantopian.pipline import Pipeline

def make_pipeline():
  return Pipeline()

pipe = make_pipeline()

from quantopian.research import run_pipeline

# without a filter, all securities will be returned
result = run_pipeline(pipe, '2017-01-03', '2017-01-03')

from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import SipmpleMovingAverage


def make_pipeline():
  mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
  return Pipeline(columns={'30 Day Mean Close': mean_close_30})

result = run_pipeline(make_pipeline(), '2017-01-03', '2017-01-03')
results.head()


def make_pipeline():
  mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
  mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
  latest_close = USEquityPricing.close.latest

  percent_diff = (mean_close_10 - mean_close_30)/mean_close_30
  return Pipeline(columns={'30 Day Mean Close': mean_close_30,
                           'Percent Diff': percent_diff,
                           'Latest Close': latest_close})

result = run_pipeline(make_pipeline(), '2017-01-03', '2017-01-03')
results.head()

# FILTERS AND SCREENS
# take in asset and timestamp and return boolean

def make_pipeline():
  mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
  mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
  latest_close = USEquityPricing.close.latest

  percent_diff = (mean_close_10 - mean_close_30)/mean_close_30

  percent_filter = percent_difference > 0
  small_price = latest_close < 5

  # COMBINE FILTERS
  final_filter = perc_filter & small_price

  # Add ~ to reverse screen ~percent_filter
  return Pipeline(columns={'30 Day Mean Close': mean_close_30,
                           'Percent Diff': percent_diff,
                           'Latest Close': latest_close,
                           'Percent Filter': percent_filter
                           }, screen=final_filter)

result = run_pipeline(make_pipeline(), '2017-01-03', '2017-01-03')
results.head()

# MASKING AND CLASSIFIERS
# masking - allows us to ignore assets all together, before the factors or filters even run
def make_pipeline():
  latest_close = USEquityPricing.close.latest
  small_price = latest_close < 5

  mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=small_price)
  mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=small_price)

  percent_diff = (mean_close_10 - mean_close_30)/mean_close_30
  percent_filter = percent_difference > 0

  # COMBINE FILTERS
  final_filter = perc_filter & small_price

  # Add ~ to reverse screen ~percent_filter
  return Pipeline(columns={'30 Day Mean Close': mean_close_30,
                           'Percent Diff': percent_diff,
                           'Latest Close': latest_close,
                           'Percent Filter': percent_filter
                           }, screen=final_filter)

from quantopian.pipeline.data import morningstar
from quantopian.pipeline.classifiers.morningstar import Sector

morningstar_sector = Sector()
exchange = morningstar_sector.share_class_reference.exchange_id.latest
exchange

def make_pipeline():
  latest_close = USEquityPricing.close.latest
  small_price = latest_close < 5

  # CLASSIFIER
  nyse_filter = exchange.eq('NYS')

  mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=small_price)
  mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=small_price)

  percent_diff = (mean_close_10 - mean_close_30)/mean_close_30
  percent_filter = percent_difference > 0

  # COMBINE FILTERS
  final_filter = perc_filter & nyse_filter

  # Add ~ to reverse screen ~percent_filter
  return Pipeline(columns={'30 Day Mean Close': mean_close_30,
                           'Percent Diff': percent_diff,
                           'Latest Close': latest_close,
                           'Percent Filter': percent_filter
                           }, screen=final_filter)


result = run_pipeline(make_pipeline(), '2017-01-03', '2017-01-03')
results.info()




