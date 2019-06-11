# Sharpe Ratios
#   Which portfolio is best?
#   measure for calculating risk adjusted returns
# S = ( Rp - Rf / STDp )

#   Rf - bank savings, tres bond, LIBOR

# SR = mean return / std
# annualized Sharpe Ratio can be obtained by multiplying against a K-Factor based off your Sampling Rate:
# Daily K=sqrt(252)
# Weekly K=sqrt(52)
# Yearly K=sqrt(12)
# ASR = K * SR

# Code Along
# Part I
import pandas as pd
import quandl

start = pd.to_datetime('2012-01-01')
end = pd.to_datetime('2017-01-01')

aapl = quandl.get('WIKI/AAPL.11',start_date=start, end_date=end)
cisco = quandl.get('WIKI/CSCO.11',start_date=start, end_date=end)
ibm = quandl.get('WIKI/IBM.11',start_date=start, end_date=end)
amzn = quandl.get('WIKI/AMZN.11',start_date=start, end_date=end)
aapl.iloc[0]['Adj. Close']

for stock_df in (aapl, cisco, ibm, amzn):
 stock_df['Normed Return'] = stock_df['Adj. Close'] / stock_df.iloc[0]['Adj. Close'] 

# 30% in aapl
# 20% in cisco
# 40% in amazon
# 10% in ibm

# zip is making a list of tuples
for stock_df, allo in zip((aapl, cisco, ibm, amzn), [.3,.2,.4,.1]):
  stock_df['Allocation'] = stock_df['Normed Return'] * allo


for stock_df, allo in (aapl, cisco, ibm, amzn):
  stock_df['Position Values'] = stock_df['Allocation'] * 1000000

all_pos_vals = [aapl['Position Values'], cisco['Position Values'],
                ibm['Position Values'], amzn['Position Values']]

portfolio_val = pd.concat(all_pos_vals, axis=1)

portfolio_val.columns = [ 'AAPL Pos', 'CISCO Pos', 'IBM Pos', 'AMZN Pos']
portfolio_val.head()
portfolio_val['Total Pos'] = portfolio_val.sum(axis=1)

import matplotlib.pyplot as plt

portfolio_val['Total Pos'].plot(figsize=(10,8))
portfolio_val.drop('Total Pos', axis=1).plot()

# Part II
portfolio_val['Daily Return'] = portfolio_val['Total Pos'].pct_change(1)
portfolio_val.head()
portfolio_val['Daily Return'].plot(kind='hist', bins=100)
portfolio_val['Daily Return'].plot(kind='kde')

cumlative_return =  100 * (portfolio_val['Total Pos'][-1]/portfolio_val['Total Pos'][0]) - 1

# Sharpe Ratio
SR = portfolio_val['Daily Return'].mean() / portfolio_val['Daily Return'].std()
ASR = (252 ** 0.5 ) * SR

# ASR > 1 is considered good
# ASR > very good
# ASR > 3 incredible

# Finding the Optimal Portfolio Allocation

# A couple methods to find optimal allocation:
# Monte Carlo
# Using a minimizer

aapl = quandl.get('WIKI/AAPL.11',start_date=start, end_date=end)
cisco = quandl.get('WIKI/CSCO.11',start_date=start, end_date=end)
ibm = quandl.get('WIKI/IBM.11',start_date=start, end_date=end)
amzn = quandl.get('WIKI/AMZN.11',start_date=start, end_date=end)

all_pos_vals = [aapl['Position Values'], cisco['Position Values'],
                ibm['Position Values'], amzn['Position Values']]
stocks = pd.concat([ aapl, cisco, ibm, amzn ])

stocks.colums = [ 'aapl', 'cisco', 'ibm', 'amzn' ]

# use close column
stocks.pct_change(1).mean()
stocks.pct_change(1).corr()

# use log returns instead of arithmetic returns to normalize data
log_ret = np.log(stocks / stocks.shift(1))

log_ret.hist(bins=100)
plt.tight_layout()
plt.show()

lot_ret.cov() * 252

np.random.seed(101)

weights = np.array(np.random.random(4))
print('Random Weights:')
print(weights)

print('Rebalance')
weights = weights/np.sum(weights)
print(weights)

# Expected Return
exp_ret = np.sum((log_ret.mean() * weights) * 252 )

# Expected Volatility
# use linear algebra to speed up calc
exp_vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))

SR = exp_ret / exp_vol
print(SR)


num_ports = 5000
all_weights = np.zeros((num_ports, len(stocks.columns)))
ret_arr = np.zeros(num_ports)
vol_arr = np.zeros(num_ports)
share_arr = np.zeros(num_ports)

for indx in rnage(num_ports):

  weights = np.array(np.random.random(4))
  weights = weights/np.sum(weights)
  all_weights[ind,:] = weights

  exp_ret = np.sum((log_ret.mean() * weights) * 252 )
  ret_arr[ind] = exp_ret

  exp_vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
  vol_arr[ind] = exp_vol

  sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]

sharpe_arr.max()

sharpe_arr.argmax()

all_weights[share_arr.argmax(), :]
max_sr_ret = ret_arr[share_arr.argmax()]
max_sr_vol = vol_arr[share_arr.argmax()]

plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='plasma')
plt.colorbar(label='Share Ration')
plt.xlabel('Volatility')
plt.ylabel('Returns')

plt.scatter(max_sr_vol, max_sr_ret, c='red', s=50, edgecolors='black')

# Part III
# Using minimizing techniques to find optimal portfolio allocaiton

def get_ret_vol_sr(weights):
  weights = np.array(weights)
  ret = np.sum(lot_ret.mean() * weights) * 252
  vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
  sr = ret/vol
  return np.array([ret, vol, sr])

from scipy.optimize import minimize

def neg_sharpe(weights):
  return get_ret_vol_sr(weights)[2] * -1

def check_sum(weights):
  # return 0 if the sum of the weights is 1
  return np.sum(weights) - 1

cons = ({ 'type': 'eq', 'fun': check_sum })
bounds = ((0,1),(0,1),(0,1),(0,1))
init_guess = [0.25, 0.25, 0.25, 0.25 ]

# sequencial least squares
opt_results = minimize(neg_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=cons)
opt_results.x

get_ret_vol_sr(opt_results.x)

# Efficient Frontier

def minimize_volatility(weights):
  return get_ret_vol_sr(weights)[1]


frontier_y = np.linspace(0,0.3,100)
frontier_volatility = []

# what is the best possible return for volatility y
for possible_return in frontier_y:

  # get ret and subtract possible return
  cons = ({ 'type': 'eq', 'fun': check_sum }, 
          { 'type': 'eq', 'fun': lambda w: get_ret_vol_sr(w)[0] - possible_return })

  result = minimize(neg_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=cons)
  frontier_volatility.append(result['fun'])

plt.plot(frontier_volatility, frontier_y, 'g--', linew=3)

# types of funds
# ETF - basket of tradeable securities
# Mutual funds - collecton of securities, run by a manager
# Hedge funds - pooled funds generally with alt investments, only aval to accredited investors

