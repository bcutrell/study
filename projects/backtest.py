from datetime import datetime
import argparse

import yfinance as yf
import backtrader as bt
import vectorbt as vbt



#
# Vectorbt
#
def vectorbt_example():
    # Download daily close data for Apple stock
    data = vbt.YFData.download('AAPL', interval='1d')

    # Calculate the 10-day and 50-day moving averages
    ma_fast = vbt.MA.run(data.data['AAPL']['Close'], 10)
    ma_slow = vbt.MA.run(data.data['AAPL']['Close'], 50)

    # Generate buy and sell signals based on the moving average crossover
    entries = ma_fast.ma_crossed_above(ma_slow)
    exits = ma_fast.ma_crossed_below(ma_slow)

    # Create a portfolio object and run the backtest
    portfolio = vbt.Portfolio.from_signals(data.data['AAPL']['Close'], entries, exits, freq='d')
    print(portfolio.total_profit())

#
# Backtrader
#
class BuyAndHoldTarget(bt.Strategy):

    def start(self):
        """ set the starting cash """
        self.val_start = self.broker.get_cash()  # keep the starting cash

    def log(self, txt, dt=None):
        """ Logging function for this strategy """
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def nextstart(self):
        """ called exactly once for each data, after the ``next`` is called for the 1st time """
        # Buy all the available cash
        size = int(self.broker.get_cash() / self.data)
        self.buy(size=size)

    def next(self):
        """ called every period """
        # log the closing price of the series from the reference
        if self.data.tick_last:
            self.log('Tick Last, %.2f' % self.data.tick_last)

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('ROI:        {:.2f}%'.format(100.0 * self.roi))

    def notify_timer(self, timer, when, *args, **kwargs):
        # Add the influx of monthly cash to the broker
        self.broker.add_cash(10)

        # buy available cash
        target_value = self.broker.get_value() + self.p.monthly_cash
        self.order_target_value(target=target_value)

def backtrader_example():
    cerebro = bt.Cerebro()

    # Add data from a file
    # data = bt.feeds.BacktraderCSVData(dataname="../data/data.txt")
    # cerebro.adddata(data)

    # Add a data feed for AAPL
    aapl_data = bt.feeds.PandasData(dataname=yf.download('AAPL', '2022-01-01', '2023-01-01'))
    cerebro.adddata(aapl_data)

    # Add a data feed for MSFT
    msft_data = bt.feeds.PandasData(dataname=yf.download('MSFT', '2022-01-01', '2023-01-01'))
    cerebro.adddata(msft_data)

    cerebro.addstrategy(BuyAndHoldTarget)
    cerebro.broker = bt.brokers.BackBroker()
    cerebro.addsizer(bt.sizers.FixedSize)
    cerebro.run()
    # cerebro.plot()

def main():
    backtrader_example()
    vectorbt_example()

if __name__ == "__main__":
    main()
