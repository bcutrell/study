'''
20 day rolling mean and 20 day rolling std dev

20 day mean +/- (2 * 20 day std dev)

Use bands and compare them to the current price as signal

Check Daily
  If above:
    short stock
  If below:
    long stock
'''

import numpy as np

def initialize(context):
    schedule_function(check_bands, date_rules.every_day(), time_rules.market_close(minutes=60))
    context.ally = sid(46015)
    
    context.long = False
    context.short = False

def check_bands(context, data):
    ally = context.ally
    prices = data.history(ally, 'price', 20, '1d')
    
    mavg_20 = np.mean(prices)
    std_20 = np.std(prices)
    
    upper = mavg_20 + 2*std_20
    lower = mavg_20 - 2*std_20
    
    current_price = data.current(ally, 'price')
    
    if current_price >= upper and not context.short:
        # above band
        order_target_percent(ally, -1.0)
        context.long = False
        context.short = True
        print('Short')
    elif current_price <= lower and not context.long:
        # below band
        order_target_percent(ally, 1.0)
        context.long = True
        context.short = False
        print('Long')
    else:
        # within band
        order_target_percent(ally, 0)
        context.long = False
        context.short = False
        print('Neutral')
    record(upper=upper, lower=lower, price=current_price)    
    
