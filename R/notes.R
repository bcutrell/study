#############################################################
## A bunch of unorganized notes from my datacamp courses
## bcutrell13@gmail.com - March 2019
#############################################################

# some good resources ->
# https://rstudio-pubs-static.s3.amazonaws.com/78839_afca73ae18194eaf8f1b86d399dde969.html
# http://www.thertrader.com/

library(quantmod)

# Get data
getSymbols('IVV')

# Plot % return
diff_ivv <- diff(IVV$IVV.Adjusted)

head(diff_ivv)

plot(diff_ivv)

# Plot the original random_walk data
ts.plot(random_walk)

# Use abline(0, ...) to add time trend to the figure
abline(0,int_wn)

model_wn <- arima(rw_diff, order=c(0,0,0))

# Simulate an AR model with 0.5 slope
x <- arima.sim(model = list(ar=0.5), n = 100)

# Simulate an AR model with 0.9 slope
y <- arima.sim(model = list(ar=0.9), n = 100)

# Simulate an AR model with -0.75 slope
z <- arima.sim(model = list(ar=-0.75), n = 100)

# Plot your simulated data
plot.ts(cbind(x, y, z))

# Simulate and plot RW model
z <- arima.sim(model = list(order = c(0, 1, 0)), n = 200)

# Fit the MA model to Nile
MA <- arima(Nile, order = c(0,0,1))
print(MA)

# Plot Nile and MA_fit
ts.plot(Nile)
MA_fit <- Nile - resid(MA)
points(MA_fit, type = "l", col = 2, lty = 2)

white noise (WN), random walk (RW), autoregressive (AR), and simple moving average (MA)

Plot A shows autocorrelation for the first lag only, which is consistent with the expectations of the MA model. Plot B shows dissipating autocorrelation across several lags, consistent with the AR model. Plot C is consistent with a RW model with considerable autocorrelation for many lags. Finally. Plot D shows virtually no autocorrelation with any lags, consistent with a WN model. Understanding the logic behind these ACF plots is crucial for understanding how each model operates.

# Generate and plot white noise
WN <- arima.sim(model=list(order=(c(0,0,0))), n=200)
plot(WN)

# Generate and plot an MA(1) with parameter .9
MA <- arima.sim(model = list(order = c(0, 0, 1), ma = .9 ), n = 200)
plot(MA)

# Generate and plot an AR(2) with parameters 1.5 and -.75
AR <- arima.sim(model = list(order= c(2,0,0), ar=c(1.5, -0.75)), n = 200)
plot(AR)

# Generate 100 observations from the AR(1) model
x <- arima.sim(model = list(order = c(1, 0, 0), ar = .9), n = 100)

# Plot the generated data
plot(x)

# Plot the sample P/ACF pair
acf2(x)

# Fit an AR(1) to the data and examine the t-table
sarima(x, 1,0,0)

# You should always examine the residuals because the model assumes the errors are Gaussian white noise.


library(quantmod)
library(tidyverse)
library(ggplot2)

# https://github.com/tidyverse/tidyverse/issues/132
# https://github.com/r-lib/xml2/issues/232

# Get data
getSymbols('IVV')

# Plot % return
diff_ivv <- diff(IVV$IVV.Adjusted)

# plot <- plot(IVV$IVV.Adjusted)

plot <- ggplot(IVV$IVV.Adjusted)
ggsave('x.png', plot)
# http://www.thertrader.com/

# Generate monthly difference in unemployment
unemployment$us_monthlydiff <- diff(unemployment$us, lag = 1, differences = 1)

# Generate yearly difference in unemployment
unemployment$us_yearlydiff <- diff(unemployment$us, lag = 12, differences = 1)

# Plot US unemployment and annual difference
par(mfrow = c(2,1))
plot.xts(unemployment$us)
plot.xts(unemployment$us_yearlydiff, type = "h")

# Convert the daily frequency of sp500 to monthly frequency: sp500_monthly
sp500_monthly <- to.monthly(sp500)

# Print the first six rows of sp500_monthly
head(sp500_monthly, 6)

# Create sp500_returns using Return.calculate using the closing prices
sp500_returns <- Return.calculate(sp500_monthly$sp500.Close)

# Time series plot
plot.zoo(sp500_returns)

# Produce the year x month table
table.CalendarReturns(sp500_returns)

# Compute the annualized mean
Return.annualized(sp500_returns)

# Compute the annualized standard deviation
StdDev.annualized(sp500_returns)

# Compute the annualized Sharpe ratio: ann_sharpe
ann_sharpe <- Return.annualized(sp500_returns)/StdDev.annualized(sp500_returns)

# Compute all of the above at once using table.AnnualizedReturns()
table.AnnualizedReturns(sp500_returns)

# Calculate the mean, volatility, and Sharpe ratio of sp500_returns
returns_ann <- Return.annualized(sp500_returns)
sd_ann <- StdDev.annualized(sp500_returns)
sharpe_ann <- SharpeRatio.annualized(sp500_returns,rf)

# Plotting the 12-month rolling annualized mean
chart.RollingPerformance(R = sp500_returns, width = 12, FUN = "Return.annualized")

# Plotting the 12-month rolling annualized standard deviation
chart.RollingPerformance(R = sp500_returns, width = 12, FUN = "StdDev.annualized")

# Plotting the 12-month rolling annualized Sharpe ratio
chart.RollingPerformance(R = sp500_returns, width = 12, FUN = "SharpeRatio.annualized", Rf=rf)

# Fill in window for 2008
sp500_2008 <- window(sp500_returns, start = "2008-01-01", end = "2008-12-31")

# Create window for 2014
sp500_2014 <-window(sp500_returns, start = "2014-01-01", end = "2014-12-31")

# Plotting settings
par(mfrow = c(1, 2) , mar=c(3, 2, 2, 2))
names(sp500_2008) <- "sp500_2008"
names(sp500_2014) <- "sp500_2014"

# Plot histogram of 2008
chart.Histogram(sp500_2008, methods = c("add.density", "add.normal"))

# Plot histogram of 2014
chart.Histogram(sp500_2014, methods = c("add.density", "add.normal"))

# Calculate the SemiDeviation
SemiDeviation(sp500_monthly)

# Calculate the value at risk
VaR(sp500_monthly, p=0.05)
VaR(sp500_monthly, p=0.025)

# Calculate the expected shortfall
ES(sp500_monthly, p=0.05)
ES(sp500_monthly, p=0.025)

# Table of drawdowns
table.Drawdowns(sp500_monthly)

# Plot of drawdowns
chart.Drawdown(sp500_monthly)

# Create a grid
grid <- seq(from = 0, to = 1, by = 0.01)

# Initialize an empty vector for Sharpe ratios
vsharpe <- rep(NA, times = length(grid) )

# Create a for loop to calculate Sharpe ratios
for(i in 1:length(grid)) {
	weight <- grid[i]
	preturns <- weight * returns_equities + (1 - weight) * returns_bonds
	vsharpe[i] <- SharpeRatio.annualized(preturns)
}

# Plot weights and Sharpe ratio
plot(grid, vsharpe, xlab = "Weights", ylab= "Ann. Sharpe ratio")
abline(v = grid[vsharpe == max(vsharpe)], lty = 3)

# Create a scatter plot
chart.Scatter(returns_bonds, returns_equities, xlab = "bond returns", ylab = "equity returns", main = "bond-equity returns")

# Find the correlation
cor(returns_bonds, returns_equities)


# Merge returns_bonds and returns_equities
returns <- merge(returns_bonds, returns_equities)

# Find and visualize the correlation using chart.Correlation
chart.Correlation(returns)

# Visualize the rolling estimates using chart.RollingCorrelation
chart.RollingCorrelation(returns_bonds, returns_equities, width = 24)

# Create portfolio weights
weights <- c(0.40, 0.40, 0.10, 0.10)

# Create volatility budget
vol_budget <- StdDev(returns, portfolio_method = "component", weights = weights)
head(vol_budget)

# Make a table of weights and risk contribution
weights_percrisk <- cbind(weights, vol_budget$pct_contrib_StdDev)
colnames(weights_percrisk) <- c("weights", "perc vol contrib")

# Print the table
weights_percrisk

# Verify the class of returns
class(returns)

# Investigate the dimensions of returns
dim(returns)

# Create a vector of row means
ew_preturns <- rowMeans(returns)

# Cast the numeric vector back to an xts object
ew_preturns <- xts(ew_preturns, order.by = time(returns))

# Plot ew_preturns
plot(ew_preturns)

# Load tseries
library(tseries)

# Create an optimized portfolio of returns
opt <- portfolio.optim(returns)

# Create pf_weights
pf_weights <- opt$pw

# Assign asset names
names(pf_weights) <- colnames(returns)

# Select optimum weights opt_weights
opt_weights <- pf_weights[pf_weights >= 0.01]


# Bar plot of opt_weights
barplot(opt_weights)

# Print expected portfolio return and volatility
opt$pm
opt$ps

# Create portfolio with target return of average returns
pf_mean <- portfolio.optim(returns, pm = mean(returns))

# Create portfolio with target return 10% greater than average returns
pf_10plus <- portfolio.optim(returns, pm = 1.1 * mean(returns))

# Print the standard deviations of both portfolios
pf_mean$ps
pf_10plus$ps


# Calculate the proportion increase in standard deviation
(pf_10plus$ps - pf_mean$ps) / (pf_mean$ps)

# Create vectors of maximum weights
max_weights1 <- rep(1, ncol(returns))
max_weights2 <- rep(0.10, ncol(returns))
max_weights3 <- rep(0.05, ncol(returns))

# Create an optimum portfolio with max weights of 100%
opt1 <- portfolio.optim(returns, reshigh = max_weights1)

# Create an optimum portfolio with max weights of 10%
opt2 <- portfolio.optim(returns, reshigh = max_weights2)

# Create an optimum portfolio with max weights of 5%
opt3 <- portfolio.optim(returns, reshigh = max_weights3)

# Calculate how many assets have a weight that is greater than 1% for each portfolio
sum(opt1$pw > .01)
sum(opt2$pw > .01)
sum(opt3$pw > .01)

# Print portfolio volatilites
opt1$ps
opt2$ps
opt3$ps

