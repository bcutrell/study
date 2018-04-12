from quantopian.algorithm import attached_pipeline, pipeline_output

from quantopian.pipeline import Pipeline
from quantopian.pipeline.factors import AverageDollarVolume
from quantopian.pipeline.data.accern import aphaone_free


def initialize(context):
  schedule_function(my_rebalance, date_rules.every_day())
  attach_pipeline(make_pipeline(), 'pipeline')

def before_trading_start(context,data):
  port = pipeline_output('pipeline')

  context.longs = port[(port['impact'] == 100) & (port['sentiment'] > 0.5)].index.tolist()
  context.shorts = port[(port['impact'] == 100) & (port['sentiment'] < -0.5)].index.tolist()

def my_compute_weights(context):
  context.long_weight = 0.5/len(context.longs)
  context.short_weight = 0.5/len(context.shorts)

def my_rebalance(context, data):
  for security in context.portfolio.positions:
    if security not in context.longs and security not in context.shorts and data.can_trade(security):
      order_target_percent(security, 0)

  for security in context.longs:
    if data.can_trade(security):
      order_target_percent(security, context.long_weight)

  for security in context.shorts:
    if data.can_trade(security):
      order_target_percent(security, context.short_weight)

def make_pipeline():

  dollar_volume = AverageDollarVolume(window_length=20)

  is_liquid = dollar_volume.top(1000)

  impact = alphaone_free.impact_score.latest
  sentiment = alphaone_free.article_sentiment.latest 


  return Pipeline(columns={
    'impact': impact,
    'sentiment': sentimenet }, screen=is_liquid)
