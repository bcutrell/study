import numpy as np
from statsmodel import regression
import statsmodels.api as sm
import matplotlib.pyplot as plt

start = '2016-01-01'
end = '2017-01-01'

asset = get_pricing('AAPL', fields='price', start_date=start, end_date=end)
benchmark = get_pricing('SPY', fields='price', start_date=start, end_date=end)

asset_ret = asset.pct_change(1)[1:]
bench_ret = benchmark.pct_change(1)[1:]

# Plot
asset_ret.plot()
bench_ret.plot()
plt.legend()

plt.scatter(bench_ret, asset_ret, alpha=0.6, s=50)
plot.xlabel('SPY Ret')
plot.ylabel('AAPL Ret')

# Isolate Alpha behavior
AAPL = asset_ret.values
spy  = bench_ret.values

spy_constant = sm.add_constant(spy)
model = regression.linear_model.OLS(AAPL, spy_constant).fit()

model.params
alpha, beta = model.params


min_spy = bench_ret.values.min()
max_spy = bench_ret.values.max()

spy_line = np.linspace(min_spy, max_spy, 100)
y =spy_line*beta + alpha

plt.plot(spy_line, y, 'r')
plt.scatter(bench_ret, asset_ret, alpha=0.6, s=50)
plot.xlabel('SPY Ret')
plot.ylabel('AAPL Ret')

# Sacrificing gains for volatillity
hedged = -1*(beta*bench_ret) + asset_ret

hedged.plot(label='AAPL with Hedge')
asset_ret.plot(alpha=0.5)
bench_ret.plot(alpha=0.5)
plt.xlim(['2016-06-01', '2016-08-01'])
plt.legend()

# PART II
def alpha_beta(benchmark_ret, stock):
  benchmark = sm.add_constant(benchmark_ret)

  model = regression.linear_model.OLS(stock,benchmark).fit()

  return model.params[0], model.params[1]



start = '2016-01-01'
end = '2017-01-01'

asset2016 = get_pricing('AAPL', fields='price', start_date=start, end_date=end)
benchmark2016 = get_pricing('SPY', fields='price', start_date=start, end_date=end)

asset_ret2016 = asset2016.pct_change(1)[1:]
benchmark_ret2016 = benchmark2016.pct_change(1)[1:]

aret_values = asset_ret2016.values
bret_values = benchmark_ret2016.values

alpha2016, beta2016 - alha_beta(bret_values, aret_values)

print('2016 Values')
print('alpha ' +str(alpha2016))
print('beta ' +str(beta2016))

portfolio = -1*beta2016*benchmark_ret2016 + asset_ret2016

alpha, beta = alpha_beta(benchmark_ret2016, portoflio)
print('PORTFOLIO ALPHA AND BETA')
print('alpha ' +str(alpha))
print('beta ' +str(beta))

portfolio.plot(alpha=0.9, label='AAPL with HEDGE')
asset_ret2016.plot(alpha=0.5)
benchmark_ret2016(alpha=0.5)
plt.ylabel('DAILY RETURN')
plt.legend()

# reduced daily returns
# imporved volatility
portfolio.mean() 
asset_ret2016.mean()

portfolio.std()
asset_ret2016.std

# Another options -> Use beta from prior year
portfolio = -1*beta2016*benchmark_ret2017 + asset_ret2017
alpha, beta = alpha_beta(benchmark_ret2016, portoflio)
