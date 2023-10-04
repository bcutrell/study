import datetime
import backtrader as bt

class BuyAndHoldTarget(bt.Strategy):
    def start(self):
        self.val_start = self.broker.get_cash()  # keep the starting cash

    def nextstart(self):
        # Buy all the available cash
        size = int(self.broker.get_cash() / self.data)
        self.buy(size=size)
        self._private = 10

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('ROI:        {:.2f}%'.format(100.0 * self.roi))

    def notify_timer(self, timer, when, *args, **kwargs):
        # Add the influx of monthly cash to the broker
        print(notify_timer)
        self.broker.add_cash(10)

        # buy available cash
        target_value = self.broker.get_value() + self.p.monthly_cash
        self.order_target_value(target=target_value)

def main():
    cerebro = bt.Cerebro()
    data = bt.feeds.BacktraderCSVData(dataname="../data/data.txt")
    cerebro.adddata(data)
    cerebro.addstrategy(BuyAndHoldTarget)
    cerebro.broker = bt.brokers.BackBroker()
    cerebro.addsizer(bt.sizers.FixedSize)
    cerebro.run()

    cerebro.plot()

if __name__ == "__main__":
    main()
