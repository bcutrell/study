from quantopian.pipline import Pipeline
from quantopian.research import run_pipeline
from quantopian.pipeline.data.builtin import USEquityPricing

from quantopian.pipline.filters import Q1500US

universe = Q1500US()

from quantopian.pipeline.data import morningstar

sector = morningstar.asset_classification.morningstar_sector_code.lastest

# filters
energy_sector = sector.eq(309)

from quantopian.pipeline.factors import SimpleMovingAverage, AverageDollarVolume

dollar_volume = AverageDollarVolume(window_length=30) # for the past 30 days

# highly trades stocks
high_dollar_volume = dollar_volume.percentile_between(90, 100) # .bottom() .top()

top_open_prices = USEquityPricing.open.latest.top(50, mask=high_dollar_volume)
high_close_price = USEquityPricing.close.latest.percentile_between(90, 100, mask=top_open_prices)

# Trading Algo
# Issue @ line41, minute ~18:30)

from quantopian.algorithm import attach_pipeline, pipeline_output

def initialize(context):

  schedule_function(my_rebalance, date_rules.week_start(), time_rules.market_open(hours=1))
  my_pipe = make_pipeline()
  attach_pipeline(my_pipe, 'my_pipeline')

def my_rebalance(context, data):
  for security in context.portfolio.positions:
    if security not in context.longs and security not in context.shorts and data.can_trade(security):
      # exit security
      order_target_percent(security, 0)

  for security in context.longs:
    if data.can_trade(security):
      order_target_percent(security, context.long_weight)

  for security in context.shorts:
    if data.can_trade(security):
      order_target_percent(security, context.short_weight)


def my_compute_weights(context):
  if len(context.longs) == 0:
    long_weight = 0
  else:
    long_weight = 0.5 / len(context.longs)

  if len(context.shorts) == 0:
    short_weight = 0
  else:
    short_weights = -0.5 / len(context.shorts)

  return (long_weight, short_weight)

def before_trading_start(context, data):
  context.output = pipeline_output('my_pipeline')

  # LONG
  context.longs = context.output[context.output['longs']].index.tolist()

  # SHORT
  context.longs = context.output[context.output['shorts']].index.tolist()

  context.long_weight, context.short_weight = my_compute_weights(context)



def make_pipeline():

  # Universe Q1500US
  base_universe = Q1500US()

  # Energy Sector
  energy_sector = sector.eq(309)

  # Make Mask of 1500US and Energy
  base_energy = base_universe & energy_sector
  
  # Dollar Volume (30 days) Grab the Info
  dollar_volume = AverageDollarVolume(window_length=30)

  # Grab the top 5% in avg dollar volume
  high_dollar_volume = dollar_volume.percentile_between(95, 100)

  # Combine the filters
  top_five_base_energy = base_energy & high_dollar_volume

  # 10 day mean close
  mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=top_five_base_energy)

  # 30 day mean close
  mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=top_five_base_energy)
  
  # Percent Difference
  percent_diff = (mean_close_10 - mean_close_30)/mean_close_30

  # list of shorts
  shorts = percent_diff < 0

  # list of longs
  shorts = percent_diff > 0

  # final mask/filter for anything in shorts or longs
  securities_to_trade = (shorts | longs)

  # return pipeline
  return Pipeline(columns={ 'longs': longs, 'shorts': shorts, 'perc_diff': percent_diff }, screen=securities_to_trade)

result = run_pipeline(make_pipeline(), '2015-05-05', '2015-05-05')
result.head()

