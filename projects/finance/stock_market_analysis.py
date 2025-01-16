import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
# %matplotlib inline

# from pandas.io.data import DataReader
from pandas_datareader.data import DataReader
from datetime import datetime

# Fama/French Data
# DataReader('5_Industry_Portfolios', 'famafrench')

def collect_stock_data():
    tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
    end = datetime.now()
    start = datetime(end.year-1, end.month, end.day)
    for stock in tech_list:
      globals()[stock] = DataReader(stock, 'quandl', start, end)

def adj_close_plot(stock_df):
    stock_df['Adj Close'].plot(legend=True, figsize=(18,4))

def volume_plot(stock_df):
    stock_df['Adj Close'].plot(legend=True, figsize=(18,4))

def ma_plot(stock_df):
    stock_df[['Adj Close','MA for 10 days','MA for 20 days','MA for 50 days']].plot(subplots=False,figsize=(10,4))

def daily_return_plot(stock_df):
    stock_df['Daily Return'].plot(figsize=(12,4),legend=True,linestyle='--',marker='o')

def daily_distplot(stock_df):
    sns.distplot(stock_df['Daily Return'].dropna(), bins=100, color='purple')

def set_ma(stock_df, ma_day=[10,20,50]):
    for ma in ma_day:
        column_name = "MA for %s days" %(str(ma))
        stock_df[column_name]=pd.rolling_mean(stock_df['Adj Close'],ma)

def set_daily_return(stock_df):
    stock_df['Daily Return'] = AAPL['Adj Close'].pct_change()

def tech_summary():
    closing_df = DataReader(['AAPL','GOOG','MSFT','AMZN'],'yahoo',start,end)['Adj Close']
    tech_rets = closing_df.pct_change()

    # from IPython.display import SVG
    # SVG(url='http://upload.wikimedia.org/wikipedia/commons/d/d4/Correlation_examples2.svg')
    sns.jointplot('GOOG','GOOG',tech_rets,kind='scatter',color='seagreen')
    sns.jointplot('GOOG','MSFT',tech_rets,kind='scatter')
    sns.pairplot(tech_rets.dropna())

    # Set up our figure by naming it returns_fig, call PairPLot on the DataFrame
    returns_fig = sns.PairGrid(tech_rets.dropna())

    # Using map_upper we can specify what the upper triangle will look like.
    returns_fig.map_upper(plt.scatter,color='purple')

    # We can also define the lower triangle in the figure, inclufing the plot type (kde) or the color map (BluePurple)
    returns_fig.map_lower(sns.kdeplot,cmap='cool_d')

    # Finally we'll define the diagonal as a series of histogram plots of the daily return
    returns_fig.map_diag(plt.hist,bins=30)

    # Set up our figure by naming it returns_fig, call PairPLot on the DataFrame
    returns_fig = sns.PairGrid(closing_df)

    # Using map_upper we can specify what the upper triangle will look like.
    returns_fig.map_upper(plt.scatter,color='purple')

    # We can also define the lower triangle in the figure, inclufing the plot type (kde) or the color map (BluePurple)
    returns_fig.map_lower(sns.kdeplot,cmap='cool_d')

    # Finally we'll define the diagonal as a series of histogram plots of the closing price
    returns_fig.map_diag(plt.hist,bins=30)

    # Let's go ahead and use sebron for a quick correlation plot for the daily returns
    sns.corrplot(tech_rets.dropna(),annot=True)

    return tech_rets

def tech_risk(tech_rets):
    rets = tech_rets.dropna()
    area = np.pi*20
    plt.scatter(rets.mean(), rets.std(),alpha = 0.5,s =area)

    # Set the x and y limits of the plot (optional, remove this if you don't see anything in your plot)
    plt.ylim([0.01,0.025])
    plt.xlim([-0.003,0.004])

    #Set the plot axis titles
    plt.xlabel('Expected returns')
    plt.ylabel('Risk')

    # Label the scatter plots, for more info on how this is done, chekc out the link below
    # http://matplotlib.org/users/annotations_guide.html
    for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
        plt.annotate(
            label,
            xy = (x, y), xytext = (50, 50),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3,rad=-0.3'))

def value_at_risk(rets):
    sns.distplot(AAPL['Daily Return'].dropna(),bins=100,color='purple')
    # The 0.05 empirical quantile of daily returns
    rets['AAPL'].quantile(0.05)
    # >> -0.019
    # The 0.05 empirical quantile of daily returns is at -0.019.
    # That means that with 95% confidence, our worst daily loss will not exceed 1.9%.
    # If we have a 1 million dollar investment, our one-day 5% VaR is 0.019 * 1,000,000 = $19,000.

def var_monte_carlo(rets):
    # geometric Brownian motion (GBM),
    # changeS = S(drift + shock)
    # drift = avg daily return * change in time
    # shock = std of returns
    # Set up our time horizon
    days = 365

    # Now our delta
    dt = 1/days

    # Now let's grab our mu (drift) from the expected return data we got for AAPL
    mu = rets.mean()['GOOG']

    # Now let's grab the volatility of the stock from the std() of the average return
    sigma = rets.std()['GOOG']
    def stock_monte_carlo(start_price,days,mu,sigma):
        ''' This function takes in starting stock price, days of simulation,mu,sigma, and returns simulated price array'''

        # Define a price array
        price = np.zeros(days)
        price[0] = start_price
        # Schok and Drift
        shock = np.zeros(days)
        drift = np.zeros(days)

        # Run price array for number of days
        for x in xrange(1,days):

            # Calculate Schock
            shock[x] = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt))
            # Calculate Drift
            drift[x] = mu * dt
            # Calculate Price
            price[x] = price[x-1] + (price[x-1] * (drift[x] + shock[x]))

        return price

    # Get start price from GOOG.head()
    start_price = 569.85

    for run in xrange(100):
        plt.plot(stock_monte_carlo(start_price,days,mu,sigma))
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.title('Monte Carlo Analysis for Google')

    # Example of histogram for a larger run
    # Set a large numebr of runs
    runs = 10000

    # Create an empty matrix to hold the end price data
    simulations = np.zeros(runs)

    # Set the print options of numpy to only display 0-5 points from an array to suppress output
    np.set_printoptions(threshold=5)

    for run in xrange(runs):
        # Set the simulation data point as the last stock price for that run
        simulations[run] = stock_monte_carlo(start_price,days,mu,sigma)[days-1]

    # Now we'lll define q as the 1% empirical qunatile, this basically means that 99% of the values should fall between here
    q = np.percentile(simulations, 1)

    # Now let's plot the distribution of the end prices
    plt.hist(simulations,bins=200)

    # Using plt.figtext to fill in some additional information onto the plot

    # Starting Price
    plt.figtext(0.6, 0.8, s="Start price: $%.2f" %start_price)
    # Mean ending price
    plt.figtext(0.6, 0.7, "Mean final price: $%.2f" % simulations.mean())

    # Variance of the price (within 99% confidence interval)
    plt.figtext(0.6, 0.6, "VaR(0.99): $%.2f" % (start_price - q,))

    # Display 1% quantile
    plt.figtext(0.15, 0.6, "q(0.99): $%.2f" % q)

    # Plot a line at the 1% quantile result
    plt.axvline(x=q, linewidth=4, color='r')

    # Title
    plt.title(u"Final price distribution for Google Stock after %s days" % days, weight='bold');

    # interpretation
    # This basically menas for every initial stock you purchase your putting about $18.38
    # at risk 99% of the time from our Monte Carlo Simulation.


if __name__ == '__main__':
    collect_stock_data()

