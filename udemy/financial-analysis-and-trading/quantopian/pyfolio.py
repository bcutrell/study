
import pyfolio as pf
import matplotlib.pyplot as plt
import empyrical

# ALGO RETURNS
bt = get_backtest('hash')
bt_returns = bt.daily_performance['returns']
bt_positions = bt.pyfolio_positions
bt_transasctions = bt.pyfolio_transactions

# BENCHMARK RETURNS
bm = get_backtest('hash')
bm_returns = bm.daily_performance['returns']
bm_positions = bm.pyfolio_positions
bm_transasctions = bm.pyfolio_transactions


empyrical.sharpe_ratio(bt_returns)
empyrical.sharpe_ratio(bm_returns)
empyrical.beta(bt_returns,bm_returns)

# Pyfolio Ploting
pf.plotting.plot_rolling_returns(bt_returns, bm_returns)
pf.plotting.plot_rolling_beta(bt_returns, bm_returns)
pf.plotting.plot_rolling_sharpe(bt_returns, bm_returns)
pf.plotting.plot_drawdown(bt_returns, bm_returns)
pf.plotting.plot_drawdown_underwater(bt_returns, bm_returns)
pf.plotting.create_round_trip_tear_sheet(bt_returns, bt_positions, bt_transactions)



